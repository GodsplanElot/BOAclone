from django.shortcuts import render
from userdetails.models import UserDetails
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import Transaction


# Create your views here.
def home(request):
    return render(request, 'bankPages/home.html')
# Create your views here.
def about(request):
    return render(request, 'bankPages/about.html')
def service(request):
    return render(request, 'bankPages/service.html')
def contact(request):
    return render(request, 'bankPages/contact.html')

@login_required
def dashboard(request):
    # Get the logged-in user's profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)


    # Pass the balance to the template
    context = {
        'balance': user_profile.balance,
        'account_number': user_profile.account_number,  # Add account number here
    }
    return render(request, 'bankPages/dashboard.html', context)


@login_required
def deposit(request):
    return render(request, 'bankPages/deposit.html')

@login_required
def withdraw(request):
    return render(request, 'bankPages/withdraw.html')

@login_required
def transactions(request):
    user_transactions = Transaction.objects.filter(receiver=request.user).order_by('-timestamp')

    context = {'transactions': user_transactions}
    return render(request, 'bankPages/transactions.html', context)

@login_required
def profile(request):
    # Get or create UserDetails (for user information)
    user_details, created = UserDetails.objects.get_or_create(user=request.user)

    # Get UserProfile (for account number and balance)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None  # Handle case where user has no UserProfile yet

    return render(request, 'bankPages/profile.html', {
        'profile': user_details,
        'user_profile': user_profile,
    })