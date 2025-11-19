from __future__ import annotations

from datetime import datetime
from typing import ClassVar
from django.db import models
from django.db.models.manager import Manager

class Token(models.Model):
    key: models.CharField[str, str]
    user: models.OneToOneField  # pyright: ignore[reportMissingTypeArgument]
    created: models.DateTimeField[datetime, datetime]

    objects: ClassVar[  # pyright: ignore[reportIncompatibleVariableOverride]
        Manager["Token"]
    ]

    @classmethod
    def generate_key(cls) -> str: ...
