from django.urls import path
from .views import MyTokenObtainPairView, VendorListCreateAPIView, VendorRetrieveUpdateDestroyAPIView, PurchaseOrderCreateListAPIView, PurchaseOrderRetrieveUpdateDestroyAPIView, AcknowledgeAPIView, VendorPerformanceAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns= [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('vendor/', VendorListCreateAPIView.as_view(), name='vendor_list'),
    path('vendor/<int:vendor_id>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor_detail'),
    path('purchase_orders/', PurchaseOrderCreateListAPIView.as_view(), name='order_list'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='order_detail'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgeAPIView.as_view(),name='acknowledge_purchase_order'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
]
    