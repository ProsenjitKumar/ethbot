from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(DailyProfitHistory)
admin.site.register(MonthlyProfitHistory)
admin.site.register(YearlyProfitHistory)
