"""Django manage.py update_currency_rates command"""
import argparse  # noqa
import decimal
import logging
from datetime import datetime
from time import mktime

import feedparser

from django.core.management.base import BaseCommand

from currency_rates.models import CurrencyRate


logger = logging.getLogger('curency_rates')


class Command(BaseCommand):
    """Update currency rates.

    Example::
        $ ./manage.py update_currency_rates
    """

    @staticmethod
    def update_currency_model(base_currency, target_currency, exchange_rate, date):
        try:
            cr = CurrencyRate.objects.get(currency=target_currency)
            op = 'Updated'
        except CurrencyRate.DoesNotExist:
            cr = CurrencyRate(base_currency='EUR', currency=target_currency)
            op = 'Created'

        # TODO change to debug level
        logger.warning('{} currency {}-{} with exchange rate {} for {}'.format(op, base_currency, target_currency, exchange_rate, date))
        cr.rate = exchange_rate
        cr.date = date
        cr.save()

    @staticmethod
    def process_entry(entry):
        # use temporary without timezone field updated_parsed
        date_st = entry['updated_parsed']
        # date_str = feed['entries'][0]['updated'] doesn't work because of
        # ValueError: time data '2018-10-05T14:15:00+01:00' does not match format '%Y-%m-%dT%H:%M:%S%z'
        # this expect 2018-10-05T14:15:00+0100
        # date_str = feed['entries'][0]['updated']
        # parsed_date = timezone.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
        # TODO fixme
        date = datetime.fromtimestamp(mktime(date_st))
        target_currency = entry['cb_targetcurrency']
        # TODO this key looks like 'cb_exchangerate': '4.3045\nEUR', ensure if this is right field, if so, add validation
        exchange_rate = decimal.Decimal(entry['cb_exchangerate'].split('\n')[0])

        Command.update_currency_model('EUR', target_currency, exchange_rate, date)

    def process_feed(self, currency):
        # TODO move it do separated RSS currency rates client
        # Parse using https://marshmallow.readthedocs.io/en/3.0/

        # TODO move it to settings
        url = 'https://www.ecb.europa.eu/rss/fxref-{}.html'.format(currency)
        feed = feedparser.parse(url)

        # TODO ensure existance of 'entries' key
        # if no 'entries' or 'updated_parsed' then log an error
        newest_entry = max(feed['entries'], key=lambda entry: entry['updated_parsed'])
        self.process_entry(newest_entry)

    def handle(self, *args, **options):
        # TODO Interested currencies, get from settings or try to read all RSS sources from site
        currencies = ['pln', 'usd']
        for currency in currencies:
            self.process_feed(currency)
