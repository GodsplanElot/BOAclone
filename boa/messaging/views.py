from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
# Create your views here.

@login_required
def user_messages(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'messaging/messages.html', {'messages': messages})