from django.db import models


# Create your models here.
class CustomerDetails(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    cash_balance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_details'

    # def __str__(self):
    #     return self.customer_name


class RestaurantDetail(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=255)
    cash_balance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurant_detail'


class RestTimingss(models.Model):
    restaurant = models.ForeignKey('RestaurantDetail', models.DO_NOTHING)
    day_num = models.IntegerField()
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rest_timingss'


class MenuDetails(models.Model):
    menu_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey('RestaurantDetail', models.DO_NOTHING)
    dish_name = models.CharField(max_length=1000, blank=True, null=True)
    menu_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_details'


class PurchaseHistory(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomerDetails, models.DO_NOTHING)
    dish_name = models.CharField(max_length=1000, blank=True, null=True)
    restaurant_name = models.CharField(max_length=255, blank=True, null=True)
    transaction_amount = models.FloatField(blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purchase_history'
