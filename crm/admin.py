from django.contrib import admin
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html
import csv
import xlwt
from .models import CRMRole, Customer, CustomerInteraction, CustomerUpload, CustomerHistory, DataTransfer



class CRMRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email')
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role == 'admin'
        except CRMRole.DoesNotExist:
            return False

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'status', 'priority', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'assigned_to', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering = ('-created_at',)
    actions = ['export_as_csv', 'export_as_excel']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'whatsapp')
        }),
        ('Address', {
            'fields': ('address', 'city')
        }),        
        ('CRM Data', {
            'fields': ('status', 'priority', 'source', 'assigned_to', 'notes')
        }),
    )
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager', 'employee']
        except CRMRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            # All CRM users can modify customer records
            return crm_role.role in ['admin', 'manager', 'employee']
        except CRMRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            # Only admin and manager can delete
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            # All CRM users can see all customers
            return qs
        except CRMRole.DoesNotExist:
            return qs.none()
        return qs
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Status', 'Priority', 'Source', 'Assigned To', 'Created At'])
        
        for customer in queryset:
            writer.writerow([
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.phone,
                customer.status,
                customer.priority,
                customer.source,
                customer.assigned_to.username if customer.assigned_to else '',
                customer.created_at
            ])
        
        return response
    export_as_csv.short_description = "Export selected customers as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Customers')
        
        row_num = 0
        columns = ['First Name', 'Last Name', 'Email', 'Phone', 'Status', 'Priority', 'Source', 'Assigned To', 'Created At']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for customer in queryset:
            row_num += 1
            ws.write(row_num, 0, customer.first_name)
            ws.write(row_num, 1, customer.last_name)
            ws.write(row_num, 2, customer.email)
            ws.write(row_num, 3, customer.phone)
            ws.write(row_num, 4, customer.status)
            ws.write(row_num, 5, customer.priority)
            ws.write(row_num, 6, customer.source)
            ws.write(row_num, 7, customer.assigned_to.username if customer.assigned_to else '')
            ws.write(row_num, 8, str(customer.created_at))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected customers as Excel"

class CustomerInteractionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'interaction_type', 'subject', 'interaction_date', 'created_by')
    list_filter = ('interaction_type', 'interaction_date', 'created_by')
    search_fields = ('customer__first_name', 'customer__last_name', 'subject')
    ordering = ('-interaction_date',)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager', 'employee']
        except CRMRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            if crm_role.role in ['admin', 'manager']:
                return True
            # Employees cannot modify interactions
            return False
        except CRMRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role == 'admin'
        except CRMRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            if crm_role.role in ['admin', 'manager']:
                return qs
            elif crm_role.role == 'employee':
                # Employees can only see interactions for customers assigned to them
                return qs.filter(customer__assigned_to=request.user)
        except CRMRole.DoesNotExist:
            return qs.none()
        return qs
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new interaction
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class CustomerUploadAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'uploaded_by', 'uploaded_at', 'status', 'total_records', 'processed_records', 'failed_records')
    list_filter = ('status', 'uploaded_at', 'uploaded_by')
    search_fields = ('original_filename',)
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_by', 'uploaded_at', 'total_records', 'processed_records', 'failed_records', 'error_log')
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role == 'admin'
        except CRMRole.DoesNotExist:
            return False

class CustomerHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'action', 'field_changed', 'changed_by', 'changed_at')
    list_filter = ('action', 'changed_by', 'changed_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'reason')
    ordering = ('-changed_at',)
    readonly_fields = ('customer', 'action', 'field_changed', 'old_value', 'new_value', 'reason', 'changed_by', 'changed_at')
    
    def has_add_permission(self, request):
        # History records are created automatically
        return False
    
    def has_change_permission(self, request, obj=None):
        # History records should not be modified
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role == 'admin'
        except CRMRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            # All CRM users can see history
            return qs
        except CRMRole.DoesNotExist:
            return qs.none()

class DataTransferAdmin(admin.ModelAdmin):
    list_display = ('customer', 'target_app', 'target_manager', 'status', 'sent_by', 'created_at')
    list_filter = ('target_app', 'status', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'transfer_reason')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Transfer Information', {
            'fields': ('customer', 'target_app', 'target_manager')
        }),
        ('Details', {
            'fields': ('transfer_reason', 'customer_request', 'priority', 'notes')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role in ['admin', 'manager']
        except CRMRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            crm_role = CRMRole.objects.get(user=request.user)
            return crm_role.role == 'admin'
        except CRMRole.DoesNotExist:
            return False
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new transfer
            obj.sent_by = request.user
        super().save_model(request, obj, form, change)

# Register models
admin.site.register(CRMRole, CRMRoleAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerInteraction, CustomerInteractionAdmin)
admin.site.register(CustomerUpload, CustomerUploadAdmin)
admin.site.register(CustomerHistory, CustomerHistoryAdmin)
admin.site.register(DataTransfer, DataTransferAdmin)
