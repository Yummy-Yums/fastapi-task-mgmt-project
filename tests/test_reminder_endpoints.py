from .test_user_endpoints import client

reminder_details = {
  "text": "string",
  "remind_at": "16:15:33.170Z",
  "task_id": 0
}

def test_add_reminder_success():
    
    response = client.post(
        "/reminder/add",
        json=reminder_details
    )
    
    assert response.text == '"reminder has been created"'
    assert response.status_code == 201
    
# have to think of another way
def test_add_reminder_failure():
    
    copy_details = reminder_details
    
    copy_details['text'] = 23
    
    response = client.post(
        "/reminder/add",
        json=copy_details
    )
    
    assert response.text == '"reminder not created"'
    assert response.status_code == 422
    
update_details = {
    "id": 2,
    "body": {
        "text": "string",
        "remind_at": "16:57:24.046Z",
        "task_id": 0
    }
}
    
def test_update_reminder_success():
    
    id = update_details["id"]
    body = update_details["body"]
    
    response = client.patch(
        f"/reminder/update/?id={id}",
        json=body
    )
    
    assert response.text == '"reminder modified"'
    assert response.status_code == 200
    

# have to refactor this 
def test_update_reminder_failure():
    
    id = update_details["id"]
    body = update_details["body"]
    
    response = client.patch(
        f"/reminder/update/?id={0}",
        json=body
    )
    
    assert response.text == "reminder not modified"
    assert response.status_code == 422
    
def test_delete_reminder_success():
    id = 1
    
    response = client.delete(
        f"/reminder/delete/{id}"
    )
    
    assert response.status_code == 200

# find a way to recreate scenario
def test_delete_reminder_failure():
    
    id = '23'
    
    response = client.delete(
        f"/reminder/delete/{id}"
    )
    
    assert response.status_code == 422
    
def test_get_single_reminder_success():
    
    expected = {
        
    }
    
    response = client.get(
        f"/reminder/update/{2}"
    )
    
    assert response.json() == expected
    
def test_get_single_reminder_failure():
    
    response = client.get(
        f"/reminder/get/{100}"
    )
    
    assert response.status_code == 404
    
def test_get_all_reminders_success():
    
    response = client.get(
        "/reminder/get/all"
    )
    
    response = response.json()
    print(response)
    assert isinstance(response, list )