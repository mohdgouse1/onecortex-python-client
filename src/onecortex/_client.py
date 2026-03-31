from ._http import HttpClient
from .auth import AuthClient
from .vector import VectorClient


class Onecortex:
    """Unified OneCortex client. Access services via namespaces: .vector, .auth"""

    def __init__(self, url: str, api_key: str):
        self._http = HttpClient(api_key=api_key, url=url)
        self.vector = VectorClient(http=self._http)
        self.auth = AuthClient(http=self._http)
