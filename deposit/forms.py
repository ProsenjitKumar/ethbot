from django import forms
from django.forms import TextInput
from .models import *


# -------------------------------
#                                |
#     Deposit Confirmation Form
#                                |
# -------------------------------


class DepositForm(forms.ModelForm):
    class Meta:
        model = DepositRequest
        fields = '__all__'
        exclude = ['user', 'active', 'confirmed',]

        widgets = {
            'amount_deposited': TextInput(attrs={'placeholder': 'Amount', 'required': 'true',}),
            'transaction_id': TextInput(attrs={'placeholder': 'Transaction ID', 'required': 'true',}),

        }


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = '__all__'
        exclude = ['user', 'active', 'confirmed',]


class TradingForm(forms.ModelForm):
    class Meta:
        model = Trading
        fields = '__all__'
        exclude = ['user', 'active', 'confirmed',]

        widgets = {
            'amount': TextInput(attrs={'placeholder': 'Amount', 'required': 'true', }),
        }

# class InvestmentRequestForm(forms.ModelForm):
#     scheme = forms.ChoiceField(choices=INVESTMENT_SELECT, required=True)
#     class Meta:
#         model = InvestmentRequest
#         fields = '__all__'
#         exclude = ['user', 'active',]
#
#         widgets = {
#             'amount': TextInput(attrs={'placeholder': 'Amount'}),
#         }


class TradingAccountForm(forms.ModelForm):
    class Meta:
        model = TradingAccount
        fields = '__all__'
        exclude = ['user', 'active', 'confirmed', 'status', 'action',]

        widgets = {
            'mt4_5': TextInput(attrs={'placeholder': 'Your mt4/mt5 id', 'required': 'true', }),
            'password': TextInput(attrs={'placeholder': 'Your mt4/mt5 password', 'required': 'true', }),
            'server': TextInput(attrs={'placeholder': 'Your mt4/mt5 server name', 'required': 'true', }),
        }