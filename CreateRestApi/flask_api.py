from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Replace these values with your Postgresql connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "restapi_db"
DB_USER = "postgres"
DB_PASSWORD = "Test@123"


# Function to establish a connection to the Postgresql database
def create_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# API endpoint to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    # Create a database connection
    connection = create_connection()
    cursor = connection.cursor()

    # Execute the SELECT query to fetch all users from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # close the cursor and connection
    cursor.close()
    connection.close()

    # Convert the fetched users into a list of dictionaries
    user_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'contact_number': user[3],
            'email_id': user[4]
        }
        user_list.append(user_dict)

    # Return a JSON response containing the list of users
    return jsonify({'users': user_list})


# API endpoint to create a new user
@app.route('/users/create', methods=['POST'])
def create_user():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract user details from the data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_number = data.get('contact_number')
    email_id = data.get('email_id')

    # Create a database connection
    connection = create_connection()
    cursor = connection.cursor()

    # Execute the INSERT query to add a new user to the database
    cursor.execute("INSERT INTO users (first_name, last_name, contact_number, email_id) VALUES (%s, %s, %s, "
                   "%s) RETURNING id",
                   (first_name, last_name, contact_number, email_id))
    new_user_id = cursor.fetchone()[0]

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User created successfully', 'id': new_user_id})


# API endpoint to update user data
@app.route('/users-put/<int:id>', methods=['PUT'])
def update_user(id):
    # Get the JSON data from the request
    data = request.get_json()

    # Extract user details from the data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_number = data.get('contact_number')
    email_id = data.get('email_id')

    # Create a database connection
    connection = create_connection()
    cursor = connection.cursor()

    # Execute the UPDATE query to modify user details based on the provided ID
    cursor.execute("UPDATE users SET first_name = %s, last_name = %s, contact_number = %s, email_id = %s WHERE id = %s",
                   (first_name, last_name, contact_number, email_id, id))

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User updated successfully'})


# API endpoint to partially update user data
@app.route('/users-patch/<int:id>', methods=['PATCH'])
def patch_user(id):
    data = request.get_json()

    # Check if 'email_id' is present in the request payload
    if 'email_id' in data and data['email_id'] is not None:
        new_email_id = data['email_id']

        # Create a database connection
        connection = create_connection()
        cursor = connection.cursor()

        # Execute the update query for 'email_id'
        cursor.execute("UPDATE users SET email_id = %s WHERE id = %s", (new_email_id, id))

        # Commit the changes and close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Email ID updated successfully'})
    else:
        return jsonify({'message': 'No valid email_id provided for update'})


# API endpoint to delete a user
@app.route('/users/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    # Create a database connection
    connection = create_connection()
    cursor = connection.cursor()

    # Execute the DELETE query to remove the user with the specified ID
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'message': 'User deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
