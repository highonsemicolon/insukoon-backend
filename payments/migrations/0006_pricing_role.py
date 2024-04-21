# Generated by Django 4.2.11 on 2024-04-21 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_remove_pricing_region_pricing_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing',
            name='role',
            field=models.CharField(choices=[('parent', 'Parent'), ('school', 'School')], default='Parent', max_length=10),
        ),
    ]
