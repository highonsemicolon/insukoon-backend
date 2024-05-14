# Generated by Django 4.2.13 on 2024-05-14 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_rename_email_verification_parentprofile_notification_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parentprofile',
            name='notification_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='parentprofile',
            name='notification_phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]