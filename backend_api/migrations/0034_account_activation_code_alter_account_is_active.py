# Generated by Django 4.2.4 on 2023-11-09 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_api', '0033_alter_account_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='activation_code',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
