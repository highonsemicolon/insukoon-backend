# Generated by Django 4.2.11 on 2024-04-21 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_rename_transactions_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricing',
            name='region',
        ),
        migrations.AddField(
            model_name='pricing',
            name='currency',
            field=models.CharField(choices=[('INR', 'Indian Rupees'), ('USD', 'US Dollars')], default='INR', max_length=3),
        ),
        migrations.AlterField(
            model_name='pricing',
            name='duration',
            field=models.CharField(choices=[('quarterly', 'Quarterly'), ('yearly', 'Yearly')], default='quarterly', max_length=10),
        ),
    ]