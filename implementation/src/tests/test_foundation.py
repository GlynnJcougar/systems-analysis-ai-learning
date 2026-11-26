import os
import subprocess
import sys
from pathlib import Path

from django.db import connection
from django.test import SimpleTestCase, TransactionTestCase
from django.urls import reverse


MANAGE_PY = Path(__file__).resolve().parents[1] / "manage.py"


class FoundationStartupTests(SimpleTestCase):
    def test_root_page_is_available(self):
        response = self.client.get(reverse("foundation"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Application foundation")

    def test_missing_secret_key_fails_configuration(self):
        environment = os.environ.copy()
        environment.pop("DJANGO_SECRET_KEY", None)
        result = subprocess.run(
            [sys.executable, str(MANAGE_PY), "check"],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY must be set.", result.stderr)

    def test_missing_database_url_fails_configuration(self):
        environment = os.environ.copy()
        environment.pop("DATABASE_URL", None)
        result = subprocess.run(
            [sys.executable, str(MANAGE_PY), "check"],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DATABASE_URL must be set.", result.stderr)

    def test_non_postgresql_database_fails_configuration(self):
        environment = os.environ.copy()
        environment["DATABASE_URL"] = "sqlite:///not-supported.sqlite3"
        result = subprocess.run(
            [sys.executable, str(MANAGE_PY), "check"],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DATABASE_URL must specify a PostgreSQL", result.stderr)


class FoundationDatabaseTests(TransactionTestCase):
    def test_postgresql_database_is_initialized(self):
        self.assertEqual(connection.vendor, "postgresql")
        tables = connection.introspection.table_names()
        self.assertIn("django_migrations", tables)
        self.assertIn("django_content_type", tables)
