===============
django-ssl-auth
===============

.. image:: https://img.shields.io/pypi/v/django-ssl-auth.svg
   :target: https://pypi.python.org/pypi/django-ssl-auth
   :alt: Latest Version

.. image:: https://travis-ci.org/tarkatronic/django-ssl-auth.svg?branch=master
   :target: https://travis-ci.org/tarkatronic/django-ssl-auth
   :alt: Test/build status

.. image:: https://codecov.io/gh/tarkatronic/django-ssl-auth/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tarkatronic/django-ssl-auth
   :alt: Code coverage

SSL authentication backend and middleware for Django for authenticating users
with SSL client certificates

License
=======

MIT license, see LICENSE.txt for full text.

Setup
=====

SSL
---

Set up nginx and create SSL certificates for your server and set up the paths
to server private key, server certificate and CA certificate used to sign
the client certificates. Example configuration file is in samples/nginx.conf

If you are on OS X, I suggest OS X KeyChain access for doing this for
testing, as it will automatically make your client certificates available in
all both Google chrome & Safari. Instructions can be found e.g.
http://www.dummies.com/how-to/content/how-to-become-a-certificate-authority-using-lion-s.html

On other platforms, there are many tutorials on how to do this with OpenSSL
e.g. http://pages.cs.wisc.edu/~zmiller/ca-howto/

Restart your ngninx (sudo nginx -s restart), make sure your green unicorn is
running and check that your https:// url loads your application and the
*server certificate is valid*.

This module
-----------

1. run setup.py (sudo python setup.py install) or install the latest release
   using ``pip install django_ssl_auth``

2. edit your ``settings.py``

   1. add ``"django_ssl_auth.SSLClientAuthMiddleware"`` to your ``MIDDLEWARE_CLASSES``
   2. add ``"django_ssl_auth.SSLClientAuthBackend"`` to your ``AUTHENTICATION_BACKENDS``

Configuration
~~~~~~~~~~~~~

There are two things you need to do in ``settings.py``

1. Define a function that can return a dictionary with fields that are required
   by your user model, e.g.
   ``USER_DATA_FN = 'django_ssl_auth.fineid.user_dict_from_dn`` is a sample
   implementation that takes the required fields from the DN of a Finnish
   government issued ID smart card for the ``contrib.auth.models.User``.
2. To automatically create ``User``s for all valid certificate holders, set
   ``AUTOCREATE_VALID_SSL_USERS = True``. Auto-created users will be set to
   inactive by default, consider using the `User.is_active`_ field in your
   `LOGIN_REDIRECT_URL`_ view to notifying the user of their status.
   
For details, see ``testapp/ssltest/settings.py``
   
Optional Configuration
~~~~~~~~~~~~~~~~~~~~~~
1. If you want to use the standard login url, set `SSLCLIENT_LOGIN_URL = None` or leave it undefined.
   For cases where you want a seperate login URL for SSL auth, set `SSLCLIENT_LOGIN_URL = "/YOUR_URL/"`.
   `SSLCLIENT_LOGIN_URL` is designed for use cases where some users login via the regular Django login
   without using SSLCLIENT auth, but you have a seperate login URL for users that login with SSLCLIENT auth.
2. If you want to allow insecure request (eg. your django app is behind a proxy or load balancer) set
   `SSLCLIENT_ALLOW_INSECURE_REQUEST = True`. If not set, secure connection will be required by default.

Smart Card support
~~~~~~~~~~~~~~~~~~

For (Finnish) instructions see ``doc/fineid/FINEID.md``


TODO
====

* Active directory integration.

How to get help
===============

Please do ask your questions on http://stackoverflow.com/
I am active there, and more likely to answer you publicly.
Also, you can try catching TheJoey on #django@freenode

.. _User.is_active: https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User.is_active
.. _LOGIN_REDIRECT_URL: https://docs.djangoproject.com/en/stable/ref/settings/#login-redirect-url
