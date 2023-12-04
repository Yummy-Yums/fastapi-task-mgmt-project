from fastapi.testclient import TestClient
import json

from main import app

client = TestClient(app)

common_id = "36b4de54-839b-11ee-8410-572c151d32b7"


def test_home_page():
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == '"Welcome to Task Management System"'
    
    
def test_add_user_success():
    
    new_user_details = {
        
        "id": common_id,
        "username": "est-name",
        "email": "test-emal@yahoo.com",
        "password": "test-password"

    }
    
    response = client.post(
        "/user/add/",
        json=new_user_details
    )
    
    assert response.status_code == 201
    assert response.text == '"user created"'
    
def test_add_user_failure():
    
    new_user_details = {
        
        "id": common_id,
        "username": "test-name",
        "email": "test-email@yahoo.com",
        "password": ""

    }
    
    response = client.post(
        "/user/add/",
        json=new_user_details
    )
    
    assert response.status_code == 422
    assert response.text == '"action incomplete"'


update_details = {
        "id" : "0295af6a-8236-11ee-bc6e-53c43995db32",
        "user": {
            "username": "useremail",
            "email": "string@yahoo.com",
            "password": "string"
        }
    }
    
def test_update_user_details_success():
    
    response = client.patch(
        f"/user/update/?id={update_details['id']}",
        json=update_details['user']
    )
    
    print(response.content)
    
    assert response.status_code == 200
    assert response.text == '"user updated"'
    
def test_update_user_details_failure():
    
    failure_details = update_details
    
    del failure_details['id']
    
    response = client.patch(
        "/user/update/",
        json=failure_details['user']
    )
    
    assert response.status_code != 200
    
    
def test_update_user_detail_username_only_success():
    
    new_details = update_details
    
    del new_details['user']['email']
    del new_details['user']['password']
    
    response = client.patch(
        f"/user/update/?id={new_details['id']}",
        json=new_details['user']
    )
    
    assert response.status_code == 200
    assert response.text == '"user updated"'
    
def test_update_user_detail_email_only():
    
    new_details = update_details
    
    del new_details['user']['username']
    del new_details['user']['password']
    
    response = client.patch(
        f"/user/update/?id={new_details['id']}",
        json=new_details['user']
    )
    
    assert response.status_code == 200
    assert response.text == '"user updated"'
    
def test_update_user_detail_password_only():
    
    new_details = update_details
    
    del new_details['user']['username']
    del new_details['user']['email']
    
    response = client.patch(
        f"/user/update/?id={new_details['id']}",
        json=new_details['user']
    )
    
    assert response.status_code == 200
    assert response.text == '"user updated"'
    
def test_delete_user_success():
    id = "3fa45f64-5717-6254-b3fc-2c963f66afa6"
    response = client.delete(
        f"/user/delete/{id}",
        headers={"accept": "application/json"}
    )
    
    print(response.json())
    
    assert response.status_code == 200
    
def test_delete_user_failure():
    id = '23'
    
    response = client.delete(
        f"/user/delete/{id}"
    )
    
    assert response.status_code == 422
    
def test_get_single_user_success():
    
    id = '3fa85f64-5717-4521-b3fc-2c963f66afa6'
    
    response = client.get(
        f"/user/{id}"
    )
    
    assert response.status_code == 200
    
def test_get_single_user_failure():
    
    id = '3fa85f64'
    
    response = client.get(
        f"/user/{id}"
    )
    
    assert response.status_code == 422
    
    
def test_get_all_users_success():

    
    response = client.get(
        "/user/all/"
    )
    
    response = response.json()

    
    assert isinstance(response, list)
    