from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
import csv
import xlwt
from .models import Agent, AgentContact, AgentPropertyContact, AgentRole, WorkNote

class AgentRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role == 'admin'
        except AgentRole.DoesNotExist:
            return False

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone')
    search_fields = ('name', 'email', 'title')
    actions = ['export_as_csv', 'export_as_excel']
    fieldsets = (
        (None, {
            'fields': ('name', 'title', 'photo', 'email', 'phone', 'hire_date')
        }),
        ('Social Media', {
            'fields': ('whatsapp', 'instagram', 'linkedin')
        }),
        ('Profile Content', {
            'fields': ('description', 'work_experience'),
            'description': 'For work experience, enter each point/achievement separated by the | (pipe) character. Each point will be displayed as a bullet point on the frontend.'
        })
    )
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            # Employees can only view/edit their own profile
            elif agent_role.role == 'agent' and obj:
                return obj.email == request.user.email
            return False
        except AgentRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role == 'admin'
        except AgentRole.DoesNotExist:
            return False
      
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            elif agent_role.role == 'agent':
                # Employees can only see their own profile
                return qs.filter(email=request.user.email)
        except AgentRole.DoesNotExist:
            return qs.none()
        return qs
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="agents.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Title', 'Email', 'Phone', 'WhatsApp', 'Instagram', 'LinkedIn', 'Hire Date'])
        
        for agent in queryset:
            writer.writerow([
                agent.name,
                agent.title,
                agent.email,
                agent.phone,
                agent.whatsapp,
                agent.instagram,
                agent.linkedin,
                agent.hire_date
            ])
        
        return response
    export_as_csv.short_description = "Export selected agents as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="agents.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Agents')
        
        row_num = 0
        columns = ['Name', 'Title', 'Email', 'Phone', 'WhatsApp', 'Instagram', 'LinkedIn', 'Hire Date']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for agent in queryset:
            row_num += 1
            ws.write(row_num, 0, agent.name)
            ws.write(row_num, 1, agent.title)
            ws.write(row_num, 2, agent.email)
            ws.write(row_num, 3, agent.phone)
            ws.write(row_num, 4, agent.whatsapp)
            ws.write(row_num, 5, agent.instagram)
            ws.write(row_num, 6, agent.linkedin)
            ws.write(row_num, 7, str(agent.hire_date))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected agents as Excel"

class AgentContactAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'agentname', 'user_email', 'contact_date')
    list_filter = ('agentname', 'contact_date')
    search_fields = ('user_name', 'user_email', 'agentname')
    ordering = ('-contact_date',)
    actions = ['export_as_csv', 'export_as_excel']
    
    def has_add_permission(self, request):
        # Contacts are created from frontend, not admin
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            # Employees can only view contacts for themselves
            elif agent_role.role == 'agent' and obj:
                return obj.agentname == request.user.first_name + ' ' + request.user.last_name
            return False
        except AgentRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            elif agent_role.role == 'agent':
                # Employees can only see contacts for themselves
                agent_name = request.user.first_name + ' ' + request.user.last_name
                return qs.filter(agentname=agent_name)
        except AgentRole.DoesNotExist:
            return qs.none()
        return qs
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="agent_contacts.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['User Name', 'Agent Name', 'User Email', 'User Phone', 'Subject', 'Contact Date'])
        
        for contact in queryset:
            writer.writerow([
                contact.user_name,
                contact.agentname,
                contact.user_email,
                contact.user_phone,
                contact.user_subject,
                contact.contact_date
            ])
        
        return response
    export_as_csv.short_description = "Export selected contacts as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="agent_contacts.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Agent Contacts')
        
        row_num = 0
        columns = ['User Name', 'Agent Name', 'User Email', 'User Phone', 'Subject', 'Contact Date']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for contact in queryset:
            row_num += 1
            ws.write(row_num, 0, contact.user_name)
            ws.write(row_num, 1, contact.agentname)
            ws.write(row_num, 2, contact.user_email)
            ws.write(row_num, 3, contact.user_phone or '')
            ws.write(row_num, 4, contact.user_subject)
            ws.write(row_num, 5, str(contact.contact_date))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected contacts as Excel"

class AgentPropertyContactAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'agentname', 'property_title', 'user_email', 'contact_date')
    list_filter = ('agentname', 'contact_date', 'property_title')
    search_fields = ('user_name', 'user_email', 'agentname', 'property_title')
    ordering = ('-contact_date',)
    actions = ['export_as_csv', 'export_as_excel']
    
    def has_add_permission(self, request):
        # Property contacts are created from frontend, not admin
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            # Employees can only view contacts for themselves
            elif agent_role.role == 'agent' and obj:
                return obj.agentname == request.user.first_name + ' ' + request.user.last_name
            return False
        except AgentRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            elif agent_role.role == 'agent':
                # Employees can only see contacts for themselves
                agent_name = request.user.first_name + ' ' + request.user.last_name
                return qs.filter(agentname=agent_name)
        except AgentRole.DoesNotExist:
            return qs.none()
        return qs
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="agent_property_contacts.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['User Name', 'Agent Name', 'Property Title', 'User Email', 'User Phone', 'Subject', 'Contact Date'])
        
        for contact in queryset:
            writer.writerow([
                contact.user_name,
                contact.agentname,
                contact.property_title,
                contact.user_email,
                contact.user_phone,
                contact.user_subject,
                contact.contact_date
            ])
        
        return response
    export_as_csv.short_description = "Export selected property contacts as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="agent_property_contacts.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Agent Property Contacts')
        
        row_num = 0
        columns = ['User Name', 'Agent Name', 'Property Title', 'User Email', 'User Phone', 'Subject', 'Contact Date']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for contact in queryset:
            row_num += 1
            ws.write(row_num, 0, contact.user_name)
            ws.write(row_num, 1, contact.agentname)
            ws.write(row_num, 2, contact.property_title)
            ws.write(row_num, 3, contact.user_email)
            ws.write(row_num, 4, contact.user_phone)
            ws.write(row_num, 5, contact.user_subject)
            ws.write(row_num, 6, str(contact.contact_date))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected property contacts as Excel"

class WorkNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-date_created',)
    actions = ['export_as_csv']
    
    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'description')
        }),
        ('Related Records', {
            'fields': ('related_customer_id', 'related_property_id', 'related_lead_id'),
            'description': 'Optional: Link this note to specific records'
        }),
    )
    
    def has_add_permission(self, request):
        # All logged in users can add work notes
        return request.user.is_authenticated
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            elif obj:
                # Users can only edit their own notes
                return obj.user == request.user
            return False
        except AgentRole.DoesNotExist:
            # If no role, users can still edit their own notes
            return obj and obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role == 'admin':
                return True
            elif obj:
                # Users can delete their own notes
                return obj.user == request.user
            return False
        except AgentRole.DoesNotExist:
            # If no role, users can still delete their own notes
            return obj and obj.user == request.user
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            else:
                # Users can only see their own notes
                return qs.filter(user=request.user)
        except AgentRole.DoesNotExist:
            # If no role, users can still see their own notes
            return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new note
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="work_notes.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'User', 'Description', 'Created Date', 'Updated Date', 'Customer ID', 'Property ID', 'Lead ID'])
        
        for note in queryset:
            writer.writerow([
                note.title,
                note.user.username,
                note.description,
                note.date_created,
                note.date_updated,
                note.related_customer_id,
                note.related_property_id,
                note.related_lead_id
            ])
        
        return response
    export_as_csv.short_description = "Export selected work notes as CSV"

# Register models
admin.site.register(AgentRole, AgentRoleAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(AgentContact, AgentContactAdmin)
admin.site.register(AgentPropertyContact, AgentPropertyContactAdmin)
admin.site.register(WorkNote, WorkNoteAdmin)