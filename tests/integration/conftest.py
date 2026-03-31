import os

import pytest

from onecortex import Onecortex
from onecortex.vector import VectorClient

HOST = os.environ.get("ONECORTEX_HOST", "http://localhost:8080")
API_KEY = os.environ.get("ONECORTEX_API_KEY", "")
# In production the gateway adds /v1/vector prefix. In local dev the server
# exposes routes directly at root, so we override base_path to "".
BASE_PATH = os.environ.get("ONECORTEX_BASE_PATH", "")


@pytest.fixture
def oc_client():
    client = Onecortex(url=HOST, api_key=API_KEY)
    client.vector = VectorClient(http=client._http, base_path=BASE_PATH)
    return client
