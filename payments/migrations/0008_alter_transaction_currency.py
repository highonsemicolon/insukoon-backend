# Generated by Django 4.2.11 on 2024-04-21 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_rename_duration_pricing_plan_pricing_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='currency',
            field=models.CharField(choices=[('INR', 'Indian Rupees'), ('USD', 'US Dollars')], default='INR', max_length=8),
        ),
    ]
