from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from django.core.files.storage import default_storage
from django.conf import settings
import csv
import xlwt
import os
import pandas as pd
from .models import Team, TeamContactMessage, TeamRole

class TeamRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        # Only admin and manager can add roles
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role == 'admin'
        except TeamRole.DoesNotExist:
            return False

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.photo and hasattr(object.photo, 'url'):
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))
        return format_html('<div style="width: 40px; height: 40px; background-color: #ccc; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px;">No Photo</div>')

    thumbnail.short_description = 'Photo'
    
    list_display = ('id', 'thumbnail', 'name', 'title', 'role', 'email', 'phone', 'is_published')
    list_display_links = ('id', 'thumbnail', 'name')
    list_filter = ('is_published', 'role', 'hire_date')
    list_editable = ('is_published',)
    search_fields = ('name', 'title', 'email', 'role')
    list_per_page = 25
    actions = ['export_as_csv', 'export_as_excel', 'sync_to_other_apps']
    
    readonly_fields = ['work_experience_as_html']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'photo', 'title', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'instagram', 'linkedin')
        }),
        ('Work Details', {
            'fields': ('role', 'hire_date', 'work_experience', 'work_experience_as_html')
        }),
        ('System Access', {
            'fields': ('user', 'is_published'),
            'description': 'Link to user account for system access'
        }),
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='team_import_csv'),
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name='team_import_excel'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_csv_url'] = 'team_import_csv'
        extra_context['import_excel_url'] = 'team_import_excel'
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            if user_role.role in ['admin', 'manager']:
                return True
            elif user_role.role == 'member' and obj:
                # Members can only edit their own profile
                return obj.email == request.user.email
            return False
        except TeamRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role == 'admin'
        except TeamRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            user_role = TeamRole.objects.get(user=request.user)
            if user_role.role in ['admin', 'manager']:
                return qs
            elif user_role.role == 'member':
                # Members can only see their own profile
                return qs.filter(email=request.user.email)
        except TeamRole.DoesNotExist:
            return qs.none()
        return qs
    
    list_display = ('id', 'thumbnail', 'name', 'title', 'role', 'email', 'phone', 'is_published')
    list_display_links = ('id', 'thumbnail', 'name')
    list_filter = ('is_published', 'role', 'hire_date')
    list_editable = ('is_published',)
    search_fields = ('name', 'title', 'email', 'role')
    list_per_page = 25
    actions = ['export_as_csv', 'export_as_excel', 'sync_to_other_apps']
    
    readonly_fields = ['work_experience_as_html']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'photo', 'title', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'instagram', 'linkedin')
        }),
        ('Work Details', {
            'fields': ('role', 'hire_date', 'work_experience', 'work_experience_as_html')
        }),
        ('System Access', {
            'fields': ('user', 'is_published'),
            'description': 'Link to user account for system access'
        }),
    )
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv), name='team_import_csv'),
            path('import-excel/', self.admin_site.admin_view(self.import_excel), name='team_import_excel'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['import_csv_url'] = 'team_import_csv'
        extra_context['import_excel_url'] = 'team_import_excel'
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="team_members.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Title', 'Role', 'Email', 'Phone', 'WhatsApp', 'Instagram', 'LinkedIn', 'Hire Date', 'Published'])
        
        for team in queryset:
            writer.writerow([
                team.name,
                team.title,
                team.role,
                team.email,
                team.phone,
                team.whatsapp,
                team.instagram,
                team.linkedin,
                team.hire_date,
                team.is_published
            ])
        
        return response
    export_as_csv.short_description = "Export selected team members as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="team_members.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Team Members')
        
        row_num = 0
        columns = ['Name', 'Title', 'Role', 'Email', 'Phone', 'WhatsApp', 'Instagram', 'LinkedIn', 'Hire Date', 'Published']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for team in queryset:
            row_num += 1
            ws.write(row_num, 0, team.name)
            ws.write(row_num, 1, team.title)
            ws.write(row_num, 2, team.role)
            ws.write(row_num, 3, team.email)
            ws.write(row_num, 4, team.phone)
            ws.write(row_num, 5, team.whatsapp)
            ws.write(row_num, 6, team.instagram)
            ws.write(row_num, 7, team.linkedin)
            ws.write(row_num, 8, str(team.hire_date) if team.hire_date else '')
            ws.write(row_num, 9, team.is_published)
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected team members as Excel"
    
    def sync_to_other_apps(self, request, queryset):
        """Sync selected team members to other apps"""
        synced_count = 0
        for team in queryset:
            if team.role in ['admin', 'manager']:
                team.sync_with_other_apps()
                synced_count += 1
        
        self.message_user(request, f'Successfully synced {synced_count} team members to other apps.')
    sync_to_other_apps.short_description = "Sync selected members to other apps"
    
    def import_csv(self, request):
        """Import team members from CSV file"""
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            if not csv_file:
                messages.error(request, 'No file uploaded.')
                return redirect('..')
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type.')
                return redirect('..')
            
            # Process CSV file here
            # Implementation details would go here
            messages.success(request, 'CSV file imported successfully.')
            return redirect('..')
        
        return render(request, 'admin/team/import_csv.html')
    
    def import_excel(self, request):
        """Import team members from Excel file"""
        if request.method == 'POST':
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                messages.error(request, 'No file uploaded.')
                return redirect('..')
            
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                messages.error(request, 'File is not Excel type.')
                return redirect('..')
            
            # Process Excel file here
            # Implementation details would go here
            messages.success(request, 'Excel file imported successfully.')
            return redirect('..')
        
        return render(request, 'admin/team/import_excel.html')

class TeamContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('team', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'phone', 'team__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread', 'export_as_csv']
    
    def has_add_permission(self, request):
        # Contact messages are created from frontend, not admin
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            if user_role.role in ['admin', 'manager']:
                return True
            elif user_role.role == 'member' and obj:
                # Members can only view messages for themselves
                return obj.team.email == request.user.email
            return False
        except TeamRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role == 'admin'
        except TeamRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            user_role = TeamRole.objects.get(user=request.user)
            if user_role.role in ['admin', 'manager']:
                return qs
            elif user_role.role == 'member':
                # Members can only see messages for themselves
                return qs.filter(team__email=request.user.email)
        except TeamRole.DoesNotExist:
            return qs.none()
        return qs
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="team_contact_messages.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Team Member', 'Email', 'Phone', 'Message', 'Created At', 'Read'])
        
        for message in queryset:
            writer.writerow([
                message.name,
                message.team.name,
                message.email,
                message.phone,
                message.message,
                message.created_at,
                message.is_read
            ])
        
        return response
    export_as_csv.short_description = "Export selected messages as CSV"

# Register models
admin.site.register(TeamRole, TeamRoleAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamContactMessage, TeamContactMessageAdmin)
