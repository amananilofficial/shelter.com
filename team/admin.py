from django.contrib import admin
from .models import Team, TeamContactMessage
from django.utils.html import format_html

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))

    thumbnail.short_description = 'Photo'
    
    list_display = ('id', 'thumbnail', 'name', 'title', 'email', 'phone', 'is_published')
    list_display_links = ('id', 'thumbnail', 'name')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('name', 'title', 'email')
    list_per_page = 25
    
    readonly_fields = ['work_experience_as_html']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'photo', 'title', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'instagram', 'linkedin')
        }),
        ('Work Details', {
            'fields': ('hire_date', 'work_experience', 'work_experience_as_html')
        }),
    )

class TeamContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'team', 'created_at', 'is_read')
    list_display_links = ('id', 'name')
    list_filter = ('is_read', 'created_at', 'team')
    list_editable = ('is_read',)
    search_fields = ('name', 'email', 'message')
    list_per_page = 25
    readonly_fields = ('created_at',)
    
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamContactMessage, TeamContactMessageAdmin)
