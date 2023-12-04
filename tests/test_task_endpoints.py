from .test_user_endpoints import client

common_user_id = '3fa45f64-5717-6354-b3fc-2c963f66afa6'

task_details = {
    "id": 0,
    "name": "string",
    "description": "string",
    "user_id": common_user_id,
    "created_at": "14:46:54.056Z",
    "due_date": "2023-11-15"
}

def test_add_task_success():
    
    response = client.post(
        "/task/add",
        json=task_details
    )
    
    
    assert response.status_code == 201
    assert response.content == '"task created"'


def test_add_task_failure():
    
    new_details = task_details
    
    response = client.post(
        "/task/add",
        json=new_details
    )
    
    
    assert response.status_code == 422
    assert response.content == '"action incomplete"'

    
def test_update_task_success():
    
    new_details = task_details
    
    del new_details['id']
    del new_details["description"]
    del new_details['name']
    
    #subject to change
    id  = 1
     
    new_details['description'] = "test-update"
    print(new_details)
    
    response = client.patch(
        f"/task/update/?id={id}",
        json=new_details
    )
    
    assert response.status_code == 200
    assert response.text == '"task modified"'
    
def test_update_task_failure():
    
    new_details = task_details
    
    del new_details['user_id']
    
    response = client.patch(
        "/task/update",
        json=new_details
    )
    
    assert response.status_code == 422
    assert response.content == '"action incomplete"'
    
def test_delete_task_success():
    
    response = client.delete(
        f"/task/delete/?id={2}"
    )
    
    assert response.status_code == 200
    assert response.content == '"task deleted"'
    
def test_delete_task_failure():
    
    
    response = client.delete(
        f"/task/delete/{200}"
    )
    
    assert response.status_code == 200
    assert response.text == '"task deleted"'

    
def test_get_single_task_success():
    
    expected = {
        "id": 2,
        "name": "string",
        "description": "string",
        "user": {
            "username": "useremail"
        },
        "created_at": "15:04:12.698000Z",
        "due_date": "2023-11-15"
    }
    
    response = client.get(
        f"/task/get/{2}"
    )
    
    assert response.json() == expected
    
def test_get_single_task_failure():

    
    response = client.get(
        f"/task/get/{200}"
    )
    
    assert response.status_code == 404

def test_get_all_tasks_success():
    
    response = client.get(
        "/task/get/all"
    )
    
    
    response = response.json()
    
    assert isinstance(response, list)