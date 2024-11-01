from core.models import Price, Rate
from rest_framework import serializers


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['id', 'price', ]


class RateSerializer(serializers.ModelSerializer):
    price = PriceSerializer(many=True)
    min_price = serializers.SerializerMethodField()

    @staticmethod
    def get_min_price(obj):
        return obj.get_min_price()

    class Meta:
        model = Rate
        fields = '__all__'
