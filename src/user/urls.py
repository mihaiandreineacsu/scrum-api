"""
URL mappings for the user API.
"""

from django.urls import include, path

from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("create-guest/", views.CreateGuestUserView.as_view(), name="create-guest"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path(
        "user-upload-image/",
        views.UserUploadImageView.as_view(  # pyright: ignore[reportUnknownMemberType]
            {"post": "upload_image"}
        ),
        name="user-upload-image",
    ),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
