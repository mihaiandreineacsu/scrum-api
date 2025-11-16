from typing import Any, override
from datetime import date
from django.urls import reverse
from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework.test import APIClient
from rest_framework.test import APITestCase as RestAPITestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from core.models import User, ScrumAPIModel
from core.tests.utils import (
    TEST_OTHER_USER_EMAIL,
    TEST_OTHER_USER_PASSWORD,
    create_test_user,
)


class ScrumAPITestCase(RestAPITestCase):

    VIEW_NAME = ""

    def api_url(self, action: str, args: list[Any]) -> str:
        """Create and return an API URL."""
        return reverse(f"{self.VIEW_NAME}:{self.VIEW_NAME}-{action}", args=args)


class PublicAPITestCase(ScrumAPITestCase):
    """Test unauthenticated API requests."""

    def assert_auth_required(self) -> None:
        """Test authentication is required to call API."""
        methods = {"list": ["get", "post"], "detail": ["get", "put", "patch", "delete"]}

        def check_auth_required(action: str, method: str, args: list[Any]) -> None:
            res: Response = getattr(self.client, method)(self.api_url(action, args))
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        for action, method_list in methods.items():
            for method in method_list:
                args = [0] if action == "detail" else []
                check_auth_required(action, method, args)


class PrivateAPITestCase(ScrumAPITestCase):

    user = User()
    other_user = User()
    api_model = type(ScrumAPIModel)
    api_serializer = type(ModelSerializer[ScrumAPIModel])
    ordering = "-id"

    queryset: QuerySet[ScrumAPIModel] = QuerySet()

    VIEW_NAME = ""

    def get_queryset(self):
        return self.queryset.filter(user=self.user).order_by(self.ordering)

    @override
    def setUp(self):
        self.user = create_test_user()
        self.other_user = create_test_user(
            email=TEST_OTHER_USER_EMAIL, password=TEST_OTHER_USER_PASSWORD
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def assert_create_model(self, payload: dict[str, Any]) -> None:
        url = self.api_url("list", [])
        res: Response = self.client.post(url, payload, format="json")
        instance = self.api_model.objects.get(id=res.data["id"])
        serializer = self.api_serializer(instance, many=False)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(instance.user, self.user)

    def assert_retrieve_models(self):
        """Test retrieving Models."""
        url = self.api_url("list", [])
        res: Response = self.client.get(url)
        results = self.get_queryset()
        serializer = self.api_serializer(results, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def assert_retrieve_model(self, model_pk: Any):
        """Test retrieving model."""
        url = self.api_url("detail", [model_pk])
        res: Response = self.client.get(url)
        result = self.api_model.objects.get(id=res.data["id"])
        serializer = self.api_serializer(result, many=False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def assert_update_model(
        self,
        payload: dict[str, Any],
        model: ScrumAPIModel,
        partial_update: bool = False,
    ):
        """Test update model."""
        url = self.api_url("detail", [model.pk])
        if partial_update:
            res = self.client.patch(url, payload, format="json")
        else:
            res = self.client.put(url, payload, format="json")

        model.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for key in payload.keys():
            model_value = getattr(model, key)
            if isinstance(model_value, User):
                self.assertEqual(model_value, self.user)
                continue
            if hasattr(model_value, "all") and callable(
                getattr(model_value, "all", None)
            ):  # check if this is a many_to_many value
                model_value = list(model_value.all().values_list("pk", flat=True))
            if isinstance(model_value, Model):
                model_value = model_value.pk
            if isinstance(model_value, date):
                model_value = model_value.isoformat()
            self.assertEqual(model_value, payload[key])

    def assert_deleting_model(self, model: ScrumAPIModel):
        """Test deleting a model successful."""
        url = self.api_url("detail", [model.pk])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.api_model.objects.filter(id=model.pk).exists())

    def assert_deleting_other_user_model_error(self, model: ScrumAPIModel):
        """Test trying to delete another users model gives error."""
        url = self.api_url("detail", [model.pk])
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(self.api_model.objects.filter(id=model.pk).exists())

    def assert_updating_other_user_model_error(
        self,
        payload: dict[str, Any],
        model: ScrumAPIModel,
        partial_update: bool = False,
    ):
        """Test trying to put another users model gives error."""

        url = self.api_url("detail", [model.pk])
        if partial_update:
            res = self.client.patch(url, payload, format="json")
        else:
            res = self.client.put(url, payload, format="json")
        model.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        for key in payload.keys():
            model_value = getattr(model, key)
            if isinstance(model_value, User):
                self.assertNotEqual(model_value, self.user)
                continue
            if isinstance(model_value, Model):
                model_value = model_value.pk
            self.assertNotEqual(model_value, payload[key])

    def assert_retrieve_other_user_model_error(self, model_pk: Any):
        """Test trying to retrieve another users model gives error."""
        url = self.api_url("detail", [model_pk])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
