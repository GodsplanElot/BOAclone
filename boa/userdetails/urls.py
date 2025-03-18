from django.urls import path
from .views import profile_view, update_profile

urlpatterns = [
    path('profile/update/', update_profile, name='update_profile'),
]
