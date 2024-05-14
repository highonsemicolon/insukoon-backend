# Generated by Django 4.2.13 on 2024-05-12 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_order_delete_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGatewayResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=20)),
                ('tracking_id', models.CharField(max_length=20)),
                ('bank_ref_no', models.CharField(blank=True, max_length=100, null=True)),
                ('order_status', models.CharField(max_length=20)),
                ('status_code', models.CharField(blank=True, max_length=20, null=True)),
                ('status_message', models.TextField()),
                ('currency', models.CharField(max_length=5)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('billing_name', models.CharField(max_length=100)),
                ('billing_email', models.EmailField(max_length=254)),
                ('payment_mode', models.CharField(blank=True, max_length=50, null=True)),
                ('card_name', models.CharField(blank=True, max_length=100, null=True)),
                ('billing_address', models.TextField(blank=True, null=True)),
                ('billing_city', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_state', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_zip', models.CharField(blank=True, max_length=20, null=True)),
                ('billing_country', models.CharField(blank=True, max_length=50, null=True)),
                ('billing_tel', models.CharField(blank=True, max_length=20, null=True)),
                ('delivery_name', models.CharField(blank=True, max_length=100, null=True)),
                ('delivery_address', models.TextField(blank=True, null=True)),
                ('delivery_city', models.CharField(blank=True, max_length=50, null=True)),
                ('delivery_state', models.CharField(blank=True, max_length=50, null=True)),
                ('delivery_zip', models.CharField(blank=True, max_length=20, null=True)),
                ('delivery_country', models.CharField(blank=True, max_length=50, null=True)),
                ('delivery_tel', models.CharField(blank=True, max_length=20, null=True)),
                ('vault', models.CharField(max_length=1)),
                ('offer_type', models.CharField(blank=True, max_length=20, null=True)),
                ('offer_code', models.CharField(blank=True, max_length=20, null=True)),
                ('discount_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('mer_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('eci_value', models.CharField(blank=True, max_length=20, null=True)),
                ('retry', models.CharField(max_length=1)),
                ('response_code', models.CharField(blank=True, max_length=20, null=True)),
                ('trans_date', models.DateTimeField()),
                ('bin_country', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]