# Generated by Django 4.2.3 on 2024-03-09 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0003_rename_user_id_referrer_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='Referred_user',
            new_name='referred_user',
        ),
    ]
