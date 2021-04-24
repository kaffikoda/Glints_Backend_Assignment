from rest_framework import serializers
from .models import CustomerDetails, RestaurantDetail, RestTimingss, MenuDetails


class searialization_class(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'


class searialize_rest_detail(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDetail
        fields = ['restaurant_name']
        # fields = '__all__'


class searialize_rest_timingss(serializers.ModelSerializer):
    class Meta:
        model = RestTimingss
        fields = ['restaurant_id']
        # fields = '__all__'

class searialize_menu_details(serializers.ModelSerializer):
    class Meta:
        model = MenuDetails
        fields = '__all__'
        # fields = ['restaurant_id']


# class ser_class_det(serializers.ModelSerializer):
#     class Meta:
#         model = Class

# class searialize_rest_timingss(serializers.ModelSerializer):
#     class Meta:
#         model = RestaurantDetail
        # fields = ['restaurant_id', 'restaurant_name']
        # fields = '__all__'
