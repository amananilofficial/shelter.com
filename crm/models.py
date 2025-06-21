from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import os
import json

User = get_user_model()

class CRMRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='crm_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Ensure user has staff access to admin
        if self.user and not self.user.is_staff:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name = "CRM Role"
        verbose_name_plural = "CRM Roles"

class Customer(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('inactive', 'Inactive'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    source = models.CharField(max_length=100, blank=True, help_text="How did they find us?")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_customers')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

class CustomerInteraction(models.Model):
    INTERACTION_TYPES = [
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('whatsapp', 'WhatsApp'),
        ('visit', 'Site Visit'),
        ('other', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    interaction_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.interaction_type} - {self.interaction_date.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-interaction_date']

class CustomerUpload(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    file = models.FileField(upload_to='crm/uploads/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_records = models.IntegerField(default=0)
    processed_records = models.IntegerField(default=0)
    failed_records = models.IntegerField(default=0)
    error_log = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.original_filename} - {self.status}"
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Customer Upload"
        verbose_name_plural = "Customer Uploads"

class CustomerHistory(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('status_changed', 'Status Changed'),
        ('assigned', 'Assigned'),
        ('note_added', 'Note Added'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    field_changed = models.CharField(max_length=100, blank=True)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    reason = models.TextField(help_text="Reason for this change")
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.action} by {self.changed_by.username}"
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = "Customer History"
        verbose_name_plural = "Customer Histories"

class DataTransfer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('received', 'Received'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    TARGET_APP_CHOICES = [
        ('agents', 'Agents App'),
        ('team', 'Team App'),
        ('marketing', 'Marketing App'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transfers')
    target_app = models.CharField(max_length=20, choices=TARGET_APP_CHOICES)
    target_manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transfers')
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transfers')
    transfer_reason = models.TextField(help_text="Reason for transferring this customer")
    customer_request = models.TextField(blank=True, help_text="What the customer is looking for")
    priority = models.CharField(max_length=20, choices=Customer.PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer.full_name} -> {self.target_app} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Data Transfer"
        verbose_name_plural = "Data Transfers"
