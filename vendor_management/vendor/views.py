from django.http import Http404

from rest_framework import status,generics
from rest_framework.response import Response
from .models import Vendor,Purchase_Order, HistoricalPerformance
from .serializers import VendorSerializer, OrderSerializer, PerfomanceSerializer


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'

    def put(self, request, *args, **kwargs):
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
        try:
            vendor = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PurchaseOrderCreateListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Purchase_Order.objects.all()
        vendor_id = self.request.query_params.get('vendor')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'po_id'

    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor')
        if vendor_id:
            queryset = Purchase_Order.objects.filter(vendor_id=vendor_id)
        else:
            queryset = Purchase_Order.objects.all()
        return queryset

    def put(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(purchase_order, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        try:
            purchase_order = self.get_object()
        except Http404:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)