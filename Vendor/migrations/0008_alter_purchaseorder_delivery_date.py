# Generated by Django 4.0.5 on 2024-05-08 19:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0007_rename_vendor_historicalperformance_vendor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 8, 19, 17, 36, 134357, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
