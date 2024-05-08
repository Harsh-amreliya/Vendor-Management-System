from rest_framework import serializers
from .models import *


class VendorSerializer(serializers.ModelSerializer):
    vendor_code = serializers.CharField(read_only=True)
    average_response_time_hours = serializers.SerializerMethodField()
    class Meta:
        model =Vendor
        fields='__all__'
    def get_average_response_time_hours(self, obj):
        # Convert average_response_time from seconds to hours
        hours = obj.average_response_time // 3600
        minutes = (obj.average_response_time % 3600) // 60
        return '{} hrs {} mins'.format(int(hours), int(minutes))
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    
    po_number=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    order_date=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    delivery_date=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    issue_date=serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model=PurchaseOrder
        fields=['id','po_number','vendor','items','quantity','order_date','status','issue_date','delivery_date']

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields='__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.name')
    average_response_time = serializers.SerializerMethodField()
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model=HistoricalPerformance
        fields = '__all__'

    def get_average_response_time(self, obj):
        # Converting average_response_time (in seconds) to a human-readable format
        seconds = obj.average_response_time
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60
        return '{:.0f} hr {:.0f} min'.format(hours, minutes)