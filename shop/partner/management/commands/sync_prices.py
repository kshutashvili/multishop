from django.core.management.base import BaseCommand, CommandError
from shop.partner.models import StockRecord
import requests
import csv


PRICES_URL = "http://up.artkamin.com.ua/EXPORT.csv"


class Command(BaseCommand):
    help = "Synchronize prices with server file"

    def handle(self, *args, **options):

        # open price data
        try:
            price_source = requests.get(PRICES_URL, stream=True).iter_lines()
            # skip headers row
            next(price_source, "")
            prices = csv.reader(price_source)
        except Exception as e:
            raise CommandError(str(e))

        # map price data to Python data types
        prices_map = (
            (
                price_row[0],
                float(price_row[1]),
                float(price_row[2])
            )
            for price_row in prices if price_row
        )

        # remove price updated flag from table
        StockRecord.objects.all().update(price_updated=False)

        for price in prices_map:
            try:
                stock_record = StockRecord.objects.get(
                    partner_sku=price[0]
                )
            except StockRecord.DoesNotExist:
                continue  # skip to next price
            else:
                # calculate prices
                price_price = price[1]
                price_discount = price[2]

                if price_price > price_discount:
                    price_new = price_discount
                    price_old = price_price
                elif price_price == price_discount:
                    price_new = price_price
                    price_old = None
                else:
                    price_new = price_price
                    price_old = price_discount

                stock_record.price_excl_tax = price_new
                stock_record.price_retail = price_new
                stock_record.previous_price = price_old
                stock_record.price_updated = True

                stock_record.save()

        # remove stock of products that are not in server file
        StockRecord.objects.filter(price_updated=False)\
            .update(num_in_stock=None)

        self.stdout.write("Finished prices update...")
