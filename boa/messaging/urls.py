from django.urls import path
from .views import user_messages

urlpatterns = [
    path('messages/', user_messages, name='user_messages'),
]
