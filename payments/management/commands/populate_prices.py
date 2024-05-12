from django.core.management.base import BaseCommand

from payments.models import Pricing


class Command(BaseCommand):
    help = 'Populate pricing table with initial values'

    def handle(self, *args, **kwargs):

        # Clear existing pricing data
        Pricing.objects.all().delete()

        prices = [
            {'role': 'parent', 'country': 'IN', 'plan': 'quarterly', 'currency': 'INR', 'price': 1500},
            {'role': 'parent', 'country': 'IN', 'plan': 'yearly', 'currency': 'INR', 'price': 4800},
            {'role': 'school', 'country': 'IN', 'plan': 'quarterly', 'currency': 'INR', 'price': 1500},
            {'role': 'school', 'country': 'IN', 'plan': 'yearly', 'currency': 'INR', 'price': 4800},

            # {'role': 'parent', 'country': 'US', 'plan': 'quarterly', 'currency': 'USD', 'price': 150},
            # {'role': 'parent', 'country': 'US', 'plan': 'yearly', 'currency': 'USD', 'price': 480},
            # {'role': 'school', 'country': 'US', 'plan': 'quarterly', 'currency': 'USD', 'price': 140},
            # {'role': 'school', 'country': 'US', 'plan': 'yearly', 'currency': 'USD', 'price': 460},
        ]

        # Populate the PricingTable model
        for price_data in prices:
            Pricing.objects.create(
                role=price_data['role'],
                plan=price_data['plan'],
                price=price_data['price'],
                currency=price_data['currency'],
                country=price_data['country'],
            )

        self.stdout.write(self.style.SUCCESS('Pricing table populated successfully!'))
