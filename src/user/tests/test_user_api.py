"""
Tests for the user API.
"""

import os
import tempfile
from typing import override

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User
from core.tests.utils import (
    TEST_OTHER_USER_EMAIL,
    TEST_OTHER_USER_FULL_NAME,
    TEST_OTHER_USER_PASSWORD,
    TEST_USER_EMAIL,
    TEST_USER_FULL_NAME,
    TEST_USER_PASSWORD,
    create_test_guest_user,
    create_test_user,
    validate_response_data,
)

CREATE_USER_URL = reverse("user:create")
CREATE_GUEST_URL = reverse("user:create-guest")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")
PASSWORD_RESET_URL = reverse("user:password_reset:reset-password-request")


def image_upload_url(_: str | int):
    """Create and return an image upload URL"""
    return reverse("user:user-upload-image")


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    @override
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "name": TEST_USER_FULL_NAME,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        data = validate_response_data(res)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", data)

    def test_create_guest_user_success(self):
        """Test creating a guest user is successful."""
        res = self.client.post(CREATE_GUEST_URL, {})

        data = validate_response_data(res)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(email__endswith="@guest.com").first()
        assert user is not None
        self.assertTrue(user.is_guest)
        self.assertNotIn("password", data)
        self.assertIn("token", data)

    def test_create_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "name": TEST_USER_FULL_NAME,
        }
        _ = create_test_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # TODO: Add assertion for object not changed

    def test_create_user_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            "email": TEST_USER_EMAIL,
            "password": "pwd1",
            "name": TEST_USER_FULL_NAME,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        payload = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "name": TEST_USER_FULL_NAME,
        }
        _ = create_test_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        data = validate_response_data(res)

        self.assertIn("token", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_password(self):
        """Test returns error if credentials invalid."""
        _ = create_test_user()

        payload = {"email": TEST_USER_EMAIL, "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        data = validate_response_data(res)

        self.assertNotIn("token", data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data["detail"], ["Unable to authenticate with provided credentials."]
        )

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "johndoe@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        data = validate_response_data(res)

        self.assertNotIn("token", data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentications is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_api_triggers_email(self):
        """Test that the password reset API triggers an email."""
        user = create_test_user()
        response = self.client.post(PASSWORD_RESET_URL, {"email": user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Password Reset for Join", str(email.subject))
        self.assertIn(user.email, email.to)


class PrivateUserApiTests(TestCase):
    """Test API request that require authentication."""

    user = User()
    guest_user = User()

    @override
    def setUp(self):
        self.user = create_test_user()
        self.guest_user = create_test_guest_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        data = validate_response_data(res)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], self.user.name)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["image"], self.user.image)

    def test_post_me_not_allowed(self):
        """Test post is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_with_password(self):
        """Test updating the user profile for the authenticated user."""
        payload = {
            "email": TEST_OTHER_USER_EMAIL,
            "name": TEST_OTHER_USER_FULL_NAME,
            "password": TEST_OTHER_USER_PASSWORD,
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_profile_without_password(self):
        """Test updating the user profile for the authenticated user."""
        payload = {
            "email": TEST_OTHER_USER_EMAIL,
            "name": TEST_OTHER_USER_FULL_NAME,
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_user_profile(self):
        """Test deleting the user profile for the authenticated user."""
        guest_client = APIClient()
        guest_client.force_authenticate(self.guest_user)
        res = guest_client.delete(ME_URL)

        with self.assertRaises(User.DoesNotExist):
            self.guest_user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    user = User()

    @override
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(self.user)

    @override
    def tearDown(self):
        self.user.image.delete()  # TODO: fix , does not work

    def test_upload_image(self):
        """Test uploading an image to a user."""
        url = image_upload_url(self.user.pk)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            _ = image_file.seek(0)
            payload = {"image": image_file}
            res = self.client.post(url, payload, format="multipart")
            data = validate_response_data(res)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", data)
        self.assertTrue(os.path.exists(self.user.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.user.pk)
        payload = {"image": "notanimage"}
        res = self.client.post(url, payload, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
