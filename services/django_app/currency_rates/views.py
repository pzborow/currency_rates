from rest_framework import (
    generics,
    mixins,
)

from currency_rates.serializers import CurrencyRateSerializer
from currency_rates.models import CurrencyRate


class CurrencyRatesView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    A simple View for listing currency rates.
    """

    serializer_class = CurrencyRateSerializer
    queryset = CurrencyRate.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
