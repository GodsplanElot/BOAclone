from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'bankPages/home.html')
@login_required
def dashboard(request):
    return HttpResponse("This is the secured dashboard.")

@login_required
def deposit(request):
    return HttpResponse("Deposit page.")

@login_required
def withdraw(request):
    return HttpResponse("Withdrawal page.")

@login_required
def transactions(request):
    return HttpResponse("Transactions history page.")

@login_required
def profile(request):
    return HttpResponse("Profile page.")