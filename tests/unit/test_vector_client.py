import httpx
import pytest
import respx

from onecortex import Onecortex
from onecortex.exceptions import NotFoundError

BASE = "http://test-server:8080"
VP = "/v1/vector"

INDEX_RESPONSE = {
    "name": "test-idx",
    "dimension": 3,
    "metric": "cosine",
    "status": {"ready": True, "state": "Ready"},
    "host": "test-server:8080",
}


@respx.mock
def test_create_index():
    respx.post(f"{BASE}{VP}/indexes").mock(return_value=httpx.Response(200, json=INDEX_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    idx = pc.vector.create_index(name="test-idx", dimension=3, metric="cosine")
    assert idx.name == "test-idx"
    assert idx.dimension == 3


@respx.mock
def test_create_index_ignores_spec():
    respx.post(f"{BASE}{VP}/indexes").mock(return_value=httpx.Response(200, json=INDEX_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    # spec= is an unknown arg — must not raise
    idx = pc.vector.create_index(
        name="test-idx",
        dimension=3,
        spec={"serverless": {"cloud": "aws", "region": "us-east-1"}},
    )
    assert idx.name == "test-idx"


@respx.mock
def test_describe_index():
    respx.get(f"{BASE}{VP}/indexes/test-idx").mock(return_value=httpx.Response(200, json=INDEX_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    idx = pc.vector.describe_index("test-idx")
    assert idx.metric == "cosine"


@respx.mock
def test_list_indexes():
    respx.get(f"{BASE}{VP}/indexes").mock(return_value=httpx.Response(200, json={"indexes": [INDEX_RESPONSE]}))
    pc = Onecortex(url=BASE, api_key="key123")
    indexes = pc.vector.list_indexes()
    assert len(indexes) == 1
    assert indexes[0].name == "test-idx"


@respx.mock
def test_delete_index():
    respx.delete(f"{BASE}{VP}/indexes/test-idx").mock(return_value=httpx.Response(202))
    pc = Onecortex(url=BASE, api_key="key123")
    pc.vector.delete_index("test-idx")  # should not raise


@respx.mock
def test_has_index_true():
    respx.get(f"{BASE}{VP}/indexes/test-idx").mock(return_value=httpx.Response(200, json=INDEX_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    assert pc.vector.has_index("test-idx") is True


@respx.mock
def test_has_index_false():
    respx.get(f"{BASE}{VP}/indexes/missing").mock(
        return_value=httpx.Response(404, json={"error": {"code": "NOT_FOUND", "message": "not found"}})
    )
    pc = Onecortex(url=BASE, api_key="key123")
    assert pc.vector.has_index("missing") is False


@respx.mock
def test_configure_index():
    respx.patch(f"{BASE}{VP}/indexes/test-idx").mock(return_value=httpx.Response(200, json=INDEX_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    result = pc.vector.configure_index("test-idx", tags={"env": "prod"})
    assert result.name == "test-idx"


@respx.mock
def test_not_found_raises():
    respx.get(f"{BASE}{VP}/indexes/missing").mock(
        return_value=httpx.Response(404, json={"error": {"code": "NOT_FOUND", "message": "not found"}})
    )
    pc = Onecortex(url=BASE, api_key="key123")
    with pytest.raises(NotFoundError):
        pc.vector.describe_index("missing")


# ── Alias tests ──────────────────────────────────────────────────────────────

ALIAS_RESPONSE = {"alias": "prod", "indexName": "my-index-v2"}
ALIAS_LIST_RESPONSE = {
    "aliases": [
        {"alias": "prod", "indexName": "my-index-v2"},
        {"alias": "staging", "indexName": "my-index-v1"},
    ]
}


@respx.mock
def test_create_alias():
    import json

    route = respx.post(f"{BASE}{VP}/aliases").mock(return_value=httpx.Response(201, json=ALIAS_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    result = pc.vector.create_alias(alias="prod", index_name="my-index-v2")
    assert result.alias == "prod"
    assert result.index_name == "my-index-v2"
    body = json.loads(route.calls[0].request.content)
    assert body == {"alias": "prod", "indexName": "my-index-v2"}


@respx.mock
def test_list_aliases():
    respx.get(f"{BASE}{VP}/aliases").mock(return_value=httpx.Response(200, json=ALIAS_LIST_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    result = pc.vector.list_aliases()
    assert len(result.aliases) == 2
    assert result.aliases[0].alias == "prod"
    assert result.aliases[1].index_name == "my-index-v1"


@respx.mock
def test_describe_alias():
    respx.get(f"{BASE}{VP}/aliases/prod").mock(return_value=httpx.Response(200, json=ALIAS_RESPONSE))
    pc = Onecortex(url=BASE, api_key="key123")
    result = pc.vector.describe_alias("prod")
    assert result.alias == "prod"
    assert result.index_name == "my-index-v2"


@respx.mock
def test_delete_alias():
    respx.delete(f"{BASE}{VP}/aliases/prod").mock(return_value=httpx.Response(204))
    pc = Onecortex(url=BASE, api_key="key123")
    pc.vector.delete_alias("prod")  # should not raise
