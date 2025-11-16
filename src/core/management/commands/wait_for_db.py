"""
Django command to wait for the database to be available.
"""

import time
from typing import Any, override

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopq2OpError


class Command(BaseCommand):
    """Django command to wait for database."""

    @override
    def handle(self, *args: tuple[Any, Any], **options: dict[str, Any]):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopq2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
