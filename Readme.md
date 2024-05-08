Vendor Management System API
Overview
This Django REST API provides endpoints for managing vendors, purchase orders, and historical performance metrics. The API also includes token-based authentication to generate an authentication token for the admin user.

Step 1: Clone the repository to your local machine:
git clone https://github.com/your/repository.git

Step 2: Install dependencies:
pip install -r requirements.txt

Step 3: Migrate the database:
py manage.py makemigrations
py manage.py migrate

Step 4: Run the development server:
python manage.py runserver

Admin's Credentials for Dashboard are:
Username: admin
Password:123

API's of the system..
First of all Generate Admin Token Endpoint

GET /generate-admin-token/: Generate an authentication token for the admin user.
The above API will create Authentication Token for the user(ADMIN)
There after use that Authentication Token in Header While Using API's else it will not show data.

Vendor Endpoints
GET /vendors/: Retrieve a list of all vendors.
POST /vendors/: Create a new vendor.
GET /vendors/<vendor_id>/: Retrieve details of a specific vendor.
PUT /vendors/<vendor_id>/: Update details of a specific vendor.
DELETE /vendors/<vendor_id>/: Delete a specific vendor.

Purchase Order Endpoints
GET /purchase_orders/: Retrieve a list of all purchase orders.
POST /purchase_orders/: Create a new purchase order.
GET /purchase_orders/<purchase_id>/: Retrieve details of a specific purchase order.
PUT /purchase_orders/<purchase_id>/: Update details of a specific purchase order.
DELETE /purchase_orders/<purchase_id>/: Delete a specific purchase order.

Historical Performance Endpoints
GET /<vendor_id>/performance: Retrieve historical performance metrics for a specific vendor.

Acknowledge Purchase Order Endpoint
POST /<po_id>/acknowledge: Acknowledge a purchase order by providing its ID.
