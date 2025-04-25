import logging
import time
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

log = logging.getLogger(__name__)


class CachedToken(models.Model):

    id = models.CharField(max_length=256, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scope = models.CharField(max_length=128)
    issued_at = models.FloatField()
    expires_at = models.FloatField()
    last_introspection = models.FloatField()

    @property
    def introspection_cache_expired(self):
        """Introspection cache is the length of time we can trust the token id
        between user invocations of this API. This is a balance of security
        and not overloading the CILogon servers with requests."""
        last_use = time.time() - self.last_introspection
        log.debug(f'Last use was {last_use}')
        limit = settings.TOKENAUTH_INTROSPECTION_CACHE_EXPIRATION
        return last_use > int(limit)

    @property
    def token_expired(self):
        log.debug(f'Token expires in {self.expires_at - time.time()} secs')
        return time.time() > self.expires_at

    def reset_introspection_cache(self):
        self.last_introspection = time.time()
        self.save()

    def delete_cached_token(self):
        log.debug(f'Removing token for user {self.user} from cache')
        self.delete()

    @classmethod
    def from_user(cls, user):
        tokens = [t for t in cls.objects.filter(user=user)
                  if not t.token_expired]
        if tokens:
            return tokens[0]
