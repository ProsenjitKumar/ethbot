# Generated by Django 4.0.2 on 2023-02-15 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_deposited', models.DecimalField(decimal_places=2, max_digits=15)),
                ('transaction_id', models.CharField(blank=True, max_length=450, null=True)),
                ('active', models.BooleanField(default=False)),
                ('confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]