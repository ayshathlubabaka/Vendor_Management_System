# Vendor_Management_System

# Overview

The Vendor Management System API is a Django-based application that allows users to manage vendors, track purchase orders and evaluate vendor performance metrics.

# Setup Instructions

1. Clone the repository: git clone https://github.com/ayshathlubabaka/Vendor_Management_System.git
2. Navigate to the project directory: cd vendor_management
3. Create a virtual environment: python3 -m venv fatenv
4. Activate the virtual environment:
   On Unix/macOS: source fatenv/bin/activate
   On Windows: fatenv\Scripts\activate
5. Install dependencies: pip install -r requirements.txt
6. Apply database migrations: python manage.py migrate
7. Create a superuser: python manage.py createsuperuser
7. Start the development server: python manage.py runserver

## Superuser Credentials

After creating a superuser using the `createsuperuser` command, you can use the provided username and password to obtain access and refresh tokens for authentication.

## Authorization

To authorize requests, include the obtained JWT token as a bearer token in the authorization header.

# API Endpoints

Token

POST /api/token/ : Obtain a JWT token by providing valid credentials
POST /api/token/refresh/ : Refresh the JWT token

Vendors

POST /api/vendors/: Create a new vendor.
GET /api/vendors/: List all vendors.
GET /api/vendors/{vendor_id}/: Retrieve details of a specific vendor.
PUT /api/vendors/{vendor_id}/: Update a vendor's details.
DELETE /api/vendors/{vendor_id}/: Delete a vendor.

Purchase Orders

POST /api/purchase_orders/: Create a new purchase order.
GET /api/purchase_orders/: List all purchase orders with optional vendor filtering.
GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
PUT /api/purchase_orders/{po_id}/: Update a purchase order.
DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

Acknowledge Purchase Order

POST /api/purchase_orders/{po_id}/acknowledge

Vendor Performance Metrics

GET /api/vendors/{vendor_id}/performance/: Retrieve performance metrics for a specific vendor.

# Test Suite

The project includes a comprehensive test suite to ensure the functionality and reliability of the API endpoints. To run the tests, execute the following command:
python manage.py test
