"""
Tests for contact APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Contact

from contact.serializers import (
    ContactSerializer
)


CONTACTS_URL = reverse('contact:contact-list')


def create_contact(user, **params):
    """Create and return a sample contact."""
    email = params.get('email', 'contact@mail.com')
    defaults = {
        'email': email,
        'phone_number': '0157777777777',
        'name': 'Contact Name',
    }
    defaults.update(params)

    contact = Contact.objects.create(user=user, **defaults)
    return contact


def detail_url(contact_id):
    """Create and return a contact detail URL."""
    return reverse('contact:contact-detail', args=[contact_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicContactAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CONTACTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContactAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_contacts(self):
        """Test retrieving a list of contacts."""
        create_contact(user=self.user)
        create_contact(user=self.user, email="contact2@mail.com")

        res = self.client.get(CONTACTS_URL)

        contacts = Contact.objects.all().order_by('-name')
        serializer = ContactSerializer(contacts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_contact(self):
        """Test retrieving a list of contacts."""
        contact = create_contact(user=self.user)
        url = detail_url(contact.id)
        res = self.client.get(url)

        serializer = ContactSerializer(contact)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_contact_list_limited_to_user(self):
        """Test list of contacts is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_contact(user=other_user)
        create_contact(user=self.user, email="contact2@mail.com")

        res = self.client.get(CONTACTS_URL)

        contacts = Contact.objects.filter(user=self.user)
        serializer = ContactSerializer(contacts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_contact(self):
        """Test creating a contact."""
        payload = {
            'email': 'contact@mail.com',
            'name': 'Contact Name',
            'phone_number': '0157336911111',
        }
        res = self.client.post(CONTACTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(contact, k), v)
        self.assertEqual(contact.user, self.user)

    def test_partial_update(self):
        """Test partial update if a contact."""
        contact = create_contact(
            user=self.user,
            email='contact@mail.com',
        )

        payload = {'email': 'contact2@mail.com'}
        url = detail_url(contact.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        self.assertEqual(contact.email, payload['email'])
        self.assertEqual(contact.user, self.user)

    def test_full_update(self):
        """Test full update of contact."""
        contact = create_contact(
            user=self.user,
        )

        payload = {
            'email': 'contact2@mail.com',
            'name': 'Contact2 Name',
            'phone_number': '015733691236',
        }
        url = detail_url(contact.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(contact, k), v)
        self.assertEqual(contact.user, self.user)

    def test_update_user_returns_error(self):
        """test changing the contact user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        contact = create_contact(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(contact.id)
        self.client.patch(url, payload)

        contact.refresh_from_db()
        self.assertEqual(contact.user, self.user)

    def test_deleting_contact(self):
        """Test deleting a contact successful."""
        contact = create_contact(user=self.user)

        url = detail_url(contact.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(id=contact.id).exists())

    def test_contact_other_users_contact_error(self):
        """Test trying to delete another users contact gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        contact = create_contact(user=new_user)

        url = detail_url(contact.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Contact.objects.filter(id=contact.id).exists())
