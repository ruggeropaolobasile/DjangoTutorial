import importlib
import os
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.db.utils import DatabaseError
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class RootRedirectTests(SimpleTestCase):
    def test_root_redirects_to_polls_index(self):
        response = self.client.get("/")
        self.assertRedirects(response, reverse("polls:index"), fetch_redirect_response=False)


class HealthzTests(TestCase):
    def test_healthz_returns_ok(self):
        response = self.client.get(reverse("healthz"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    @patch("mysite.views.connections")
    def test_healthz_returns_503_when_database_is_unreachable(self, mocked_connections):
        mocked_connections.__getitem__.return_value.cursor.side_effect = DatabaseError

        response = self.client.get(reverse("healthz"))

        self.assertEqual(response.status_code, 503)
        self.assertJSONEqual(response.content, {"status": "error", "database": "unreachable"})


class DatabaseConfigTests(SimpleTestCase):
    def test_database_url_requires_database_name(self):
        with patch.dict(os.environ, {"DATABASE_URL": "postgres://user:pass@localhost:5432"}, clear=False):
            import mysite.settings as settings

            with self.assertRaisesMessage(ImproperlyConfigured, "DATABASE_URL must include a database name"):
                importlib.reload(settings)

            with patch.dict(os.environ, {"DATABASE_URL": ""}, clear=False):
                importlib.reload(settings)


class ProductionSettingsValidationTests(SimpleTestCase):
    def test_debug_false_requires_public_host_configuration(self):
        with patch.dict(
            os.environ,
            {
                "DEBUG": "False",
                "SECRET_KEY": "test-secret",
                "ALLOWED_HOSTS": "",
                "CSRF_TRUSTED_ORIGINS": "",
                "PUBLIC_DOMAIN": "",
                "RENDER_EXTERNAL_HOSTNAME": "",
                "RAILWAY_PUBLIC_DOMAIN": "",
                "DATABASE_URL": "",
            },
            clear=False,
        ):
            import mysite.settings as settings

            with self.assertRaisesMessage(
                ImproperlyConfigured,
                "Set PUBLIC_DOMAIN or ALLOWED_HOSTS with your public host when DEBUG=False",
            ):
                importlib.reload(settings)

            with patch.dict(
                os.environ,
                {
                    "DEBUG": "True",
                    "ALLOWED_HOSTS": "127.0.0.1,localhost",
                    "DATABASE_URL": "",
                },
                clear=False,
            ):
                importlib.reload(settings)


class PublicDomainSettingsTests(SimpleTestCase):
    def test_public_domain_is_added_to_allowed_hosts_and_csrf_origins(self):
        with patch.dict(
            os.environ,
            {
                "ALLOWED_HOSTS": "example.com",
                "CSRF_TRUSTED_ORIGINS": "https://example.com",
                "PUBLIC_DOMAIN": "demo-app.up.railway.app",
                "DATABASE_URL": "",
            },
            clear=False,
        ):
            import mysite.settings as settings

            reloaded_settings = importlib.reload(settings)

            self.assertIn("demo-app.up.railway.app", reloaded_settings.ALLOWED_HOSTS)
            self.assertIn("https://demo-app.up.railway.app", reloaded_settings.CSRF_TRUSTED_ORIGINS)

            with patch.dict(
                os.environ,
                {
                    "ALLOWED_HOSTS": "",
                    "CSRF_TRUSTED_ORIGINS": "",
                    "PUBLIC_DOMAIN": "",
                    "RAILWAY_PUBLIC_DOMAIN": "",
                    "DATABASE_URL": "",
                },
                clear=False,
            ):
                importlib.reload(settings)

    def test_public_domain_accepts_url_format(self):
        with patch.dict(
            os.environ,
            {
                "ALLOWED_HOSTS": "",
                "CSRF_TRUSTED_ORIGINS": "",
                "PUBLIC_DOMAIN": "https://demo-app.up.railway.app/",
                "DATABASE_URL": "",
            },
            clear=False,
        ):
            import mysite.settings as settings

            reloaded_settings = importlib.reload(settings)

            self.assertIn("demo-app.up.railway.app", reloaded_settings.ALLOWED_HOSTS)
            self.assertIn("https://demo-app.up.railway.app", reloaded_settings.CSRF_TRUSTED_ORIGINS)

            with patch.dict(os.environ, {"PUBLIC_DOMAIN": "", "DATABASE_URL": ""}, clear=False):
                importlib.reload(settings)

    def test_render_external_hostname_is_used_as_fallback(self):
        with patch.dict(
            os.environ,
            {
                "ALLOWED_HOSTS": "",
                "CSRF_TRUSTED_ORIGINS": "",
                "PUBLIC_DOMAIN": "",
                "RENDER_EXTERNAL_HOSTNAME": "my-app.onrender.com",
                "RAILWAY_PUBLIC_DOMAIN": "",
                "DATABASE_URL": "",
            },
            clear=False,
        ):
            import mysite.settings as settings

            reloaded_settings = importlib.reload(settings)

            self.assertIn("my-app.onrender.com", reloaded_settings.ALLOWED_HOSTS)
            self.assertIn("https://my-app.onrender.com", reloaded_settings.CSRF_TRUSTED_ORIGINS)

            with patch.dict(
                os.environ,
                {
                    "RENDER_EXTERNAL_HOSTNAME": "",
                    "DATABASE_URL": "",
                },
                clear=False,
            ):
                importlib.reload(settings)

    def test_public_domain_has_priority_over_railway_public_domain(self):
        with patch.dict(
            os.environ,
            {
                "ALLOWED_HOSTS": "",
                "CSRF_TRUSTED_ORIGINS": "",
                "PUBLIC_DOMAIN": "https://my-server.example.com/",
                "RAILWAY_PUBLIC_DOMAIN": "railway.up.railway.app",
                "DATABASE_URL": "",
            },
            clear=False,
        ):
            import mysite.settings as settings

            reloaded_settings = importlib.reload(settings)

            self.assertIn("my-server.example.com", reloaded_settings.ALLOWED_HOSTS)
            self.assertNotIn("railway.up.railway.app", reloaded_settings.ALLOWED_HOSTS)
            self.assertIn("https://my-server.example.com", reloaded_settings.CSRF_TRUSTED_ORIGINS)

            with patch.dict(
                os.environ,
                {
                    "PUBLIC_DOMAIN": "",
                    "RAILWAY_PUBLIC_DOMAIN": "",
                    "DATABASE_URL": "",
                },
                clear=False,
            ):
                importlib.reload(settings)

    def test_database_url_parses_supported_options(self):
        with patch.dict(
            os.environ,
            {
                "DATABASE_URL": (
                    "postgres://user:pass@localhost:5432/mydb?sslmode=require&connect_timeout=10&application_name=demo"
                )
            },
            clear=False,
        ):
            import mysite.settings as settings

            reloaded_settings = importlib.reload(settings)
            db_settings = reloaded_settings.DATABASES["default"]

            self.assertEqual(db_settings["NAME"], "mydb")
            self.assertEqual(db_settings["OPTIONS"], {"sslmode": "require", "connect_timeout": "10"})

            with patch.dict(os.environ, {"DATABASE_URL": ""}, clear=False):
                importlib.reload(settings)
