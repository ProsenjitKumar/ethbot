# Generated by Django 4.0.2 on 2023-02-22 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0003_withdrawaldata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawaldata',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
