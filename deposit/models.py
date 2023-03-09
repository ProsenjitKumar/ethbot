from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

COIN_SELECTED = (
    ('UPI Payment', 'UPI Payment'),
    ('Bkash', 'Bkash'),
    ('Nagad', 'Nagad'),
    ('Bitcoin', 'Bitcoin'),
    ('USDT', 'USDT'),
    ('Ethereum', 'Ethereum'),
    ('BUSD', 'BUSD'),
    ('Dogecoin', 'Dogecoin'),
    ('BNB', 'BNB'),
    ('Litecoin', 'Litecoin'),
    ('USDC', 'USDC'),
    ('SOL Solana', 'SOL Solana'),
    ('BNB', 'BNB'),
    ('MATIC Polygon', 'MATIC Polygon'),
    ('XRP Ripple', 'XRP Ripple'),
    ('ADA Cardano', 'ADA Cardano'),
)


class PaymentMethod(models.Model):
    currency_name = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="coin/logo/", null=True, blank=True)
    deposit_address = models.CharField(max_length=455, null=True, blank=True)
    qr_code_image = models.ImageField(upload_to="coin/qrcode/", null=True, blank=True)
    network = models.CharField(max_length=255, blank=True, null=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.currency_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.currency_name


class DepositRequest(models.Model):
    user = models.ForeignKey(User, related_name="deposit_request", on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=25, choices=COIN_SELECTED, null=True, blank=True)
    amount_deposited = models.DecimalField(max_digits=15,decimal_places=5)
    in_usd = models.DecimalField(max_digits=20,decimal_places=2)
    transaction_id = models.CharField(max_length=450, null=True, blank=True)
    wallet_number = models.CharField(max_length=50, blank=True, null=True)

    active = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.amount_deposited}"

    def update_active(self, active):
        self.active = active
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Bot(models.Model):
    BOT_SELECT = (
        ('1', '6 Months'),
        ('2', '12 Months'),
    )
    user = models.ForeignKey(User, related_name="bot", on_delete=models.CASCADE)
    selected_bot = models.CharField(max_length=200, choices=BOT_SELECT, null=False, blank=False)
    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Trading(models.Model):
    user = models.ForeignKey(User, related_name="trade", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=5, blank=False, null=False)
    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def update_active(self, active):
        self.active = active
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class TradingProfit(models.Model):
    user = models.ForeignKey(User, related_name="trading_profit", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=5, blank=False, null=False)
    percentage = models.DecimalField(max_digits=15, decimal_places=1, blank=False, null=False)
    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class TradingAccount(models.Model):
    user = models.ForeignKey(User, related_name="trade_account", on_delete=models.CASCADE)
    mt4_5 = models.CharField(max_length=450, null=True, blank=True)
    password = models.CharField(max_length=450, null=True, blank=True)
    server = models.CharField(max_length=450, null=True, blank=True)
    status = models.BooleanField(default=True)
    action = models.CharField(max_length=450, null=True, blank=True)

    active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username