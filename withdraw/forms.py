from .models import WithdrawalData, WithdrawalRequest
from django import forms
from django.forms import TextInput


class WithDataForm(forms.ModelForm):
    class Meta:
        model = WithdrawalData
        fields = '__all__'
        exclude = ['user', 'active',]

        widgets = {
            'eth_address': TextInput(attrs={'placeholder': 'Ethereum Address', 'required': 'true',}),
        }

def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


class WithrawForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'
        exclude = ['user', 'active',]

        widgets = {
            'withdraw_amount': TextInput(attrs={'placeholder': 'Amount', 'required': 'true',}),
            'eth_address': TextInput(attrs={'placeholder': 'Ethereum Address', 'required': 'true',}),
        }