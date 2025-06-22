from django.contrib import admin
from django.http import HttpResponse
import csv
import xlwt
from .models import Listening, Contact, Quickcontact, Newsletter

@admin.register(Listening)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'agent', 'location', 'price', 'status', 'bedrooms', 'bathrooms', 'available', 'created')
    list_filter = ('status', 'available', 'agent', 'created', 'is_featured', 'marketing_priority')
    search_fields = ('title', 'location', 'description')
    actions = ['export_as_csv', 'export_as_excel', 'mark_as_featured', 'mark_as_unavailable']
    ordering = ('-created',)
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        # Check all possible roles
        for app_name in ['agent_role', 'team_role', 'crm_role', 'marketing_role']:
            try:
                role = getattr(request.user, app_name, None)
                if role and role.role in ['admin', 'manager']:
                    return True
            except:
                continue
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Check all possible roles
        for app_name in ['agent_role', 'team_role', 'crm_role', 'marketing_role']:
            try:
                role = getattr(request.user, app_name, None)
                if role and role.role in ['admin', 'manager']:
                    return True
            except:
                continue
        return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Only admins can delete
        for app_name in ['agent_role', 'team_role', 'crm_role', 'marketing_role']:
            try:
                role = getattr(request.user, app_name, None)
                if role and role.role == 'admin':
                    return True
            except:
                continue
        return False
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected listings as featured"
    
    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_as_unavailable.short_description = "Mark selected listings as unavailable"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="listings.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'Agent', 'Location', 'Price', 'Status', 'Bedrooms', 'Bathrooms', 'Area', 'Kitchen', 'Garage', 'Available', 'Featured', 'Created'])
        
        for listing in queryset:
            writer.writerow([
                listing.title,
                listing.agent.name,
                listing.location,
                listing.price,
                listing.status,
                listing.bedrooms,
                listing.bathrooms,
                listing.area,
                listing.kitchen,
                listing.garage,
                listing.available,
                listing.is_featured,
                listing.created
            ])
        
        return response
    export_as_csv.short_description = "Export selected listings as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="listings.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Listings')
        
        row_num = 0
        columns = ['Title', 'Agent', 'Location', 'Price', 'Status', 'Bedrooms', 'Bathrooms', 'Area', 'Kitchen', 'Garage', 'Available', 'Featured', 'Created']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for listing in queryset:
            row_num += 1
            ws.write(row_num, 0, listing.title)
            ws.write(row_num, 1, listing.agent.name)
            ws.write(row_num, 2, listing.location)
            ws.write(row_num, 3, str(listing.price))
            ws.write(row_num, 4, listing.status)
            ws.write(row_num, 5, listing.bedrooms)
            ws.write(row_num, 6, listing.bathrooms)
            ws.write(row_num, 7, listing.area)
            ws.write(row_num, 8, listing.kitchen)
            ws.write(row_num, 9, listing.garage)
            ws.write(row_num, 10, listing.available)
            ws.write(row_num, 11, listing.is_featured)
            ws.write(row_num, 12, str(listing.created))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected listings as Excel"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    actions = ['export_as_csv', 'export_as_excel']
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Message', 'Created At'])
        
        for contact in queryset:
            writer.writerow([
                contact.name,
                contact.email,
                contact.phone,
                contact.message,
                contact.created_at
            ])
        
        return response
    export_as_csv.short_description = "Export selected contacts as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="contacts.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Contacts')
        
        row_num = 0
        columns = ['Name', 'Email', 'Phone', 'Message', 'Created At']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for contact in queryset:
            row_num += 1
            ws.write(row_num, 0, contact.name)
            ws.write(row_num, 1, contact.email)
            ws.write(row_num, 2, contact.phone)
            ws.write(row_num, 3, contact.message)
            ws.write(row_num, 4, str(contact.created_at))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected contacts as Excel"

@admin.register(Quickcontact)
class QuickContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    actions = ['export_as_csv', 'export_as_excel']
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quick_contacts.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone'])
        
        for contact in queryset:
            writer.writerow([
                contact.name,
                contact.email,
                contact.phone
            ])
        
        return response
    export_as_csv.short_description = "Export selected quick contacts as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="quick_contacts.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Quick Contacts')
        
        row_num = 0
        columns = ['Name', 'Email', 'Phone']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for contact in queryset:
            row_num += 1
            ws.write(row_num, 0, contact.name)
            ws.write(row_num, 1, contact.email)
            ws.write(row_num, 2, contact.phone)
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected quick contacts as Excel"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'whatsapp_updates', 'is_active', 'date_subscribed')
    list_filter = ('whatsapp_updates', 'is_active', 'date_subscribed')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-date_subscribed',)
    actions = ['export_as_csv', 'export_as_excel', 'activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"
    
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'WhatsApp Updates', 'Is Active', 'Date Subscribed'])
        
        for subscriber in queryset:
            writer.writerow([
                subscriber.name,
                subscriber.email,
                subscriber.phone,
                subscriber.whatsapp_updates,
                subscriber.is_active,
                subscriber.date_subscribed
            ])
        
        return response
    export_as_csv.short_description = "Export selected subscribers as CSV"
    
    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Newsletter Subscribers')
        
        row_num = 0
        columns = ['Name', 'Email', 'Phone', 'WhatsApp Updates', 'Is Active', 'Date Subscribed']
        
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num])
        
        for subscriber in queryset:
            row_num += 1
            ws.write(row_num, 0, subscriber.name)
            ws.write(row_num, 1, subscriber.email)
            ws.write(row_num, 2, subscriber.phone or '')
            ws.write(row_num, 3, subscriber.whatsapp_updates)
            ws.write(row_num, 4, subscriber.is_active)
            ws.write(row_num, 5, str(subscriber.date_subscribed))
        
        wb.save(response)
        return response
    export_as_excel.short_description = "Export selected subscribers as Excel"


