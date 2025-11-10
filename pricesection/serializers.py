from rest_framework import serializers
from .models import PriceSection, BulletPoints

class BulletPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulletPoints
        fields = ['id', 'points']

class PriceSectionSerializer(serializers.ModelSerializer):
    bullet = BulletPointsSerializer(many=True, read_only=True)

    class Meta:
        model = PriceSection
        fields = ['id', 'title', 'price', 'validity', 'offer', 'bullet']


