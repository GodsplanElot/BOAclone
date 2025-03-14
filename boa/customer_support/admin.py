from django.contrib import admin
from .models import SupportMessage
# Register your models here.

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'is_resolved', 'timestamp')
    search_fields = ('user__username', 'subject', 'message')
    list_filter = ('is_resolved',)

admin.site.site_header = "Customer Support Admin"
