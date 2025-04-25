from typing import Any, Dict, Optional, Union

from perigon_sdk.api_client import ApiClient
from perigon_sdk.models.journalist import Journalist
from perigon_sdk.models.standard_search_result import StandardSearchResult
from perigon_sdk.models.table_search_result import TableSearchResult
from pydantic import Field, StrictStr
from typing_extensions import Annotated


class SupplementalEndpointsApi:
    """"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        self.api_client = api_client or ApiClient()

    # ----------------- get_journalist_by_id (sync) ----------------- #
    def get_journalist_by_id(self, id: str) -> Journalist:
        """Journalists ID"""
        path = "/v1/journalists/{id}"
        path = path.replace("{$id}", str(id))

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()

        return Journalist.model_validate(resp.text)

    # ---------------- get_journalist_by_id_async ------------------- #
    async def get_journalist_by_id_async(self, id: str) -> Journalist:
        """Journalists ID (async)"""
        path = "/v1/journalists/{id}"
        path = path.replace("{$id}", str(id))

        params: Dict[str, Any] = {}

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()

        return Journalist.model_validate(resp.text)

    # ----------------- search_companies (sync) ----------------- #
    def search_companies(
        self,
        id: Optional[str] = None,
        symbol: Optional[str] = None,
        domain: Optional[str] = None,
        country: Optional[str] = None,
        exchange: Optional[str] = None,
        num_employees_from: Optional[str] = None,
        num_employees_to: Optional[str] = None,
        ipo_from: Optional[str] = None,
        ipo_to: Optional[str] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        sector: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
    ) -> StandardSearchResult:
        """Companies"""
        path = "/v1/companies/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if symbol is not None:
            params["symbol"] = symbol
        if domain is not None:
            params["domain"] = domain
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        if num_employees_from is not None:
            params["numEmployeesFrom"] = num_employees_from
        if num_employees_to is not None:
            params["numEmployeesTo"] = num_employees_to
        if ipo_from is not None:
            params["ipoFrom"] = ipo_from
        if ipo_to is not None:
            params["ipoTo"] = ipo_to
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if industry is not None:
            params["industry"] = industry
        if sector is not None:
            params["sector"] = sector
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ---------------- search_companies_async ------------------- #
    async def search_companies_async(
        self,
        id: Optional[str] = None,
        symbol: Optional[str] = None,
        domain: Optional[str] = None,
        country: Optional[str] = None,
        exchange: Optional[str] = None,
        num_employees_from: Optional[str] = None,
        num_employees_to: Optional[str] = None,
        ipo_from: Optional[str] = None,
        ipo_to: Optional[str] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        industry: Optional[str] = None,
        sector: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
    ) -> StandardSearchResult:
        """Companies (async)"""
        path = "/v1/companies/all"

        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if symbol is not None:
            params["symbol"] = symbol
        if domain is not None:
            params["domain"] = domain
        if country is not None:
            params["country"] = country
        if exchange is not None:
            params["exchange"] = exchange
        if num_employees_from is not None:
            params["numEmployeesFrom"] = num_employees_from
        if num_employees_to is not None:
            params["numEmployeesTo"] = num_employees_to
        if ipo_from is not None:
            params["ipoFrom"] = ipo_from
        if ipo_to is not None:
            params["ipoTo"] = ipo_to
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if industry is not None:
            params["industry"] = industry
        if sector is not None:
            params["sector"] = sector
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ----------------- search_journalists1 (sync) ----------------- #
    def search_journalists1(
        self,
        id: Optional[str] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        twitter: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
        source: Optional[str] = None,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        label: Optional[str] = None,
        min_monthly_posts: Optional[str] = None,
        max_monthly_posts: Optional[str] = None,
        country: Optional[str] = None,
        updated_at_from: Optional[str] = None,
        updated_at_to: Optional[str] = None,
        show_num_results: Optional[str] = None,
    ) -> StandardSearchResult:
        """Journalists"""
        path = "/v1/journalists/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if twitter is not None:
            params["twitter"] = twitter
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page
        if source is not None:
            params["source"] = source
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if label is not None:
            params["label"] = label
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if updated_at_from is not None:
            params["updatedAtFrom"] = updated_at_from
        if updated_at_to is not None:
            params["updatedAtTo"] = updated_at_to
        if show_num_results is not None:
            params["showNumResults"] = show_num_results

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ---------------- search_journalists1_async ------------------- #
    async def search_journalists1_async(
        self,
        id: Optional[str] = None,
        q: Optional[str] = None,
        name: Optional[str] = None,
        twitter: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
        source: Optional[str] = None,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        label: Optional[str] = None,
        min_monthly_posts: Optional[str] = None,
        max_monthly_posts: Optional[str] = None,
        country: Optional[str] = None,
        updated_at_from: Optional[str] = None,
        updated_at_to: Optional[str] = None,
        show_num_results: Optional[str] = None,
    ) -> StandardSearchResult:
        """Journalists (async)"""
        path = "/v1/journalists/all"

        params: Dict[str, Any] = {}
        if id is not None:
            params["id"] = id
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if twitter is not None:
            params["twitter"] = twitter
        if size is not None:
            params["size"] = size
        if page is not None:
            params["page"] = page
        if source is not None:
            params["source"] = source
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if label is not None:
            params["label"] = label
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if updated_at_from is not None:
            params["updatedAtFrom"] = updated_at_from
        if updated_at_to is not None:
            params["updatedAtTo"] = updated_at_to
        if show_num_results is not None:
            params["showNumResults"] = show_num_results

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ----------------- search_people (sync) ----------------- #
    def search_people(
        self,
        name: Optional[str] = None,
        wikidata_id: Optional[str] = None,
        occupation_id: Optional[str] = None,
        occupation_label: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> StandardSearchResult:
        """People"""
        path = "/v1/people/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if wikidata_id is not None:
            params["wikidataId"] = wikidata_id
        if occupation_id is not None:
            params["occupationId"] = occupation_id
        if occupation_label is not None:
            params["occupationLabel"] = occupation_label
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ---------------- search_people_async ------------------- #
    async def search_people_async(
        self,
        name: Optional[str] = None,
        wikidata_id: Optional[str] = None,
        occupation_id: Optional[str] = None,
        occupation_label: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> StandardSearchResult:
        """People (async)"""
        path = "/v1/people/all"

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if wikidata_id is not None:
            params["wikidataId"] = wikidata_id
        if occupation_id is not None:
            params["occupationId"] = occupation_id
        if occupation_label is not None:
            params["occupationLabel"] = occupation_label
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ----------------- search_sources (sync) ----------------- #
    def search_sources(
        self,
        domain: Optional[str] = None,
        name: Optional[str] = None,
        source_group: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        min_monthly_visits: Optional[str] = None,
        max_monthly_visits: Optional[str] = None,
        min_monthly_posts: Optional[str] = None,
        max_monthly_posts: Optional[str] = None,
        country: Optional[str] = None,
        source_country: Optional[str] = None,
        source_state: Optional[str] = None,
        source_county: Optional[str] = None,
        source_city: Optional[str] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        category: Optional[str] = None,
        topic: Optional[str] = None,
        label: Optional[str] = None,
        paywall: Optional[str] = None,
        show_subdomains: Optional[str] = None,
        show_num_results: Optional[str] = None,
    ) -> StandardSearchResult:
        """Sources"""
        path = "/v1/sources/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if domain is not None:
            params["domain"] = domain
        if name is not None:
            params["name"] = name
        if source_group is not None:
            params["sourceGroup"] = source_group
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if min_monthly_visits is not None:
            params["minMonthlyVisits"] = min_monthly_visits
        if max_monthly_visits is not None:
            params["maxMonthlyVisits"] = max_monthly_visits
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if category is not None:
            params["category"] = category
        if topic is not None:
            params["topic"] = topic
        if label is not None:
            params["label"] = label
        if paywall is not None:
            params["paywall"] = paywall
        if show_subdomains is not None:
            params["showSubdomains"] = show_subdomains
        if show_num_results is not None:
            params["showNumResults"] = show_num_results

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ---------------- search_sources_async ------------------- #
    async def search_sources_async(
        self,
        domain: Optional[str] = None,
        name: Optional[str] = None,
        source_group: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        min_monthly_visits: Optional[str] = None,
        max_monthly_visits: Optional[str] = None,
        min_monthly_posts: Optional[str] = None,
        max_monthly_posts: Optional[str] = None,
        country: Optional[str] = None,
        source_country: Optional[str] = None,
        source_state: Optional[str] = None,
        source_county: Optional[str] = None,
        source_city: Optional[str] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        category: Optional[str] = None,
        topic: Optional[str] = None,
        label: Optional[str] = None,
        paywall: Optional[str] = None,
        show_subdomains: Optional[str] = None,
        show_num_results: Optional[str] = None,
    ) -> StandardSearchResult:
        """Sources (async)"""
        path = "/v1/sources/all"

        params: Dict[str, Any] = {}
        if domain is not None:
            params["domain"] = domain
        if name is not None:
            params["name"] = name
        if source_group is not None:
            params["sourceGroup"] = source_group
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if min_monthly_visits is not None:
            params["minMonthlyVisits"] = min_monthly_visits
        if max_monthly_visits is not None:
            params["maxMonthlyVisits"] = max_monthly_visits
        if min_monthly_posts is not None:
            params["minMonthlyPosts"] = min_monthly_posts
        if max_monthly_posts is not None:
            params["maxMonthlyPosts"] = max_monthly_posts
        if country is not None:
            params["country"] = country
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if category is not None:
            params["category"] = category
        if topic is not None:
            params["topic"] = topic
        if label is not None:
            params["label"] = label
        if paywall is not None:
            params["paywall"] = paywall
        if show_subdomains is not None:
            params["showSubdomains"] = show_subdomains
        if show_num_results is not None:
            params["showNumResults"] = show_num_results

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()

        return StandardSearchResult.model_validate(resp.text)

    # ----------------- search_topics (sync) ----------------- #
    def search_topics(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> TableSearchResult:
        """Topics"""
        path = "/v1/topics/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if category is not None:
            params["category"] = category
        if subcategory is not None:
            params["subcategory"] = subcategory
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()

        return TableSearchResult.model_validate(resp.text)

    # ---------------- search_topics_async ------------------- #
    async def search_topics_async(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> TableSearchResult:
        """Topics (async)"""
        path = "/v1/topics/all"

        params: Dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if category is not None:
            params["category"] = category
        if subcategory is not None:
            params["subcategory"] = subcategory
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()

        return TableSearchResult.model_validate(resp.text)
