from django.contrib import admin
from .models import Vendor, HistoricalPerformance, Purchase_Order
# Register your models here.

admin.site.register(Vendor)
admin.site.register(Purchase_Order)
admin.site.register(HistoricalPerformance)