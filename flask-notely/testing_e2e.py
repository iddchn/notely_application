import requests
import json

BASE_URL = "http://backend:5001"

def test_signup():
    url = f"{BASE_URL}/user/signup"
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    print("Signup test passed")

def test_login():
    url = f"{BASE_URL}/user/login"
    payload = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    user_id = response.json().get("user_id")
    print("Login test passed")
    return user_id

def test_create_note(user_id):
    url = f"{BASE_URL}/notes"
    payload = {
        "user_id": user_id,
        "header": "Test Note",
        "body": "This is a test note."
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    note_id = response.json().get("note_id")
    print("Create note test passed")
    return note_id

def test_get_notes(user_id):
    url = f"{BASE_URL}/notes/all/{user_id}"
    response = requests.get(url)
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) > 0
    print("Get notes test passed")

def test_update_note(note_id):
    url = f"{BASE_URL}/notes/{note_id}"
    payload = {
        "header": "Updated Test Note",
        "body": "This is an updated test note."
    }
    response = requests.put(url, json=payload)
    assert response.status_code == 200
    print("Update note test passed")

def test_delete_note(note_id):
    url = f"{BASE_URL}/notes/{note_id}"
    response = requests.delete(url)
    assert response.status_code == 200
    print("Delete note test passed")

if __name__ == "__main__":
    test_signup()
    user_id = test_login()
    note_id = test_create_note(user_id)
    test_get_notes(user_id)
    test_update_note(note_id)
    test_delete_note(note_id)