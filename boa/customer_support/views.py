from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import SupportMessage
from .forms import SupportMessageForm

@login_required
def support_messages(request):
    if request.user.is_staff:  
        # Admins see all messages
        messages = SupportMessage.objects.all()
    else:
        # Users see only their own messages
        messages = SupportMessage.objects.filter(user=request.user)
    return render(request, 'customer_support/messages.html', {'messages': messages})

@login_required
def send_support_message(request):
    if request.method == "POST":
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user  # Set the logged-in user as sender
            message.save()
            return redirect('support_messages')
    else:
        form = SupportMessageForm()
    return render(request, 'customer_support/send_message.html', {'form': form})
