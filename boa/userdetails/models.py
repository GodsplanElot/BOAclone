from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Basic Info
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()



    # Account Info
    ACCOUNT_TYPES = [('Basic', 'Basic'), ('Premium', 'Premium')]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='Basic')
    branch = models.CharField(max_length=100)
    kyc_status = models.BooleanField(default=False)
    linked_account = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"
