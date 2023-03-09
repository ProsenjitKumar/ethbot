from django.urls import re_path
from .views import *

urlpatterns = [
    re_path('daily-profit-history/', daily_profit_history, name='daily-profit-history'),
    re_path('withdraw-history/', withdraw_history, name='withdraw-history'),
    re_path('deposit-history/', deposit_history, name='deposit-history'),
]