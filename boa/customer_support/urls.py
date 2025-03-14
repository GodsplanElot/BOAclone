from django.urls import path
from .views import support_messages, send_support_message

urlpatterns = [
    path('messages/', support_messages, name='support_messages'),
    path('send/', send_support_message, name='send_support_message'),
]