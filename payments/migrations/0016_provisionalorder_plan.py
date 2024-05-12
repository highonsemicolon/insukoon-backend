# Generated by Django 4.2.13 on 2024-05-12 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0015_paymentgatewayresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='provisionalorder',
            name='plan',
            field=models.CharField(choices=[('INR', 'Indian Rupees'), ('USD', 'US Dollars')], default='yearly', max_length=8),
        ),
    ]
