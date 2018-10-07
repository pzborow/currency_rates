from django.db import models


class CurrencyRate(models.Model):
    base_currency = models.CharField(max_length=3, default='EUR')
    currency = models.CharField(max_length=3, db_index=True)
    # TODO Use FK to Currency table based on ISO 4217

    date = models.DateField()
    # Rate indicates how many currency can be bought by 1 base_currency
    # i.e. if base_currency is EUR and currency is PLN and rate is 4.0
    # it means that 1EUR buys 4.0 PLNs
    rate = models.DecimalField(max_digits=19, decimal_places=10)

    # TODO add source info, and created_at and updated_at field

    class Meta:
        unique_together = (("base_currency", "currency"),)

    def __str__(self):
        return u"1 %s=%s %s" % (self.base_currency, self.rate, self.currency)
