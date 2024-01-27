import requests
import random
import json
import string

# base url:
base_url = "http://127.0.0.1:5000"

# Auth token:
# auth_token = "Bearer e4b8e1f593dc4a731a153c5ec8cc9b8bbb583ae964ce650a741113091b4e2ac6"

test_data = {}


# get random email id:
def generate_random_email():
    domain = "test.com"
    email_length = 10
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(email_length))
    email = random_string + "@" + domain
    test_data["email_id"] = email
    return email


# get random first name
def generate_random_first_name():
    first_name = ''.join(random.choices(string.ascii_lowercase, k=5))
    test_data["first_name"] = first_name
    return first_name


# get random last name
def generate_random_last_name():
    last_name = ''.join(random.choices(string.ascii_lowercase, k=5))
    test_data["last_name"] = last_name
    return last_name


# get random contact number
def generate_random_contact_number():
    contact_number = ''.join(random.choices(string.digits, k=10))
    test_data["contact_number"] = contact_number
    return contact_number


# GET Request
def get_request():
    url = base_url + "/users"
    print("get url: " + url)

    # headers = {"Authorization": auth_token}
    response = requests.get(url)

    # Status code validation
    assert response.status_code == 200

    json_data = response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json GET response body: ", json_str)

    print(".......GET USER IS DONE.......")
    print(".......=====================.......")


# POST Request
def post_request():
    post_url = base_url + "/users/create"
    print("post url: " + post_url)

    # headers = {"Authorization": auth_token}
    post_data = {
        "first_name": generate_random_first_name(),
        "last_name": generate_random_last_name(),
        "contact_number": generate_random_contact_number(),
        "email_id": generate_random_email()
    }

    try:
        post_response = requests.post(post_url, json=post_data)
        post_response.raise_for_status()  # Raise HTTPError for bad responses
        json_data = post_response.json()
        json_str = json.dumps(json_data, indent=4)
        print("json POST response body: ", json_str)
        id = json_data.get("id")
        print("id ===>", id)

        # Status code validation
        assert post_response.status_code == 200

        # Response key validation
        assert "id" in json_data.keys()
        assert "message" in json_data.keys()

        # Message/value validation
        assert json_data["message"] == "User created successfully", "User Not Created !!"

        # Verifying data get updated with get call (db-verification)
        get_url = base_url + "/users"
        get_response = requests.get(get_url)
        get_data = get_response.json()
        assert get_data["users"][-1]["first_name"] == test_data["first_name"]
        assert get_data["users"][-1]["last_name"] == test_data["last_name"]
        assert get_data["users"][-1]["contact_number"] == test_data["contact_number"]
        assert get_data["users"][-1]["email_id"] == test_data["email_id"]

        print(".......POST/Create USER IS DONE.......")
        print(".......=====================.......")
        return id

    except requests.exceptions.RequestException as e:
        print(f"Error in POST request: {e}")


# PUT Request
def put_request(id):
    # Picking the data to be updated using get call
    get_url = base_url + "/users"
    get_response = requests.get(get_url)
    get_data = get_response.json()
    data = get_data["users"][-1]

    put_url = base_url + f"/users-put/{id}"
    print("PUT url: " + put_url)

    # headers = {"Authorization": auth_token}
    test_data["email_id"] = generate_random_email()
    data.update({"email_id": test_data["email_id"]})

    put_response = requests.put(put_url, json=data)
    json_data = put_response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json PUT response body: ", json_str)

    # Status code validation
    assert put_response.status_code == 200

    # Response key validation
    assert "message" in json_data.keys()

    # Message/value validation
    assert json_data["message"] == "User updated successfully", "User Not Updated !!"

    # Validate that the email-id got updated using get call (db-validation)
    get_url = base_url + "/users"
    get_response = requests.get(get_url)
    json_get_data = get_response.json()
    assert json_get_data["users"][-1]["email_id"] == test_data["email_id"]

    print(".......PUT/Update USER IS DONE.......")
    print(".......=====================.......")


# PATCH Request
def patch_request(id):
    # Picking the data to be updated using get call
    get_url = base_url + "/users"
    get_response = requests.get(get_url)
    get_data = get_response.json()
    data = get_data["users"][-1]

    # Updating only the email_id for demonstration purposes
    updated_email = generate_random_email()
    data_to_patch = {"email_id": updated_email}

    patch_url = base_url + f"/users-patch/{id}"
    print("PATCH url: " + patch_url)

    # Sending PATCH request
    patch_response = requests.patch(patch_url, json=data_to_patch)
    json_data = patch_response.json()
    json_str = json.dumps(json_data, indent=4)
    print("json PATCH response body: ", json_str)

    # Status code validation
    assert patch_response.status_code == 200

    # Response key validation
    assert "message" in json_data.keys()

    # Message/value validation
    assert json_data["message"] == "Email ID updated successfully", "Emai-id Not Updated !!"

    # Validate that the email-id got updated using get call (db-validation)
    get_url = base_url + "/users"
    get_response = requests.get(get_url)
    json_get_data = get_response.json()
    assert json_get_data["users"][-1]["email_id"] == updated_email

    print(".......PATCH/Update USER IS DONE.......")
    print(".......=====================.......")


# DELETE Request
def delete_request(id):
    del_url = base_url + f"/users/delete/{id}"
    print("DELETE url: " + del_url)

    # headers = {"Authorization": auth_token}
    del_response = requests.delete(del_url)

    # Status code validation
    assert del_response.status_code == 200

    json_data = del_response.json()

    # Key validation
    assert "message" in json_data.keys()

    # Message/value validation
    assert json_data["message"] == "User deleted successfully", "User Not Deleted !!"

    print(".......DELETE USER IS DONE.......")
    print(".......=====================.......")


# Call the functions
get_request()
id = post_request()
put_request(id)
patch_request(id)
delete_request(id)

