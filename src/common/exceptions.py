from typing import Any

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def drf_exception_handler(exc: Exception, context: dict[str, Any]):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        response = Response(
            {"detail": f"A database constraint was violated. {exc}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return response
