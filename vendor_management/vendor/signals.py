from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, Purchase_Order, HistoricalPerformance
from django.db.models import Avg, F
from django.db.models.signals import ModelSignal
from django.utils import timezone
from datetime import datetime

purchase_order_modified = ModelSignal()

@receiver(purchase_order_modified)
def update_vendor_performance(sender, instance, **kwargs):
    print('signal called')
    try:
        vendor = instance.vendor
        total_completed_orders = Purchase_Order.objects.filter(vendor=vendor,status__iexact='completed').count()

        if instance.status != instance._original_status:
            if instance.status == 'completed':
                actual_delivery_date = datetime.now()
                on_time_orders = Purchase_Order.objects.filter(vendor=vendor, status__iexact='completed', delivery_date__gte=actual_delivery_date).count()
                on_time_delivery_rate = (on_time_orders/total_completed_orders)*100 if total_completed_orders>0 else 0
                Vendor.objects.filter(id=vendor.id).update(on_time_delivery_rate=on_time_delivery_rate)
            
                if instance.quality_rating:
                    quality_rating_avg = Purchase_Order.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(average_quality_rating=Avg('quality_rating'))['average_quality_rating']
                    Vendor.objects.filter(id=vendor.id).update(quality_rating_avg=quality_rating_avg)

            fulfillment_rate = (total_completed_orders / Purchase_Order.objects.filter(vendor=vendor).count())*100 if total_completed_orders>0 else 0
            Vendor.objects.filter(id=vendor.id).update(fulfillment_rate=fulfillment_rate)

        if instance.acknowledgment_date and instance.acknowledgment_date != instance._original_acknowledgment_date:

            response_times =  Purchase_Order.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).exclude(acknowledgment_date__lte=F('issue_date')).annotate(response_time=F('acknowledgment_date')-F('issue_date'))
            average_response_time = response_times.aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
            Vendor.objects.filter(id=vendor.id).update(average_response_time=average_response_time.days)

        if instance.status != instance._original_status or instance.acknowledgment_date != instance._original_acknowledgment_date:

            historical_performance = HistoricalPerformance.objects.create(
                vendor=vendor,
                average_response_time=vendor.average_response_time,
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                fulfillment_rate=vendor.fulfillment_rate,
                date = timezone.now()
            )
            historical_performance.save()

    except Exception as e:
            print(f"Error occured during performane calculation: {e}")