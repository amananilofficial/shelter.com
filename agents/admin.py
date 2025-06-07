from django.contrib import admin
from .models import Agent, AgentContact, AgentPropertyContact

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone')
    search_fields = ('name', 'email', 'title')
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

class AgentContactAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'agentname', 'user_email', 'contact_date')
    list_filter = ('agentname', 'contact_date')
    search_fields = ('user_name', 'user_email', 'agentname')
    ordering = ('-contact_date',)

class AgentPropertyContactAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'agentname', 'property_title', 'user_email', 'contact_date')
    list_filter = ('agentname', 'contact_date')
    search_fields = ('user_name', 'user_email', 'agentname', 'property_title')
    ordering = ('-contact_date',)

admin.site.register(Agent, AgentAdmin)
admin.site.register(AgentContact, AgentContactAdmin)
admin.site.register(AgentPropertyContact, AgentPropertyContactAdmin)