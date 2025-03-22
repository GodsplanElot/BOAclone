from django import forms
from .models import WithdrawalRequest

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['account_number', 'account_holder_name', 'sort_code', 'amount', 'payment_method']

        widgets = {
            'account_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Account Number'}),
            'account_holder_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Account Holder Name'}),
            'sort_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Sort Code'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Amount'}),
            'payment_method': forms.Select(attrs={'class': 'form-input'}, choices=[
                ('Bank Transfer', 'Bank Transfer'),
                ('PayPal', 'PayPal'),
                ('Crypto Wallet', 'Crypto Wallet'),
            ]),
        }
