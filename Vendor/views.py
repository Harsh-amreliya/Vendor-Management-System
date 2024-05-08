from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F, ExpressionWrapper, DateTimeField
from django.db.models import Avg
from .serializers import *
from .models import *
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import F, ExpressionWrapper, DateTimeField, Count, Avg, Sum
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status


# Create your views here.
class GenerateAdminToken(APIView):
    def get(self, request):
        try:
            admin_user = User.objects.get(username='admin')  # Assuming admin's username is 'admin'
            token, created = Token.objects.get_or_create(user=admin_user)
            if created:
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'token': token.key}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Admin user not found'}, status=status.HTTP_404_NOT_FOUND)
        
# Function to calculate and update vendor metrics

def update_vendor_metrics(vendor):

    # Completed orders
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='Completed')

    # Calculate on-time delivery count
    on_time_delivery_count = completed_orders.filter(delivery_date__lte=F('order_date')).count()

    # Calculate total completed orders
    total_completed_orders = completed_orders.count()

    # Calculate on-time delivery rate
    vendor.on_time_delivery_rate = (on_time_delivery_count / total_completed_orders) * 100 if total_completed_orders > 0 else 0
    # Calculating Quality Rating Average
    vendor.quality_rating_avg = completed_orders.aggregate(
        Avg('quality_rating'))['quality_rating__avg'] or 0
    
    # Calculating Average Response Time
    response_times = completed_orders.exclude(acknowledgement_date__isnull=True).values_list(
        'acknowledgement_date', flat=True)
    total_response_time = sum((timezone.now() - ack_date).total_seconds() for ack_date in response_times)
    avg_response_time = total_response_time / len(response_times) if response_times else 0
    vendor.average_response_time = avg_response_time
    
    # Calculating Fulfillment Rate
    successful_orders = completed_orders.filter(status='Completed')
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    vendor.fulfillment_rate = (successful_orders.count(
    ) / total_orders) * 100 if total_orders > 0 else 0
    
    vendor.save()
    
    vendordata={'vendor':vendor.pk,
        'date':timezone.now(),
        'on_time_delivery_rate':vendor.on_time_delivery_rate,
        'quality_rating_avg':vendor.quality_rating_avg,
        'average_response_time':vendor.average_response_time,
        'fulfillment_rate':vendor.fulfillment_rate}
    serialiser=HistoricalPerformanceSerializer(data=vendordata)
    if serialiser.is_valid():
        serialiser.save()
    else:
        print(serialiser.errors)

class VendorList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'message': 'Vendor Created Successfully', 'payload': serializer.data})
        return Response({'status': 403, 'message': 'Vendor Not Created', 'payload': serializer.errors})

    def get(self, request):
        try:
            vendor_details = Vendor.objects.all()
            serializer = VendorSerializer(vendor_details, many=True)
            if vendor_details:
                return Response({'status': 200, 'payload': serializer.data})
            else:
                return Response({'status': 200, 'Message': "No Vendors are Listed Yet"})
        except:
            return Response({'status': 200, 'message': 'No data found'})


class VendorDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id):
        try:
            vendor_details = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor_details)
            return Response({'status': 200, 'payload': serializer.data, 'message': 'Data found'})
        except:
            return Response({'status': 403, 'message': 'No data found'})

    def put(self, request, vendor_id):
        try:
            vendor_details = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor_details, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'message': 'Vendor Updated Successfully', 'payload': serializer.data})
            return Response({'status': 403, 'message': 'Vendor Not Updated', 'payload': serializer.errors})
        except:
            return Response({'status': 403, 'message': 'Please Enter Valid ID'})

    def delete(self, request, vendor_id):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        try:
            vendor_details = Vendor.objects.get(id=vendor_id)
            VendorName = vendor_details.name
            vendor_details.delete()
            return Response({'status': 200, 'message': f'Vendor Named {VendorName} Deleted Successfully'})
        except:
            return Response({'status': 403, 'message': 'Please Enter Valid ID'})


class PurchaseOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'message': 'Purchase Order Created Successfully', 'payload': serializer.data})
        return Response({'status': 403, 'message': 'Purchase Order Not Created', 'payload': serializer.errors})

    def get(self, request):
        try:
            purchase_details = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_details, many=True)
            if purchase_details:
                return Response({'status': 200, 'payload': serializer.data})
            else:
                return Response({'status': 200, 'Message': "No Orders have been Placed Yet"})
        except:
            return Response({'status': 403, 'message': 'No data found'})


class PurchaseOrderDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, purchase_id):
        try:
            purchase_details = PurchaseOrder.objects.get(id=purchase_id)
            serializer = PurchaseDetailSerializer(purchase_details)
            return Response({'status': 200, 'payload': serializer.data})
        except:
            return Response({'status': 403, 'message': 'No data found'})

    def put(self, request, purchase_id):
        try:
            purchase_details = PurchaseOrder.objects.get(id=purchase_id)
            serializer = PurchaseDetailSerializer(
                purchase_details, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'message': 'Purchase Order Updated Successfully', 'payload': serializer.data})
            return Response({'status': 403, 'message': 'Purchase Order Not Updated', 'payload': serializer.errors})
        except:
            return Response({'status': 403, 'message': 'Please Enter Valid Details'})

    def delete(self, request, purchase_id):
        try:
            purchase_details = PurchaseOrder.objects.get(id=purchase_id)
            purchase_details.delete()
            return Response({'status': 200, 'message': 'Purchase Order Deleted Successfully'})
        except:
            return Response({'status': 403, 'message': 'Please Enter Valid ID'})


@ api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def HistoricalDetails(request, vendor_id):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    try:
        vendor = HistoricalPerformance.objects.filter(vendor=vendor_id)
        
        serializer=HistoricalPerformanceSerializer(data=vendor,many=True)
        serializer.is_valid()
        if vendor:
            return Response({'status': 200, 'payload': serializer.data})
        else:
            return Response({'status': 200, 'message': 'No Record Found'})
    except:
        return Response({'status': 403, 'message': 'No data found / Invalid ID!!',})


@ api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_id)
        purchase_order.acknowledgement_date = timezone.now()
        purchase_order.save()
    except PurchaseOrder.DoesNotExist:
        return Response({'status': 403, 'message': 'Invalid Id!!'})

    # Trigger recalculation of average_response_time
    vendor = purchase_order.vendor
    # update_vendor_metrics(vendor)
    return Response({'status': 200, 'message': 'Acknowledge successfully'})
