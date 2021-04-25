from rest_framework import serializers
from .models import RestaurantDetail


class searialize_restaurant_detail(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDetail
        fields = ['restaurant_name']
        # fields = '__all__'
