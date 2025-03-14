from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SupportMessage
from .forms import SupportMessageForm

# Create your views here.

@login_required
def support_messages(request):
    messages = SupportMessage.objects.filter(user=request.user)
    return render(request, 'customer_support/messages.html', {'messages': messages})

@login_required
def send_support_message(request):
    if request.method == "POST":
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return redirect('support_messages')
    else:
        form = SupportMessageForm()
    return render(request, 'customer_support/send_message.html', {'form': form})
