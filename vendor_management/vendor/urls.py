from django.urls import path
from .views import VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView, PurchaseOrderCreateListAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView

urlpatterns= [
    path('vendor/', VendorListCreateAPIView.as_view(), name='vendor_list'),
    path('vendor/<int:vendor_id>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor_detail'),
    path('purchase_orders/', PurchaseOrderCreateListAPIView.as_view(), name='order_list'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='order_detail')
]
    