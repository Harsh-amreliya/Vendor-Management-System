
from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('vendors/',VendorList.as_view()),
    path('vendors/<int:vendor_id>',VendorDetail.as_view()),
    path('purchase_orders/',PurchaseOrderView.as_view()),
    path('purchase_orders/<int:purchase_id>',PurchaseOrderDetail.as_view()),
    path('<int:vendor_id>/performance',views.HistoricalDetails),
    path('<int:po_id>/acknowledge',views.acknowledge_purchase_order),
    path('generate-admin-token/', GenerateAdminToken.as_view()),

   
]
