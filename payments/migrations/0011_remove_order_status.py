# Generated by Django 4.2.13 on 2024-05-11 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_remove_transaction_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
    ]