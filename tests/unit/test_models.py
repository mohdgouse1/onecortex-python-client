from onecortex.vector.models import (
    AliasDescription,
    AliasListResult,
    BatchQueryResult,
    FetchResult,
    GroupedQueryResult,
    IndexDescription,
    IndexStats,
    ListResult,
    QueryResult,
    RecommendResult,
    ScrollResult,
    UpsertResult,
)


def test_index_description_defaults():
    data = {
        "name": "my-index",
        "dimension": 1536,
        "metric": "cosine",
        "status": {"ready": True, "state": "Ready"},
        "host": "localhost:8080",
    }
    idx = IndexDescription.model_validate(data)
    assert idx.name == "my-index"
    assert idx.vector_type == "dense"
    assert idx.spec == {}
    assert idx.tags is None


def test_upsert_result_alias():
    result = UpsertResult.model_validate({"upsertedCount": 5})
    assert result.upserted_count == 5


def test_upsert_result_by_name():
    result = UpsertResult.model_validate({"upserted_count": 3})
    assert result.upserted_count == 3


def test_query_result():
    data = {
        "matches": [
            {"id": "v1", "score": 0.95},
            {"id": "v2", "score": 0.80, "metadata": {"key": "val"}},
        ],
        "namespace": "ns1",
    }
    result = QueryResult.model_validate(data)
    assert len(result.matches) == 2
    assert result.matches[0].id == "v1"
    assert result.matches[1].metadata == {"key": "val"}
    assert result.results == []


def test_index_stats_aliases():
    data = {
        "namespaces": {"": {"vectorCount": 10}},
        "dimension": 1536,
        "indexFullness": 0.01,
        "totalVectorCount": 10,
    }
    stats = IndexStats.model_validate(data)
    assert stats.total_vector_count == 10
    assert stats.index_fullness == 0.01
    assert stats.namespaces[""].vector_count == 10


def test_fetch_result():
    data = {
        "vectors": {"v1": {"id": "v1", "values": [0.1, 0.2], "metadata": {}}},
        "namespace": "",
    }
    result = FetchResult.model_validate(data)
    assert "v1" in result.vectors


def test_list_result_no_pagination():
    data = {
        "vectors": [{"id": "v1"}, {"id": "v2"}],
        "namespace": "",
    }
    result = ListResult.model_validate(data)
    assert len(result.vectors) == 2
    assert result.pagination is None


# ── New model tests ──────────────────────────────────────────────────────────


def test_scroll_result_with_cursor():
    data = {
        "vectors": [{"id": "v1", "values": [1.0, 0.0, 0.0]}],
        "namespace": "",
        "nextCursor": "abc123",
    }
    result = ScrollResult.model_validate(data)
    assert len(result.vectors) == 1
    assert result.vectors[0].id == "v1"
    assert result.next_cursor == "abc123"  # camelCase alias resolved


def test_scroll_result_no_cursor():
    data = {
        "vectors": [{"id": "v2"}],
        "namespace": "",
        # nextCursor intentionally absent (last page)
    }
    result = ScrollResult.model_validate(data)
    assert result.next_cursor is None


def test_batch_query_result():
    data = {
        "results": [
            {"matches": [{"id": "v1", "score": 0.9}], "namespace": ""},
            {"matches": [{"id": "v2", "score": 0.8}], "namespace": ""},
        ]
    }
    result = BatchQueryResult.model_validate(data)
    assert len(result.results) == 2
    assert result.results[0].matches[0].id == "v1"
    assert result.results[1].matches[0].id == "v2"


def test_alias_description_alias():
    data = {"alias": "prod", "indexName": "my-index-v2"}
    desc = AliasDescription.model_validate(data)
    assert desc.alias == "prod"
    assert desc.index_name == "my-index-v2"  # camelCase alias resolved


def test_alias_list_result():
    data = {
        "aliases": [
            {"alias": "prod", "indexName": "idx-1"},
            {"alias": "staging", "indexName": "idx-2"},
        ]
    }
    result = AliasListResult.model_validate(data)
    assert len(result.aliases) == 2
    assert result.aliases[0].index_name == "idx-1"


def test_recommend_result():
    data = {
        "matches": [{"id": "v2", "score": 0.85}, {"id": "v3", "score": 0.70}],
        "namespace": "",
    }
    result = RecommendResult.model_validate(data)
    assert len(result.matches) == 2
    assert result.matches[0].id == "v2"
    assert result.namespace == ""


def test_grouped_query_result():
    # GroupedQueryResult is constructed in code (not via model_validate from JSON)
    from onecortex.vector.models import GroupedMatch, Match

    groups = [
        GroupedMatch(group="news-1", matches=[Match(id="n1", score=0.9)]),
        GroupedMatch(group="sports-1", matches=[Match(id="s1", score=0.7)]),
    ]
    result = GroupedQueryResult(groups=groups, namespace="")
    assert len(result.groups) == 2
    assert result.groups[0].group == "news-1"
    assert result.groups[0].matches[0].id == "n1"
