import decimal

from django.db import models
from django.contrib.auth.models import User


class WithdrawalInfos(models.Model):
    user = models.OneToOneField(User, related_name="withdraw_info", on_delete=models.CASCADE)
    eth_address = models.CharField(max_length=250, blank=False, null=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.eth_address}"


class WithdrawalData(models.Model):
    user = models.OneToOneField(User, related_name="withdraw_data", on_delete=models.CASCADE)
    eth_address = models.CharField(max_length=250, blank=False, null=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.eth_address}"


class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, related_name="withdraw_request", on_delete=models.CASCADE)
    withdraw_amount = models.DecimalField(max_digits=15, decimal_places=5)
    eth_address = models.CharField(max_length=250, blank=False, null=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.withdraw_amount}"

    def update_amount(self, withdraw_amount):
        self.withdraw_amount = decimal.Decimal(withdraw_amount)
        self.save()
