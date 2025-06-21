from django.db import models
from django.contrib.auth import get_user_model
from shelter.models import Listening

User = get_user_model()

class MarketingRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='marketing_role')
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
        verbose_name = "Marketing Role"
        verbose_name_plural = "Marketing Roles"



class MarketingLead(models.Model):
    LEAD_SOURCES = [
        ('website', 'Website'),
        ('social_media', 'Social Media'),
        ('paid_ads', 'Paid Advertising'),
        ('email', 'Email Campaign'),
        ('referral', 'Referral'),
        ('walk_in', 'Walk-in'),
        ('phone', 'Phone Call'),
    ]
    
    LEAD_STATUS = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    source = models.CharField(max_length=20, choices=LEAD_SOURCES)
    status = models.CharField(max_length=20, choices=LEAD_STATUS, default='new')
    notes = models.TextField(blank=True)
    property_interest = models.ForeignKey(Listening, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']

class PropertyCampaign(models.Model):
    CAMPAIGN_TYPES = [
        ('featured', 'Featured Listing'),
        ('premium', 'Premium Promotion'),
        ('social', 'Social Media'),
        ('email', 'Email Campaign'),
        ('paid_ads', 'Paid Advertising'),
    ]
    
    CAMPAIGN_STATUS = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    property = models.ForeignKey(Listening, on_delete=models.CASCADE, related_name='marketing_campaigns')
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS, default='draft')
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    target_audience = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_campaigns')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_campaigns')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class PropertyPromotion(models.Model):
    PROMOTION_TYPES = [
        ('featured', 'Featured'),
        ('hot', 'Hot Deal'),
        ('new', 'New Listing'),
        ('reduced', 'Price Reduced'),
        ('urgent', 'Urgent Sale'),
    ]
    
    property = models.ForeignKey(Listening, on_delete=models.CASCADE, related_name='promotions')
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.property.title}"
    
    class Meta:
        ordering = ['-created_at']

class CampaignMetrics(models.Model):
    campaign = models.OneToOneField(PropertyCampaign, on_delete=models.CASCADE, related_name='metrics')
    views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    inquiries = models.IntegerField(default=0)
    leads_generated = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    cost_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Metrics for {self.campaign.name}"
