from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase


class Tests(TestCase):
    """Automated tests to ensure everything is working as designed."""

    def test_login_new_user(self):
        """Ensure users are automatically created."""
        # Simulate an SSL connection (of a new user)
        self.client.get(
            settings.LOGIN_URL,
            HTTP_X_SSL_AUTHENTICATED='SUCCESS',
            HTTP_X_SSL_USER_DN='C=FI/serialNumber=42/GN=John/SN=Smith/CN=John Smith',
            HTTP_X_FORWARDED_PROTOCOL='https'
        )

        # Ensure the new user was created
        user = User.objects.last()
        self.assertEqual(user.username, '42')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Smith')

    def test_login_new_user_sslurl(self):
        """Ensure users are automatically created."""
        # Simulate an SSL connection (of a new user)
        with self.settings(SSLCLIENT_LOGIN_URL = "/pivlogin"):
            self.client.get(
                settings.SSLCLIENT_LOGIN_URL,
                HTTP_X_SSL_AUTHENTICATED='SUCCESS',
                HTTP_X_SSL_USER_DN='C=FI/serialNumber=42/GN=John/SN=Smith/CN=John Smith',
                HTTP_X_FORWARDED_PROTOCOL='https'
            )

            # Ensure the new user was created
            user = User.objects.last()
            self.assertEqual(user.username, '42')
            self.assertEqual(user.first_name, 'John')
            self.assertEqual(user.last_name, 'Smith')
