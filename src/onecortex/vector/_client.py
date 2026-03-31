from typing import Any

from .._http import HttpClient
from ._index import Index
from .models import AliasDescription, AliasListResult, IndexDescription


class VectorClient:
    """
    Control-plane client for vector index management.
    Access via client.vector (e.g., client.vector.create_index(...)).
    """

    def __init__(self, http: HttpClient, base_path: str = "/v1/vector"):
        self._http = http
        self._base_path = base_path

    def create_index(
        self,
        name: str,
        dimension: int,
        metric: str = "cosine",
        bm25_enabled: bool = False,
        deletion_protection: str | None = None,
        tags: dict | None = None,
        **kwargs: Any,  # absorb unknown args like spec= without erroring
    ) -> IndexDescription:
        """Create a new vector index."""
        body: dict = {"name": name, "dimension": dimension, "metric": metric}
        if bm25_enabled:
            body["bm25_enabled"] = True
        if deletion_protection:
            body["deletion_protection"] = deletion_protection
        if tags:
            body["tags"] = tags
        response = self._http.post(f"{self._base_path}/indexes", json=body)
        return IndexDescription.model_validate(response.json())

    def describe_index(self, name: str) -> IndexDescription:
        response = self._http.get(f"{self._base_path}/indexes/{name}")
        return IndexDescription.model_validate(response.json())

    def list_indexes(self) -> list[IndexDescription]:
        response = self._http.get(f"{self._base_path}/indexes")
        return [IndexDescription.model_validate(i) for i in response.json().get("indexes", [])]

    def delete_index(self, name: str) -> None:
        self._http.delete(f"{self._base_path}/indexes/{name}")

    def configure_index(
        self,
        name: str,
        deletion_protection: str | None = None,
        tags: dict | None = None,
        **kwargs: Any,
    ) -> IndexDescription:
        body: dict = {}
        if deletion_protection is not None:
            body["deletion_protection"] = deletion_protection
        if tags is not None:
            body["tags"] = tags
        response = self._http.patch(f"{self._base_path}/indexes/{name}", json=body)
        return IndexDescription.model_validate(response.json())

    def has_index(self, name: str) -> bool:
        try:
            self.describe_index(name)
            return True
        except Exception:
            return False

    def index(self, name: str) -> Index:
        """Get a handle to a specific index for data-plane operations."""
        return Index(http=self._http, base_path=self._base_path, name=name)

    # ── Aliases ──────────────────────────────────────────────────────────────

    def create_alias(self, alias: str, index_name: str) -> AliasDescription:
        """Create or update an alias pointing to index_name (upsert semantics)."""
        response = self._http.post(
            f"{self._base_path}/aliases",
            json={"alias": alias, "indexName": index_name},
        )
        return AliasDescription.model_validate(response.json())

    def describe_alias(self, alias: str) -> AliasDescription:
        """Fetch details for a single alias."""
        response = self._http.get(f"{self._base_path}/aliases/{alias}")
        return AliasDescription.model_validate(response.json())

    def list_aliases(self) -> AliasListResult:
        """List all aliases in the account."""
        response = self._http.get(f"{self._base_path}/aliases")
        return AliasListResult.model_validate(response.json())

    def delete_alias(self, alias: str) -> None:
        """Delete an alias. Raises NotFoundError if it does not exist."""
        self._http.delete(f"{self._base_path}/aliases/{alias}")
