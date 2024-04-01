from django.test import TestCase
from django.test import TestCase
from .models import User, Doctor, Chats
from .views import (
    register_user,
    login_user,
    get_user_details,
    register_doctor,
    get_doctor_details,
    update_chat_data,
    get_stress_data,
)
import json
from unittest.mock import patch

class UserLoginTests(TestCase):
    def test_successful_login(self):
        # Login with correct credentials
        data = {"email": "kam@gmail.com", "password": "password"}
        response = self.client.post("http://127.0.0.1:8000/users/login/", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Login successful")
        self.assertIn("token", response.json())

    def test_incorrect_email(self):
    # Login with incorrect email
        data = {"email": "invalid@email.com", "password": "password"}
        response = self.client.post("http://127.0.0.1:8000/users/login/", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("Login unsuccessful", response.json()["message"])
        self.assertEqual(response.json()["message"], "Login unsuccessful")
    
    def test_incorrect_password(self):
         # Login with incorrect password        
        data = {"email": "kam@gmail.com", "password": "wrongpassword"} 
        response = self.client.post("http://127.0.0.1:8000/users/login/", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Login unsuccessful")


class DoctorDetailsTests(TestCase):

    def test_retrieve_all_doctor_details(self):
        # Retrieve doctor details
        response = self.client.get("http://127.0.0.1:8000/users/get_details/")  # Assuming URL for this view

        self.assertEqual(response.status_code, 200)
        doctor_data = json.loads(response.content)

        self.assertEqual(len(doctor_data), 10)

         # Assert details of first doctor
        self.assertEqual(doctor_data[0]["name"], "Dr. Sarah Johnson")
        self.assertEqual(doctor_data[0]["specialisation"], "Clinical Psychologist")
        self.assertEqual(doctor_data[0]["experience"], "15 years")
        self.assertEqual(doctor_data[0]["charge"], "2000.00")

        # Assert details of second doctor
        self.assertEqual(doctor_data[1]["name"], "Dr. Michael Smith")
        self.assertEqual(doctor_data[1]["specialisation"], "Psychiatrist")
        self.assertEqual(doctor_data[1]["experience"], "7 years")
        self.assertEqual(doctor_data[1]["charge"], "2500.00")

class ChatDataTests(TestCase):

    def test_successful_chat_update(self):
        # Generate a valid authorization token
        token = "b645e21d-db30-4729-bc60-4cf83df96c49"
        print(token)  # This will print the actual token value

        # Prepare test data
        data = {
            "text": "This is a test chat message.",
            "is_stress_checked": True,
        }

         # Send POST request with authorization header and data
        response = self.client.post("http://127.0.0.1:8000/users/update_chat/", json.dumps(data), content_type="application/json",
                                    HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["message"], "Chat added successfully")

    def test_invalid_token(self):
        # Send POST request with an invalid token
        data = {
            "text": "Test message with invalid token.",
            "is_stress_checked": True,
        }

        response = self.client.post("http://127.0.0.1:8000/users/update_chat/", json.dumps(data), content_type="application/json",
                                    HTTP_AUTHORIZATION="Bearer invalid_token")

        self.assertEqual(response.status_code, 405)  # Unauthorized


class StressDataTests(TestCase):
    def test_successful_stress_data_retrieval(self):
        # Generate a valid authorization token
        token = "b645e21d-db30-4729-bc60-4cf83df96c49"

        response = self.client.get("http://127.0.0.1:8000/users/get_stress_info/", HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, 201)

