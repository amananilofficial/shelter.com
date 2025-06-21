from django.db import models
from datetime import datetime
from django.utils.html import format_html
from django.contrib.auth import get_user_model

User = get_user_model()

class AgentRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('agent', 'Agent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='agent')
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
        verbose_name = "Agent Role"
        verbose_name_plural = "Agent Roles"

# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='agent_profile')
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='agents/%Y/%m/%d')
    title = models.CharField(max_length=100, default='Real Estate Agent')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=30)
    instagram = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)
    work_experience = models.TextField(
        blank=True,
        help_text="Enter work experience points separated by the '|' character. Each point will be displayed as a separate bullet point on the frontend."
    )
    is_mvp = models.BooleanField(default=False, help_text="Whether this agent is an MVP (Most Valuable Player)")

    def work_experience_as_list(self):
        """Returns work_experience as a list of bullet points"""
        return [exp.strip() for exp in self.work_experience.split('|') if exp.strip()]

    def work_experience_as_html(self):
        """Returns work_experience as HTML bullet list"""
        items = self.work_experience_as_list()
        if not items:
            return "-"
        return format_html("<ul>{}</ul>", format_html("".join(f"<li>{item}</li>" for item in items)))

    def __str__(self):
        return self.name


class AgentContact(models.Model):
    agentname = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_subject = models.TextField(max_length=200)
    user_phone = models.CharField(max_length=20, null=True, blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.agentname}"

class AgentPropertyContact(models.Model):
    agentname = models.CharField(max_length=100)
    property_title = models.CharField(max_length=200)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20)
    user_subject = models.TextField(max_length=200)
    contact_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.property_title} - {self.agentname}"

class WorkNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_notes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    # Link to specific records (optional)
    related_customer_id = models.IntegerField(null=True, blank=True, help_text="Related customer ID if applicable")
    related_property_id = models.IntegerField(null=True, blank=True, help_text="Related property ID if applicable")
    related_lead_id = models.IntegerField(null=True, blank=True, help_text="Related lead ID if applicable")
    
    class Meta:
        ordering = ['-date_created']
        verbose_name = "Work Note"
        verbose_name_plural = "Work Notes"
    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.date_created.strftime('%Y-%m-%d')})"

# Add utility function for receiving CRM transfers
def receive_crm_transfer(transfer_data):
    """Receive customer data from CRM and create agent lead"""
    try:
        from crm.models import DataTransfer
        
        transfer_id = transfer_data.get('transfer_id')
        customer_data = transfer_data.get('customer_data')
        
        # Here you would create an agent lead or contact from the customer data
        # This is where the agents app would process incoming customer data
        
        # Update transfer status
        if transfer_id:
            transfer = DataTransfer.objects.get(id=transfer_id)
            transfer.status = 'received'
            transfer.save()
            
        return True
        
    except Exception as e:
        print(f"Error receiving CRM transfer: {str(e)}")
        return False
