from django.http import Http404
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Vendor, Purchase_Order, HistoricalPerformance
from .serializers import VendorSerializer, OrderSerializer, PerfomanceSerializer
from .signals import purchase_order_modified


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer.
    """    
    @classmethod
    def get_token(cls, user):
        """
        Return token for the given user.
        """
        token = super().get_token(user)
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view.
    """
    serializer_class = MyTokenObtainPairSerializer


class VendorListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating vendors.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting vendors.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'

    def put(self, request, *args, **kwargs):
        """
        Update an existing vendor.
        """
        try:
            vendor = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        """
        Delete an existing vendor.
        """
        try:
            vendor = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderCreateListAPIView(generics.ListCreateAPIView):
    """
    API view for creating and listing purchase orders.
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Get queryset of purchase orders.
        """
        queryset = Purchase_Order.objects.all()
        vendor_id = self.request.query_params.get('vendor')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset


class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting purchase orders.
    """
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'po_id'

    def get_queryset(self):
        """
        Get queryset of purchase orders.
        """
        vendor_id = self.request.query_params.get('vendor')
        if vendor_id:
            queryset = Purchase_Order.objects.filter(vendor_id=vendor_id)
        else:
            queryset = Purchase_Order.objects.all()
        return queryset

    def put(self, request, *args, **kwargs):
        """
        Update an existing purchase order.
        """
        try:
            purchase_order = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            purchase_order_modified.send(sender=self.__class__, instance=purchase_order)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, *args, **kwargs):
        """
        Delete an existing purchase order.
        """
        try:
            purchase_order = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcknowledgeAPIView(generics.UpdateAPIView):
    """
    API view for acknowledging a purchase order.
    """
    serializer_class = OrderSerializer

    def update(self, request, po_id, format=None):
        """
        Update acknowledgment date of a purchase order.
        """
        try:
            purchase_order = get_object_or_404(Purchase_Order, id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            purchase_order_modified.send(sender=self.__class__, instance=purchase_order)
            return Response({"message": "Acknowledgment date updated successfully"}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


class VendorPerformanceAPIView(APIView):
    """
    API view for retrieving vendor performance.
    """
    serializer_class = PerfomanceSerializer

    def get(self, request, vendor_id, format=None):
        """
        Get historical performance data for a vendor.
        """
        vendor = get_object_or_404(Vendor, id=vendor_id)
        historical_performance = HistoricalPerformance.objects.filter(vendor=vendor)
        serializer = self.serializer_class(historical_performance, many=True)
        return Response(serializer.data)
        
        

    
        
