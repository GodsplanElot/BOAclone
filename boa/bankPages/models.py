from django.db import models
from decimal import Decimal
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
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

# Transaction Model
class Transaction(models.Model):
    sender_name = models.CharField(max_length=255)  # Superuser manually inputs this
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    session_id = models.CharField(max_length=7, unique=True, blank=True)
    transaction_id = models.CharField(max_length=7, unique=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure receiver has a UserProfile
        receiver_profile, created = UserProfile.objects.get_or_create(user=self.receiver)

        # Generate unique session_id and transaction_id
        if not self.session_id:
            self.session_id = generate_session_id()
        if not self.transaction_id:
            self.transaction_id = generate_transaction_id()

        # Automatically update receiver balance for deposits and transfers
        if self.status == 'completed':
            if self.transaction_type in ['deposit', 'transfer']:
                receiver_profile.balance += Decimal(self.amount)  
            elif self.transaction_type == 'withdrawal':
                receiver_profile.balance -= Decimal(self.amount)

            receiver_profile.save()  

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
