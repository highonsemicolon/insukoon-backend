# Generated by Django 4.2.13 on 2024-05-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_provisionalorder_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentgatewayresponse',
            name='billing_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='paymentgatewayresponse',
            name='billing_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
