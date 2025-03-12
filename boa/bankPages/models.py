from django.db import models

# Create your models here.
from django.contrib.auth.models import User
import random
import string

# Function to generate a unique 10-digit account number
def generate_account_number():
    while True:
        account_number = ''.join(random.choices(string.digits, k=10))
        if not UserProfile.objects.filter(account_number=account_number).exists():
            return account_number

# Function to generate a 7-digit numeric Transaction ID
def generate_transaction_id():
    return ''.join(random.choices(string.digits, k=7))

# Function to generate a 7-character alphanumeric Session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

# User Profile Model to store account number
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    sender_name = models.CharField(max_length=255)  # Admin inputs sender name manually
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=7, unique=True, default=generate_transaction_id)
    session_id = models.CharField(max_length=7, unique=True, default=generate_session_id)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 'completed':
            if self.transaction_type == 'deposit':
                self.receiver.balance += self.amount
            elif self.transaction_type == 'withdrawal':
                self.receiver.balance -= self.amount
            elif self.transaction_type == 'transfer':
                sender_profile = UserProfile.objects.get(account_number=self.sender_name)  # Assuming sender is another user
                sender_profile.balance -= self.amount
                sender_profile.save()
                self.receiver.balance += self.amount
            self.receiver.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.receiver.user.username}"
