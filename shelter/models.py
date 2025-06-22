from django.db import models
from django.urls import reverse
from django.utils import timezone
from agents.models import Agent, AgentContact
# Create your models here.
class Listening(models.Model):
    STATUS_CHOICES = (
        ('rent', 'Rent'),
        ('sale', 'Sale'),
    )
    agent = models.ForeignKey(Agent,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200,unique=True,db_index=True)
    image = models.ImageField(upload_to='listings/%Y/%m/%d',blank=True)
    image2 = models.ImageField(upload_to='listings/%Y/%m/%d',blank=True)
    image3 = models.ImageField(upload_to='listings/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(null=False,max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.CharField(max_length=200)
    kitchen = models.IntegerField()
    garage = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rent')
    
    # Marketing fields
    is_featured = models.BooleanField(default=False, help_text="Featured on homepage")
    marketing_priority = models.CharField(
        max_length=20, 
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    
    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listing_detail',args=[str(self.slug)])

class Contact(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Contact from {self.name} on {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

class Quickcontact(models.Model):
    name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    phone = models.CharField(max_length=20, default='')
    
    def __str__(self):
        return self.name


# AgentContact model moved to agents app

class Newsletter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_updates = models.BooleanField(default=False)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-date_subscribed']


