from django.contrib import admin
from .models import Listening, Quickcontact, Newsletter, Contact


admin.site.register(Listening)
admin.site.register(Quickcontact)
admin.site.register(Newsletter)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


