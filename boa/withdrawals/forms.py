from django import forms
from .models import WithdrawalRequest

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'payment_method']
