from .._http import HttpClient


class AuthClient:
    """Stub for future auth service integration."""

    def __init__(self, http: HttpClient, base_path: str = "/v1/auth"):
        self._http = http
        self._base_path = base_path
