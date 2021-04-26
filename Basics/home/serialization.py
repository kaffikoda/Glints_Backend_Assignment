from rest_framework import serializers
from .models import RestaurantDetail, PurchaseHistory


class searialize_restaurant_detail(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDetail
        fields = ['restaurant_name']
        # fields = '__all__'


class serializing(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        # fields = ['restaurant_name']
        fields = '__all__'
