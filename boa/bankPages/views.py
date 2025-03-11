from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'bankPages/home.html')

@login_required
def dashboard(request):
    return render(request, 'bankPages/dashboard.html')

@login_required
def deposit(request):
    return render(request, 'bankPages/deposit.html')

@login_required
def withdraw(request):
    return render(request, 'bankPages/withdraw.html')

@login_required
def transactions(request):
    return render(request, 'bankPages/transactions.html')

@login_required
def profile(request):
    return render(request, 'bankPages/profile.html')