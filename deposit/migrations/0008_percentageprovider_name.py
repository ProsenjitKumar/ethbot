# Generated by Django 4.0.2 on 2023-02-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deposit', '0007_percentageprovider'),
    ]

    operations = [
        migrations.AddField(
            model_name='percentageprovider',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
