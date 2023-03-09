from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(DepositRequest)
admin.site.register(Bot)
admin.site.register(Trading)
admin.site.register(TradingProfit)
admin.site.register(PaymentMethod)
admin.site.register(TradingAccount)
