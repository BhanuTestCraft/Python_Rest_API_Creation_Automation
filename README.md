# Flask REST API and Automation

This repository contains a Flask REST API created to manage user data, connected to a local PostgreSQL database (`restapi_db`).
Additionally, there is an automation script in the `AccessRestApi` folder (`RequestApi`) that interacts with the REST API using the `requests` module.

## Flask REST API (CreateRestApi)

### Installation and Setup

1. Clone the repository: git clone <repository_url>
2. Install required dependencies: pip install -r requirements.txt
3. Set up the PostgreSQL database (restapi_db) with the users tables.
4. Run the Flask app: python3 flask_api.py

API Endpoints
1. GET /users: Retrieve a list of all users.
2. POST /users/create: Create a new user.
3. PUT /users-put/{id}: Update user details.
4. PATCH /users-patch/{id}: Partially update user details.
5. DELETE /users/delete/{id}: Delete a user.   

Automation Script (AccessRestApi/RequestApi)
1. Navigate to the AccessRestApi folder: cd AccessRestApi
2. Update the base URL in the script (request_api.py) to match your Flask API endpoint.

Automated Requests
1. GET Request: Retrieve a list of all users.
2. POST Request: Create a new user.
3. PUT Request: Update user details.
4. PATCH Request: Partially update user details.
5. DELETE Request: Delete a user.

Additional Notes
1. Feel free to customize the Flask app and automation script based on your project requirements.
2. Make sure the Flask app is running before executing automated requests.
   

