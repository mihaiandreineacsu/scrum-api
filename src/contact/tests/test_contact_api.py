"""
Tests for contact APIs.
"""

from typing import override

from django.db.models.functions import Lower

from contact.serializers import ContactSerializer
from core.models import Contact
from core.tests.api_test_case import PrivateAPITestCase, PublicAPITestCase
from core.tests.utils import (
    TEST_OTHER_CONTACT_EMAIL,
    TEST_OTHER_CONTACT_FULL_NAME,
    TEST_OTHER_CONTACT_PHONE_NUMBER,
    create_test_contact,
)


class PublicContactAPITests(PublicAPITestCase):
    """Test unauthenticated API requests."""

    VIEW_NAME = "contact"

    def test_auth_required(self):
        self.assert_auth_required()


class PrivateContactAPITests(PrivateAPITestCase):
    """Test authenticated API requests."""

    user_contact = Contact()
    other_user_contact = Contact()

    api_model = Contact
    api_serializer = ContactSerializer

    ordering = Lower("name")

    VIEW_NAME = "contact"

    queryset = Contact.objects.all()

    @override
    def setUp(self) -> None:
        super().setUp()
        self.user_contact = create_test_contact(user=self.user)
        self.other_user_contact = create_test_contact(user=self.other_user)

    def test_create_contact(self):
        """Test creating a contact."""
        payload = {
            "email": TEST_OTHER_CONTACT_EMAIL,
            "name": TEST_OTHER_CONTACT_FULL_NAME,
            "phone_number": TEST_OTHER_CONTACT_PHONE_NUMBER,
            "user": self.other_user.pk,
        }
        self.assert_create_model(payload)

    def test_retrieve_contacts(self):
        """Test retrieving contacts."""
        self.assert_retrieve_models()

    def test_retrieve_contact(self):
        """Test retrieving contact."""
        self.assert_retrieve_model(self.user_contact.pk)

    def test_partial_update(self):
        """Test partial update a contact."""
        updates = [
            {"email": TEST_OTHER_CONTACT_EMAIL, "user": self.other_user.pk},
            {"name": TEST_OTHER_CONTACT_FULL_NAME, "user": self.other_user.pk},
            {
                "phone_number": TEST_OTHER_CONTACT_PHONE_NUMBER,
                "user": self.other_user.pk,
            },
        ]
        for update in updates:
            self.assert_update_model(update, self.user_contact, partial_update=True)

    def test_full_update(self):
        """Test full update of contact."""
        payload = {
            "email": TEST_OTHER_CONTACT_EMAIL,
            "name": TEST_OTHER_CONTACT_FULL_NAME,
            "phone_number": TEST_OTHER_CONTACT_PHONE_NUMBER,
            "user": self.other_user.pk,
        }
        self.assert_update_model(payload, self.user_contact)

    def test_deleting_contact(self):
        """Test deleting a contact successful."""
        self.assert_deleting_model(self.user_contact)

    def test_deleting_other_user_contact_error(self):
        """Test trying to delete another users contact gives error."""
        self.assert_deleting_other_user_model_error(self.other_user_contact)

    def test_full_updating_other_user_contact_error(self):
        """Test trying to put another users contact gives error."""
        payload = {
            "email": TEST_OTHER_CONTACT_EMAIL,
            "name": TEST_OTHER_CONTACT_FULL_NAME,
            "phone_number": TEST_OTHER_CONTACT_PHONE_NUMBER,
            "user": self.user.pk,
        }
        self.assert_updating_other_user_model_error(payload, self.other_user_contact)

    def test_partial_update_other_user_contact_error(self) -> None:
        """Test trying to patch another user's contact gives error."""

        updates = [
            {"email": TEST_OTHER_CONTACT_EMAIL, "user": self.user.pk},
            {"name": TEST_OTHER_CONTACT_FULL_NAME, "user": self.user.pk},
            {"phone_number": TEST_OTHER_CONTACT_PHONE_NUMBER, "user": self.user.pk},
        ]

        for update in updates:
            self.assert_updating_other_user_model_error(
                update, self.other_user_contact, partial_update=True
            )

    def test_retrieve_other_user_contact_error(self):
        """Test trying to retrieve another users contact gives error."""
        self.assert_retrieve_other_user_model_error(self.other_user_contact.pk)
