from onecortex import Onecortex
from onecortex.auth import AuthClient
from onecortex.vector import VectorClient

BASE = "http://test-server:8080"


def test_onecortex_has_vector_namespace():
    client = Onecortex(url=BASE, api_key="key123")
    assert isinstance(client.vector, VectorClient)


def test_onecortex_has_auth_namespace():
    client = Onecortex(url=BASE, api_key="key123")
    assert isinstance(client.auth, AuthClient)
