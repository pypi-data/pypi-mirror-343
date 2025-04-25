from __future__ import unicode_literals
import logging
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from allauth.socialaccount.models import SocialAccount
from requests_oauth2client import ClientSecretBasic
from cilogon_tokenauth.client import CiLogonClient

import cilogon_tokenauth
import cilogon_tokenauth.exc
import cilogon_tokenauth.models
import cilogon_tokenauth.client


log = logging.getLogger(__name__)


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Specify which permissions a valid ACCESS user should have. We currently
    don't have any reason to restrict them from calling any views as long as
    they are a valid user."""

    def has_permission(self, request, view):
        """Only authenticated ACCESS users have access to write. Anon users
        can only read and list."""
        return request.user.is_authenticated or \
            request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return obj.user == request.user


def get_cilogon_auth_client():
    return CiLogonClient.from_discovery_endpoint(
        "https://cilogon.org/.well-known/openid-configuration",
        auth=ClientSecretBasic(settings.CILOGON_CLIENT_KEY, settings.CILOGON_CLIENT_SECRET),
    )


def get_or_create_user(user_details):
    """
    Get a Django User with a matching CILogon (sub) or create
    one if it does not exist. The SocialSccount user instance is
    created whether or not a user logged in via social auth or
    simply passed a token into the API. This allows the user to
    do either in either order.
    token_details -- Token response details from introspecting a
    CILogon access Token
    """
    try:
        return SocialAccount.objects.get(uid=user_details['sub']).user
    except SocialAccount.DoesNotExist:
        first_name = user_details['given_name']
        last_name = user_details['family_name']
        user = User(username=user_details['preferred_username'],
                    first_name=first_name, last_name=last_name,
                    email=user_details['email'])
        user.save()
        usa = SocialAccount(user=user, provider='CILogon',
                            uid=user_details['sub'])
        usa.save()
        return user


def introspect_cilogon_token(raw_token):
    """Introspect the CILogon token to check if it is active.

    Introspections are cached for a short duration set by
    settings.TOKENAUTH_INTROSPECTION_CACHE_EXPIRATION. If many introspections
    (api calls) happen within the cache window, the last introspection will
    be trusted and the CILogon intropection call will be skipped.

    If the token is revoked by CILogon, an AuthenticationFailed exception
    will be raised.

    A valid token for first time use will result in user creation based on the
    uuid 'sub' field on the token data. """
    log.debug(f'Received Token: {raw_token}')
    try:
        ctoken = cilogon_tokenauth.models.CachedToken.objects.get(pk=raw_token)
        if not ctoken.introspection_cache_expired:
            return ctoken
        if ctoken.token_expired:
            user = ctoken.user
            # If the token is expired, delete it from the cache
            # ctoken.delete_cached_token()
            raise cilogon_tokenauth.exc.TokenExpired(f'Token expired for user {user}')
    except cilogon_tokenauth.models.CachedToken.DoesNotExist:
        ctoken = None
    try:
        log.debug('Cache Exp or new token, introspecting...')
        token_details, user_details = cilogon_introspect(raw_token)
        log.debug(f'{token_details}')
        if token_details['active'] is False:
            log.info('Auth failed, token is not active.')
            raise cilogon_tokenauth.exc.TokenInactive(
                    'Introspection revealed inactive '
                    'token.')
        if not ctoken:
            user = get_or_create_user(user_details)
            log.warning(f'Creating new Cached Token for {user}')
            # CILogon  has a bug where the "exp" value is incorrect
            # So, for now, we're using "nbf"+900 to be the expiration
            # value, since lifetime seems to always be 900 seconds`
            ctoken = cilogon_tokenauth.models.CachedToken(
                id=raw_token, user=user,
                # expires_at=token_details['exp'],
                expires_at=token_details['nbf']+900,
                issued_at=token_details['iat'],
                scope=token_details['scope']
            )
        ctoken.reset_introspection_cache()
        ctoken.save()
        log.debug(f'Auth Successful for user {ctoken.user}')
        return ctoken
    except Exception as e:
        log.exception(e)
        raise AuthenticationFailed('Encountered an error in CILogon')


def cilogon_introspect(raw_token):
    try:
        # In general, it's a bad idea to put these in your logs, so
        # only uncomment to debug installation, then recomment
        # log.debug(f'{settings.CILOGON_CLIENT_KEY} secret {settings.CILOGON_CLIENT_SECRET}')
        client = get_cilogon_auth_client()
        log.debug('Cache Exp or new token, introspecting...')
        token_details = client.introspect_token(raw_token)
        log.debug(f'Token details: {token_details}')
        log.debug(f'Is Token active: {token_details["active"]}')
        if token_details['active'] is False:
            raise cilogon_tokenauth.exc.TokenInactive(
                                        'Introspection revealed inactive '
                                        'token.')
        user_details = client.userinfo(raw_token)
        log.debug(f'User Details: {user_details}')
    except Exception as e:
        log.exception(e)
        raise AuthenticationFailed('Encountered an error with CILogon '
                                   f'{raw_token}{token_details}')
    return token_details, user_details


class CITokenAuthentication(TokenAuthentication):
    """
    Simple token based authentication for CILogon  Auth.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer".  For example:
        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a

    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py#L145 # noqa
    """

    keyword = 'Bearer'

    def authenticate_credentials(self, raw_token):
        log.debug('Authorizing API Client...')
        cached_token = introspect_cilogon_token(raw_token)
        log.info(f'Authorized API Client {cached_token.user}')
        return cached_token.user, cached_token
