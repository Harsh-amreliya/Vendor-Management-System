Vendor Management System API <br>
Overview <br>
This Django REST API provides endpoints for managing vendors, purchase orders, and historical performance metrics. The API also includes token-based authentication to generate an authentication token for the admin user. <br>

Step 1: Clone the repository to your local machine: <br>
git clone https://github.com/your/repository.git <br>

Step 2: Install dependencies: <br>
pip install -r requirements.txt <br>

Step 3: Migrate the database: <br>
py manage.py makemigrations <br>
py manage.py migrate <br>

Step 4: Run the development server: <br>
python manage.py runserver <br>

Admin's Credentials for Dashboard are: <br>
Username: admin <br>
Password:123 <br>

API's of the system.. <br>
First of all Generate Admin Token Endpoint <br>

GET /generate-admin-token/: Generate an authentication token for the admin user. <br>
The above API will create Authentication Token for the user(ADMIN) <br>
There after use that Authentication Token in Header While Using API's else it will not show data. <br>

Vendor Endpoints <br>
GET /vendors/: Retrieve a list of all vendors. <br>
POST /vendors/: Create a new vendor. <br>
GET /vendors/<vendor_id>/: Retrieve details of a specific vendor. <br>
PUT /vendors/<vendor_id>/: Update details of a specific vendor. <br>
DELETE /vendors/<vendor_id>/: Delete a specific vendor. <br>

Purchase Order Endpoints <br>
GET /purchase_orders/: Retrieve a list of all purchase orders. <br>
POST /purchase_orders/: Create a new purchase order. <br>
GET /purchase_orders/<purchase_id>/: Retrieve details of a specific purchase order. <br>
PUT /purchase_orders/<purchase_id>/: Update details of a specific purchase order. <br>
DELETE /purchase_orders/<purchase_id>/: Delete a specific purchase order. <br>

Historical Performance Endpoints <br>
GET /<vendor_id>/performance: Retrieve historical performance metrics for a specific vendor. <br>

Acknowledge Purchase Order Endpoint <br>
POST /<po_id>/acknowledge: Acknowledge a purchase order by providing its ID. <br>
