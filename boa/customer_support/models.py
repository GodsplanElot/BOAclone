from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SupportMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_messages")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)  # Admin's reply
    is_resolved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Support Message from {self.user.username}"

