from django.shortcuts import render
from .models import DailyProfitHistory
from mainapp.models import Customer
from deposit.models import DepositRequest
from withdraw.models import WithdrawalRequest
from deposit.models import DepositRequest

# Create your views here.


def daily_profit_history(request):
    object_list = DailyProfitHistory.objects.filter(user=request.user)
    print(object_list)
    context = {
        'object_list': object_list
    }

    return render(request, 'history/history.html', context)


def withdraw_history(request):
    object_list = WithdrawalRequest.objects.filter(user=request.user)
    print(object_list)
    context = {
        'object_list': object_list
    }

    return render(request, 'history/withdraw-history.html', context)


def deposit_history(request):
    object_list = DepositRequest.objects.filter(user=request.user)
    print(object_list)
    context = {
        'object_list': object_list
    }

    return render(request, 'history/deposit-history.html', context)
