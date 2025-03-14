from django.urls import path
from .views import withdrawal_request

urlpatterns = [
    path("request/", withdrawal_request, name="withdrawal_request"),
]
