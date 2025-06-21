from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import MarketingRole, PropertyCampaign, MarketingLead

class MarketingRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except MarketingRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except MarketingRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            return user_role.role == 'admin'
        except MarketingRole.DoesNotExist:
            return False

class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign_type', 'status', 'budget', 'start_date', 'end_date', 'created_by')
    list_filter = ('campaign_type', 'status', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'target_audience')
    ordering = ('-created_at',)
    actions = ['export_as_csv']
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except MarketingRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            if user_role.role in ['admin', 'manager']:
                return True
            elif user_role.role == 'employee' and obj:
                return obj.created_by == request.user
            return False
        except MarketingRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            return user_role.role == 'admin'
        except MarketingRole.DoesNotExist:
            return False
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="campaigns.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Type', 'Status', 'Budget', 'Start Date', 'End Date', 'Created By'])
        
        for campaign in queryset:
            writer.writerow([
                campaign.name,
                campaign.campaign_type,
                campaign.status,
                campaign.budget,
                campaign.start_date,
                campaign.end_date,
                campaign.created_by.username
            ])
        
        return response
    export_as_csv.short_description = "Export selected campaigns as CSV"

class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'source', 'status', 'assigned_to', 'created_at')
    list_filter = ('source', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)
    actions = ['export_as_csv']
    
    def has_add_permission(self, request):
        return request.user.is_authenticated
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            if user_role.role in ['admin', 'manager']:
                return True
            elif obj:
                return obj.assigned_to == request.user
            return False
        except MarketingRole.DoesNotExist:
            return obj and obj.assigned_to == request.user
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = MarketingRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except MarketingRole.DoesNotExist:
            return False
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Source', 'Status', 'Assigned To', 'Created At'])
        
        for lead in queryset:
            writer.writerow([
                lead.first_name,
                lead.last_name,
                lead.email,
                lead.phone,
                lead.source,
                lead.status,
                lead.assigned_to.username if lead.assigned_to else '',
                lead.created_at
            ])
        
        return response
    export_as_csv.short_description = "Export selected leads as CSV"

# Register models
admin.site.register(MarketingRole, MarketingRoleAdmin)
admin.site.register(PropertyCampaign, CampaignAdmin)
admin.site.register(MarketingLead, LeadAdmin)
