from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Vendor, HistoricalPerformance
from datetime import datetime



class VendorAPITest(APITestCase):
    def setUp(self):
        self.vendor_data = {
            'name': 'GHI Corporation',
            'contact_details': '121-456-7890',
            'address': 'XYZ Mainn St, City, Country',
            'vendor_code': 'VENDOR003',
            'on_time_delivery_rate': '93.5',
            'quality_rating_avg': '6.5',
            'average_response_time': '2.5',
            'fulfillment_rate': '91.0',
        }
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_vendor_crud_operations(self):
        # Create Vendor
        url = '/api/vendor/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']
        self.assertTrue(Vendor.objects.filter(id=vendor_id).exists())

        # Retrieve Vendor
        existing_vendor = Vendor.objects.get(id=vendor_id)
        url = f'/api/vendor/{existing_vendor.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update Vendor
        updated_data = {
            'name': 'GHI Corporation',
            'contact_details': '121-454-7870',
            'address': 'XYZ Mainn St, City, Country',
            'vendor_code': 'VENDOR003',
            'on_time_delivery_rate': '93.5',
            'quality_rating_avg': '6.5',
            'average_response_time': '15',
            'fulfillment_rate': '91.0',
        }
        url = f'/api/vendor/{existing_vendor.id}/'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        existing_vendor.refresh_from_db()
        self.assertEqual(existing_vendor.name, updated_data['name'])

        # Delete Vendor
        url = f'/api/vendor/{existing_vendor.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(id=existing_vendor.id).exists())

class VendorPurchaseOrderAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_create_and_retrieve_purchase_order(self):
        # Create a vendor
        vendor_data = {
            'name': 'GHI Corporation',
            'contact_details': '121-456-7890',
            'address': 'XYZ Mainn St, City, Country',
            'vendor_code': 'VENDOR003',
            'on_time_delivery_rate': 93.5,
            'quality_rating_avg': 6.5,
            'average_response_time': 2.5,
            'fulfillment_rate': 91.0,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/vendor/', vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vendor_id = response.data['id']

        # Create a purchase order
        purchase_order_data = {
            "po_number": "PO123456",
            "vendor": vendor_id,
            "order_date": "2024-05-10T08:00:00Z",
            "delivery_date": "2024-05-20T08:00:00Z",
            "items": [
                {
                    "name": "Item 1",
                    "description": "Description of Item 1",
                    "price": 10.50,
                    "quantity": 2
                },
                {
                    "name": "Item 2",
                    "description": "Description of Item 2",
                    "price": 15.75,
                    "quantity": 1
                }
            ],
            "quantity": 3,
            "status": "pending",
            "quality_rating": 5.5,
            "issue_date": "2024-05-10T08:00:00Z",
        }
        response = self.client.post('/api/purchase_orders/', purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        purchase_order_id = response.data['id']

        # Retrieve the created purchase order
        response = self.client.get(f'/api/purchase_orders/{purchase_order_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(f'/api/purchase_orders/{purchase_order_id}/acknowledge/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        # Update the purchase order
        updated_purchase_order_data = {
            "po_number": "PO123456",
            "vendor": vendor_id,
            "order_date": "2024-05-10T08:00:00Z",
            "delivery_date": "2024-05-20T08:00:00Z",
            "items": [
                {
                    "name": "Item 1",
                    "description": "Description of Item 1",
                    "price": 10.50,
                    "quantity": 2
                },
                {
                    "name": "Item 2",
                    "description": "Description of Item 2",
                    "price": 15.75,
                    "quantity": 1
                }
            ],
            "quantity": 3,
            "status": "completed",
            "quality_rating": 5.5,
            "issue_date": "2024-05-10T08:00:00Z",
        }
        response = self.client.put(f'/api/purchase_orders/{purchase_order_id}/', updated_purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete the purchase order
        response = self.client.delete(f'/api/purchase_orders/{purchase_order_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

