# Generated by Django 4.0.2 on 2023-02-20 10:20

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
            name='YearlyProfitHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yearly_profit', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('yearly_percent', models.PositiveSmallIntegerField(blank=True, max_length=10, null=True)),
                ('active', models.BooleanField(default=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yearly_profit_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyProfitHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_profit', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('monthly_percent', models.PositiveSmallIntegerField(blank=True, max_length=10, null=True)),
                ('active', models.BooleanField(default=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_profit_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyProfitHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('today_profit', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('today_percent', models.PositiveSmallIntegerField(blank=True, max_length=10, null=True)),
                ('active', models.BooleanField(default=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_profit_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
