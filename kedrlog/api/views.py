from api.serializers import PriceSerializer, RateSerializer
from core.models import Price, Rate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class RateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'max_guest': ['gte', 'lte', 'exact', 'gt', 'lt', ],
        'house': ['exact', ]
    }


class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'price_rates': ['exact', ],
    }
