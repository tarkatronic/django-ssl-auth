SECRET_KEY = 'Pangalactic Gargleblaster'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'testapp'
]

ROOT_URLCONF = 'testapp.urls'

MIDDLEWARE = MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_ssl_auth.SSLClientAuthMiddleware',
)

ROOT_URLCONF = 'testapp.urls'

AUTHENTICATION_BACKENDS = ('django_ssl_auth.SSLClientAuthBackend', )
USER_DATA_FN = 'django_ssl_auth.fineid.user_dict_from_dn'
AUTOCREATE_VALID_SSL_USERS = True

# This setting is used for testing so that the test cases can simulate
# an https connection to Django. Please see the Django documentation
# and understand this setting before considering using it in your own site.
# https://docs.djangoproject.com/en/1.9/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

SILENCED_SYSTEM_CHECKS = (
    '1_10.W001',
)

SSLCLIENT_LOGIN_URL = None
