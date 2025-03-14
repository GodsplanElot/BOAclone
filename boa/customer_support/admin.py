from django.contrib import admin
from .models import SupportMessage

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'is_resolved', 'timestamp')
    search_fields = ('user__username', 'subject', 'message')
    list_filter = ('is_resolved',)
    readonly_fields = ('user', 'subject', 'message', 'timestamp')  # Users cannot edit these

    def get_queryset(self, request):
        """Restrict normal users from seeing messages in admin."""
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs  # Staff can see all messages
        return qs.filter(user=request.user)  # Users can only see their own

    def has_change_permission(self, request, obj=None):
        """Allow only staff users to respond to messages."""
        if obj and not request.user.is_staff:
            return False
        return super().has_change_permission(request, obj)
