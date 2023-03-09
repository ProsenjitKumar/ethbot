# Generated by Django 4.0.2 on 2023-02-22 05:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('withdraw', '0002_rename_withdrawalinfo_withdrawalinfos'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eth_address', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='withdraw_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]