from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class DailyProfitHistory(models.Model):
    user = models.ForeignKey(User, related_name="daily_profit_history", on_delete=models.CASCADE)
    today_profit = models.DecimalField(max_digits=15,decimal_places=5, blank=True, null=True)
    today_percent = models.DecimalField(max_digits=15,decimal_places=2, blank=True, null=True)

    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class MonthlyProfitHistory(models.Model):
    user = models.ForeignKey(User, related_name="monthly_profit_history", on_delete=models.CASCADE)
    monthly_profit = models.DecimalField(max_digits=15,decimal_places=5, blank=True, null=True)
    monthly_percent = models.DecimalField(max_digits=15,decimal_places=2, blank=True, null=True)

    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class YearlyProfitHistory(models.Model):
    user = models.ForeignKey(User, related_name="yearly_profit_history", on_delete=models.CASCADE)
    yearly_profit = models.DecimalField(max_digits=15,decimal_places=5, blank=True, null=True)
    yearly_percent = models.DecimalField(max_digits=15,decimal_places=2, blank=True, null=True)

    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

