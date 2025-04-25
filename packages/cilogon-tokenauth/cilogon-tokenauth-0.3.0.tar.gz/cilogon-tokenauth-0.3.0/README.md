cilogon-tokenauth is a package that implements the Django Rest Framework
TokenAuthentication, using CILogon.

One can submit an API request with an "Authentication: Bearer <token>" 
line in the header, and the cilogon-tokenauth package will introspect the
bearer token with CILogon, match it to a SocialAccount user by the "sub" 
value from the CILogon userinfo endpoint (or create a user if one does not already exist).

So as not to overtax the CILogon introspection endpoint, should many API requests come through at the same time, the token's introspection information is cached for a settable amount of time.  Set the value in seconds in settings.py as TOKENAUTH_INTROSPECTION_CACHE_EXPIRATION.

You must register a CILogon OIDC client at registry.access-ci.org.
Your values for Client ID and Secret must then be put in settings as CILOGON_CLIENT_KEY and CILOGON_CLIENT_SECRET

Settings:
CILOGON_CLIENT_KEY
CILOGON_CLIENT_SECRET
TOKENAUTH_INTROSPECTION_CACHE_EXPIRATION

