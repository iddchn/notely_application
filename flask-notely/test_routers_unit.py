import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from bson import ObjectId
from application.routers.note_routers import note_blueprint
from application.routers.user_routers import user_blueprint

class TestNoteRouters(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(note_blueprint, url_prefix="/notes")
        self.client = self.app.test_client()

    @patch("application.routers.note_routers.mongo_db")
    def test_create_note_success(self, mock_db):
        mock_db.notes.insert_one.return_value.inserted_id = "mocked_note_id"
        response = self.client.post(
            "/notes",
            json={"user_id": str(ObjectId()), "header": "Test Header", "body": "Test Body"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("Note created successfully", response.json["message"])

    @patch("application.routers.note_routers.mongo_db")
    def test_get_notes_success(self, mock_db):
        mock_db.notes.find.return_value = [
            {"_id": "mocked_id", "user_id": str(ObjectId()), "header": "Header", "body": "Body"}
        ]
        response = self.client.get(f"/notes/all/{str(ObjectId())}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    @patch("application.routers.note_routers.mongo_db")
    def test_update_note_success(self, mock_db):
        mock_db.notes.update_one.return_value.matched_count = 1
        response = self.client.put(
            f"/notes/{str(ObjectId())}",
            json={"header": "Updated Header", "body": "Updated Body"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Note updated successfully", response.json["message"])

    @patch("application.routers.note_routers.mongo_db")
    def test_delete_note_success(self, mock_db):
        mock_db.notes.delete_one.return_value.deleted_count = 1
        response = self.client.delete(f"/notes/{str(ObjectId())}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Note deleted successfully", response.json["message"])


class TestUserRouters(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(user_blueprint, url_prefix="/user")
        self.client = self.app.test_client()

    @patch("application.routers.user_routers.mongo_db")
    def test_signup_success(self, mock_db):
        mock_db.users.insert_one.return_value = None
        response = self.client.post(
            "/user/signup",
            json={"name": "Test User", "email": "test@example.com", "password": "password123"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.json["message"])

    @patch("application.routers.user_routers.mongo_db")
    def test_login_success(self, mock_db):
        mock_user = {"_id": "mocked_id", "email": "test@example.com", "password": "hashed_password"}
        mock_db.users.find_one.return_value = mock_user
        with patch("application.routers.user_routers.check_password_hash", return_value=True):
            response = self.client.post(
                "/user/login",
                json={"email": "test@example.com", "password": "password123"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("Login successful", response.json["message"])

    @patch("application.routers.user_routers.mongo_db")
    def test_update_user_success(self, mock_db):
        mock_db.users.update_one.return_value.matched_count = 1
        response = self.client.put(
            "/user/",
            json={"id": str(ObjectId()), "name": "Updated User", "email": "updated@example.com", "password": "newpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("User updated successfully", response.json["message"])

    @patch("application.routers.user_routers.mongo_db")
    def test_delete_user_success(self, mock_db):
        mock_db.users.delete_one.return_value.deleted_count = 1
        response = self.client.delete("/user/", json={"id": str(ObjectId())})
        self.assertEqual(response.status_code, 200)
        self.assertIn("User and associated notes deleted", response.json["message"])


if __name__ == "__main__":
    unittest.main()