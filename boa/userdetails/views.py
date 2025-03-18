from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserDetails
from .forms import UserDetailsForm
# Create your views here.




@login_required
def update_profile(request):
    profile, created = UserDetails.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserDetailsForm(instance=profile)

    return render(request, 'userdetails/update_profile.html', {'form': form})
