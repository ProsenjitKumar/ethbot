# Generated by Django 4.0.2 on 2023-03-08 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0015_alter_depositrequest_payment_method_tradingaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='depositrequest',
            name='in_usd',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
            preserve_default=False,
        ),
    ]
