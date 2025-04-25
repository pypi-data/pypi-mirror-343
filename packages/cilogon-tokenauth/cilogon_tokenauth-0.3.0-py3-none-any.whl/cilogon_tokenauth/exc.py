from __future__ import unicode_literals
import logging
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework import status

log = logging.getLogger(__name__)


class TokenInactive(AuthenticationFailed):
    pass


class TokenExpired(TokenInactive):
    pass
