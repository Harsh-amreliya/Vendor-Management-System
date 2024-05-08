from django.db import models
from datetime import timedelta
from django.utils import timezone
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Vendor(models.Model):
    name=models.CharField(max_length=25)
    contact_details=models.IntegerField()
    address=models.TextField(max_length=100)
    vendor_code=models.CharField(max_length=5,unique=True)
    on_time_delivery_rate=models.FloatField(default=0)
    quality_rating_avg=models.FloatField(default=0)
    average_response_time=models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.vendor_code:  
            self.vendor_code = str(uuid.uuid4())[:5].upper()  # Generates a random 5-character code
        super().save(*args, **kwargs) 

class PurchaseOrder(models.Model):
    pending='Pending'
    cancelled='Cancelled'
    completed='Completed'
    statusoption=((pending,pending),(cancelled,cancelled),(completed,completed))
    

    po_number=models.CharField(max_length=5,unique=True)
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    delivery_date=models.DateTimeField()
    items=models.JSONField()
    quantity=models.IntegerField()
    status=models.CharField(max_length=15,default=pending,choices=statusoption)
    quality_rating=models.FloatField(blank=True,null=True,validators=[MaxValueValidator(5.0),MinValueValidator(0.0)])
    issue_date=models.DateTimeField(auto_now_add=True)
    acknowledgement_date=models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            # Generating a unique PO number using UUID
            self.po_number = str(uuid.uuid4())[:5].upper()
        if not self.delivery_date:  # If delivery_date is not provided, set it to 2 days from the current date
            self.delivery_date = timezone.now() + timedelta(days=2)
        super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate=models.FloatField(default=0)
    quality_rating_avg=models.FloatField(default=0)
    average_response_time=models.FloatField(default=0)
    fulfillment_rate=models.FloatField(default=0)

    
from .views import update_vendor_metrics
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics_on_purchase_order_save(sender, instance, **kwargs):
    if instance.status == 'Completed':
        vendor = instance.vendor
        print("This is Update_Vendor_Metrics Signal")
        update_vendor_metrics(vendor)