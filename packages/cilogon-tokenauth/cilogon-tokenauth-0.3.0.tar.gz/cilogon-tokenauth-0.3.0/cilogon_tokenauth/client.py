from requests_oauth2client import OAuth2Client, BearerToken, Endpoints
from typing import Any


class CiLogonClient(OAuth2Client):

    def userinfo(self, access_token: BearerToken | str) -> Any:
        """Call the UserInfo endpoint.

        This sends a request to the UserInfo endpoint, with the specified
        access_token, and returns
        the parsed result.

        Args:
            access_token: the access token to use

        Returns:
            the [Response][requests.Response] returned by the userinfo
            endpoint.

        """
        if isinstance(access_token, str):
            access_token = BearerToken(access_token)
        return self._request(
            Endpoints.USER_INFO,
            auth=access_token,
            method="GET",
            on_success=self.parse_userinfo_response,
            on_failure=self.on_userinfo_error,
        )
