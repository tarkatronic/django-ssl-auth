# -*- coding: utf-8 -*-
#
# Copyright © 2013 SSH Communication Security Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
from importlib import import_module

import django
from django.conf import settings
from django.contrib.auth import authenticate, backends, get_user_model, login
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url


try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10+
except ImportError:
    MiddlewareMixin = object  # Django < 1.10


logging.basicConfig()
logger = logging.getLogger(__name__)

User = get_user_model()


def check_user_auth(user):
    if django.VERSION < (1, 10):
        return user.is_authenticated()
    else:
        return user.is_authenticated


class SSLClientAuthBackend(backends.ModelBackend):
    @staticmethod
    def authenticate(request=None):
        _module_name, _function_name = settings.USER_DATA_FN.rsplit('.', 1)
        _module = import_module(_module_name)  # We need a non-empty fromlist
        USER_DATA_FN = getattr(_module, _function_name)  # NOQA: N806

        if not request.is_secure():
            logger.debug("insecure request")
            return None
        authentication_status = request.META.get('HTTP_X_SSL_AUTHENTICATED', None)
        if (authentication_status != "SUCCESS" or 'HTTP_X_SSL_USER_DN' not in request.META):
            logger.warn(
                "HTTP_X_SSL_AUTHENTICATED marked failed or HTTP_X_SSL_USER_DN header missing"
            )
            return None
        dn = request.META.get('HTTP_X_SSL_USER_DN')
        user_data = USER_DATA_FN(dn)
        username = user_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.info("user {0} not found".format(username))
            if settings.AUTOCREATE_VALID_SSL_USERS:
                user = User(**user_data)
                user.save()
            else:
                return None
        logger.info("user {0} authenticated using a certificate issued to {1}".format(username, dn))
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SSLClientAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured()
        if check_user_auth(request.user):
            return
        if int(request.META.get('HTTP_X_REST_API', 0)):
            user = authenticate(request=request)
            if user is None or not check_user_auth(user):
                return
            logger.debug("REST API call, not logging user in")
            request.user = user
        elif request.path_info == settings.LOGIN_URL:
            user = authenticate(request=request)
            if user is None or not check_user_auth(user):
                return
            logger.info("Logging user in")
            login(request, user)
            return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
