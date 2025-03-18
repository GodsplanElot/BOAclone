from django.contrib import admin
from .models import UserDetails
# Register your models here.


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'branch', 'kyc_status', 'date_joined')
    list_filter = ('kyc_status', 'account_type')
