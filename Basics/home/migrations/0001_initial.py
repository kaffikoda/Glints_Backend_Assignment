# Generated by Django 3.1.7 on 2021-04-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('customer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('cash_balance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'customer_details',
                'managed': False,
            },
        ),
    ]
