# Generated by Django 4.0.2 on 2023-03-04 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0012_depositrequest_wallet_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositrequest',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('UPI', 'UPI'), ('Bkash', 'Bkash'), ('Nagad', 'Nagad'), ('Bitcoin', 'Bitcoin'), ('USDT', 'USDT'), ('Ethereum', 'Ethereum'), ('BUSD', 'BUSD'), ('Dogecoin', 'Dogecoin'), ('BNB', 'BNB'), ('Litecoin', 'Litecoin'), ('USDC', 'USDC'), ('SOL Solana', 'SOL Solana'), ('BNB', 'BNB'), ('MATIC Polygon', 'MATIC Polygon'), ('XRP Ripple', 'XRP Ripple'), ('ADA Cardano', 'ADA Cardano')], max_length=25, null=True),
        ),
    ]