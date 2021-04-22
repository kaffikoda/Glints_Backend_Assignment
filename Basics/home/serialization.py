from rest_framework import serializers
from .models import CustomerDetails, RestaurantDetail, RestTimingss


class searialization_class(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'


class searialize_rest_detail(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDetail
        fields = '__all__'


class searialize_rest_timingss(serializers.ModelSerializer):
    class Meta:
        model = RestTimingss
        fields = ['restaurant_id']
        # fields = '__all__'

# class searialize_rest_timingss(serializers.ModelSerializer):
#     class Meta:
#         model = RestaurantDetail
        # fields = ['restaurant_id', 'restaurant_name']
        # fields = '__all__'
