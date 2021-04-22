from django.db import models


# Create your models here.
class CustomerDetails(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    cash_balance = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_details'

    def __str__(self):
        return self.customer_name
