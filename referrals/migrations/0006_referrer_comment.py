# Generated by Django 4.2.3 on 2024-03-10 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0005_alter_referrer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='referrer',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
