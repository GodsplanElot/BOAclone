from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WithdrawalForm

@login_required
def withdrawal_request(request):
    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            withdrawal.save()
            return render(request, "withdrawals/success.html")  # Redirect to a success page
    else:
        form = WithdrawalForm()

    return render(request, "withdrawals/withdraw.html", {"form": form})
