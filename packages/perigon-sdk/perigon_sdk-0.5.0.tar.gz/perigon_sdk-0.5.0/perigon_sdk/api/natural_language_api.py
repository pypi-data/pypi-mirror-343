from typing import Any, Dict, Optional

from perigon_sdk.api_client import ApiClient
from perigon_sdk.models.article_search_params import ArticleSearchParams
from perigon_sdk.models.search_result import SearchResult


class NaturalLanguageApi:
    """"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()

    # ----------------- vector_search_articles (sync) ----------------- #
    def vector_search_articles(
        self, article_search_params: ArticleSearchParams
    ) -> SearchResult:
        """Vector"""
        path = "/v1/vector/news/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}

        resp = self.api_client.request(
            "POST", path, params=params, json=article_search_params
        )
        resp.raise_for_status()

        return SearchResult.model_validate(resp.text)

    # ---------------- vector_search_articles_async ------------------- #
    async def vector_search_articles_async(
        self, article_search_params: ArticleSearchParams
    ) -> SearchResult:
        """Vector (async)"""
        path = "/v1/vector/news/all"

        params: Dict[str, Any] = {}

        resp = await self.api_client.request_async(
            "POST", path, params=params, json=article_search_params
        )
        resp.raise_for_status()

        return SearchResult.model_validate(resp.text)
