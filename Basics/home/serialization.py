from rest_framework import serializers
from .models import CustomerDetails, RestaurantDetail, RestTimingss


class searialization_class(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'


class searialization_class1(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDetail
        fields = '__all__'


class searialization_class2(serializers.ModelSerializer):
    class Meta:
        model = RestTimingss
        fields = '__all__'
