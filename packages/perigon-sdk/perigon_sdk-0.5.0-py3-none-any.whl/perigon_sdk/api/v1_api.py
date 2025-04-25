from typing import Any, Dict, Optional, Union

from perigon_sdk.api_client import ApiClient
from perigon_sdk.models.article_search_params import ArticleSearchParams
from perigon_sdk.models.journalist import Journalist
from perigon_sdk.models.query_search_result import QuerySearchResult
from perigon_sdk.models.search_result import SearchResult
from perigon_sdk.models.standard_search_result import StandardSearchResult
from perigon_sdk.models.table_search_result import TableSearchResult
from pydantic import Field, StrictBool, StrictStr
from typing_extensions import Annotated


class V1Api:
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
        return Journalist.model_validate(resp.json())

    # ---------------- get_journalist_by_id_async ------------------- #
    async def get_journalist_by_id_async(self, id: str) -> Journalist:
        """Journalists ID (async)"""
        path = "/v1/journalists/{id}"
        path = path.replace("{$id}", str(id))

        params: Dict[str, Any] = {}

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return Journalist.model_validate(resp.json())

    # ----------------- search_articles (sync) ----------------- #
    def search_articles(
        self,
        q: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        article_id: Optional[str] = None,
        cluster_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[str] = None,
        to: Optional[str] = None,
        add_date_from: Optional[str] = None,
        add_date_to: Optional[str] = None,
        refresh_date_from: Optional[str] = None,
        refresh_date_to: Optional[str] = None,
        medium: Optional[str] = None,
        source: Optional[str] = None,
        source_group: Optional[str] = None,
        exclude_source_group: Optional[str] = None,
        exclude_source: Optional[str] = None,
        paywall: Optional[str] = None,
        byline: Optional[str] = None,
        author: Optional[str] = None,
        exclude_author: Optional[str] = None,
        journalist_id: Optional[str] = None,
        exclude_journalist_id: Optional[str] = None,
        language: Optional[str] = None,
        exclude_language: Optional[str] = None,
        search_translation: Optional[str] = None,
        label: Optional[str] = None,
        exclude_label: Optional[str] = None,
        category: Optional[str] = None,
        exclude_category: Optional[str] = None,
        topic: Optional[str] = None,
        exclude_topic: Optional[str] = None,
        link_to: Optional[str] = None,
        show_reprints: Optional[str] = None,
        reprint_group_id: Optional[str] = None,
        city: Optional[str] = None,
        exclude_city: Optional[str] = None,
        area: Optional[str] = None,
        state: Optional[str] = None,
        exclude_state: Optional[str] = None,
        county: Optional[str] = None,
        exclude_county: Optional[str] = None,
        locations_country: Optional[str] = None,
        country: Optional[str] = None,
        exclude_locations_country: Optional[str] = None,
        location: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance: Optional[float] = None,
        source_city: Optional[str] = None,
        source_county: Optional[str] = None,
        source_country: Optional[str] = None,
        source_state: Optional[str] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        person_wikidata_id: Optional[str] = None,
        exclude_person_wikidata_id: Optional[str] = None,
        person_name: Optional[str] = None,
        exclude_person_name: Optional[str] = None,
        company_id: Optional[str] = None,
        exclude_company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        exclude_company_domain: Optional[str] = None,
        company_symbol: Optional[str] = None,
        exclude_company_symbol: Optional[str] = None,
        show_num_results: Optional[str] = None,
        positive_sentiment_from: Optional[str] = None,
        positive_sentiment_to: Optional[str] = None,
        neutral_sentiment_from: Optional[str] = None,
        neutral_sentiment_to: Optional[str] = None,
        negative_sentiment_from: Optional[str] = None,
        negative_sentiment_to: Optional[str] = None,
        taxonomy: Optional[str] = None,
        prefix_taxonomy: Optional[str] = None,
    ) -> QuerySearchResult:
        """Articles"""
        path = "/v1/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if desc is not None:
            params["desc"] = desc
        if content is not None:
            params["content"] = content
        if url is not None:
            params["url"] = url
        if article_id is not None:
            params["articleId"] = article_id
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if add_date_from is not None:
            params["addDateFrom"] = add_date_from
        if add_date_to is not None:
            params["addDateTo"] = add_date_to
        if refresh_date_from is not None:
            params["refreshDateFrom"] = refresh_date_from
        if refresh_date_to is not None:
            params["refreshDateTo"] = refresh_date_to
        if medium is not None:
            params["medium"] = medium
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if exclude_source_group is not None:
            params["excludeSourceGroup"] = exclude_source_group
        if exclude_source is not None:
            params["excludeSource"] = exclude_source
        if paywall is not None:
            params["paywall"] = paywall
        if byline is not None:
            params["byline"] = byline
        if author is not None:
            params["author"] = author
        if exclude_author is not None:
            params["excludeAuthor"] = exclude_author
        if journalist_id is not None:
            params["journalistId"] = journalist_id
        if exclude_journalist_id is not None:
            params["excludeJournalistId"] = exclude_journalist_id
        if language is not None:
            params["language"] = language
        if exclude_language is not None:
            params["excludeLanguage"] = exclude_language
        if search_translation is not None:
            params["searchTranslation"] = search_translation
        if label is not None:
            params["label"] = label
        if exclude_label is not None:
            params["excludeLabel"] = exclude_label
        if category is not None:
            params["category"] = category
        if exclude_category is not None:
            params["excludeCategory"] = exclude_category
        if topic is not None:
            params["topic"] = topic
        if exclude_topic is not None:
            params["excludeTopic"] = exclude_topic
        if link_to is not None:
            params["linkTo"] = link_to
        if show_reprints is not None:
            params["showReprints"] = show_reprints
        if reprint_group_id is not None:
            params["reprintGroupId"] = reprint_group_id
        if city is not None:
            params["city"] = city
        if exclude_city is not None:
            params["excludeCity"] = exclude_city
        if area is not None:
            params["area"] = area
        if state is not None:
            params["state"] = state
        if exclude_state is not None:
            params["excludeState"] = exclude_state
        if county is not None:
            params["county"] = county
        if exclude_county is not None:
            params["excludeCounty"] = exclude_county
        if locations_country is not None:
            params["locationsCountry"] = locations_country
        if country is not None:
            params["country"] = country
        if exclude_locations_country is not None:
            params["excludeLocationsCountry"] = exclude_locations_country
        if location is not None:
            params["location"] = location
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if max_distance is not None:
            params["maxDistance"] = max_distance
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if exclude_person_wikidata_id is not None:
            params["excludePersonWikidataId"] = exclude_person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if exclude_person_name is not None:
            params["excludePersonName"] = exclude_person_name
        if company_id is not None:
            params["companyId"] = company_id
        if exclude_company_id is not None:
            params["excludeCompanyId"] = exclude_company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if exclude_company_domain is not None:
            params["excludeCompanyDomain"] = exclude_company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if exclude_company_symbol is not None:
            params["excludeCompanySymbol"] = exclude_company_symbol
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if prefix_taxonomy is not None:
            params["prefixTaxonomy"] = prefix_taxonomy

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return QuerySearchResult.model_validate(resp.json())

    # ---------------- search_articles_async ------------------- #
    async def search_articles_async(
        self,
        q: Optional[str] = None,
        title: Optional[str] = None,
        desc: Optional[str] = None,
        content: Optional[str] = None,
        url: Optional[str] = None,
        article_id: Optional[str] = None,
        cluster_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[str] = None,
        to: Optional[str] = None,
        add_date_from: Optional[str] = None,
        add_date_to: Optional[str] = None,
        refresh_date_from: Optional[str] = None,
        refresh_date_to: Optional[str] = None,
        medium: Optional[str] = None,
        source: Optional[str] = None,
        source_group: Optional[str] = None,
        exclude_source_group: Optional[str] = None,
        exclude_source: Optional[str] = None,
        paywall: Optional[str] = None,
        byline: Optional[str] = None,
        author: Optional[str] = None,
        exclude_author: Optional[str] = None,
        journalist_id: Optional[str] = None,
        exclude_journalist_id: Optional[str] = None,
        language: Optional[str] = None,
        exclude_language: Optional[str] = None,
        search_translation: Optional[str] = None,
        label: Optional[str] = None,
        exclude_label: Optional[str] = None,
        category: Optional[str] = None,
        exclude_category: Optional[str] = None,
        topic: Optional[str] = None,
        exclude_topic: Optional[str] = None,
        link_to: Optional[str] = None,
        show_reprints: Optional[str] = None,
        reprint_group_id: Optional[str] = None,
        city: Optional[str] = None,
        exclude_city: Optional[str] = None,
        area: Optional[str] = None,
        state: Optional[str] = None,
        exclude_state: Optional[str] = None,
        county: Optional[str] = None,
        exclude_county: Optional[str] = None,
        locations_country: Optional[str] = None,
        country: Optional[str] = None,
        exclude_locations_country: Optional[str] = None,
        location: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        max_distance: Optional[float] = None,
        source_city: Optional[str] = None,
        source_county: Optional[str] = None,
        source_country: Optional[str] = None,
        source_state: Optional[str] = None,
        source_lat: Optional[float] = None,
        source_lon: Optional[float] = None,
        source_max_distance: Optional[float] = None,
        person_wikidata_id: Optional[str] = None,
        exclude_person_wikidata_id: Optional[str] = None,
        person_name: Optional[str] = None,
        exclude_person_name: Optional[str] = None,
        company_id: Optional[str] = None,
        exclude_company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        exclude_company_domain: Optional[str] = None,
        company_symbol: Optional[str] = None,
        exclude_company_symbol: Optional[str] = None,
        show_num_results: Optional[str] = None,
        positive_sentiment_from: Optional[str] = None,
        positive_sentiment_to: Optional[str] = None,
        neutral_sentiment_from: Optional[str] = None,
        neutral_sentiment_to: Optional[str] = None,
        negative_sentiment_from: Optional[str] = None,
        negative_sentiment_to: Optional[str] = None,
        taxonomy: Optional[str] = None,
        prefix_taxonomy: Optional[str] = None,
    ) -> QuerySearchResult:
        """Articles (async)"""
        path = "/v1/all"

        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if title is not None:
            params["title"] = title
        if desc is not None:
            params["desc"] = desc
        if content is not None:
            params["content"] = content
        if url is not None:
            params["url"] = url
        if article_id is not None:
            params["articleId"] = article_id
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if add_date_from is not None:
            params["addDateFrom"] = add_date_from
        if add_date_to is not None:
            params["addDateTo"] = add_date_to
        if refresh_date_from is not None:
            params["refreshDateFrom"] = refresh_date_from
        if refresh_date_to is not None:
            params["refreshDateTo"] = refresh_date_to
        if medium is not None:
            params["medium"] = medium
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if exclude_source_group is not None:
            params["excludeSourceGroup"] = exclude_source_group
        if exclude_source is not None:
            params["excludeSource"] = exclude_source
        if paywall is not None:
            params["paywall"] = paywall
        if byline is not None:
            params["byline"] = byline
        if author is not None:
            params["author"] = author
        if exclude_author is not None:
            params["excludeAuthor"] = exclude_author
        if journalist_id is not None:
            params["journalistId"] = journalist_id
        if exclude_journalist_id is not None:
            params["excludeJournalistId"] = exclude_journalist_id
        if language is not None:
            params["language"] = language
        if exclude_language is not None:
            params["excludeLanguage"] = exclude_language
        if search_translation is not None:
            params["searchTranslation"] = search_translation
        if label is not None:
            params["label"] = label
        if exclude_label is not None:
            params["excludeLabel"] = exclude_label
        if category is not None:
            params["category"] = category
        if exclude_category is not None:
            params["excludeCategory"] = exclude_category
        if topic is not None:
            params["topic"] = topic
        if exclude_topic is not None:
            params["excludeTopic"] = exclude_topic
        if link_to is not None:
            params["linkTo"] = link_to
        if show_reprints is not None:
            params["showReprints"] = show_reprints
        if reprint_group_id is not None:
            params["reprintGroupId"] = reprint_group_id
        if city is not None:
            params["city"] = city
        if exclude_city is not None:
            params["excludeCity"] = exclude_city
        if area is not None:
            params["area"] = area
        if state is not None:
            params["state"] = state
        if exclude_state is not None:
            params["excludeState"] = exclude_state
        if county is not None:
            params["county"] = county
        if exclude_county is not None:
            params["excludeCounty"] = exclude_county
        if locations_country is not None:
            params["locationsCountry"] = locations_country
        if country is not None:
            params["country"] = country
        if exclude_locations_country is not None:
            params["excludeLocationsCountry"] = exclude_locations_country
        if location is not None:
            params["location"] = location
        if lat is not None:
            params["lat"] = lat
        if lon is not None:
            params["lon"] = lon
        if max_distance is not None:
            params["maxDistance"] = max_distance
        if source_city is not None:
            params["sourceCity"] = source_city
        if source_county is not None:
            params["sourceCounty"] = source_county
        if source_country is not None:
            params["sourceCountry"] = source_country
        if source_state is not None:
            params["sourceState"] = source_state
        if source_lat is not None:
            params["sourceLat"] = source_lat
        if source_lon is not None:
            params["sourceLon"] = source_lon
        if source_max_distance is not None:
            params["sourceMaxDistance"] = source_max_distance
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if exclude_person_wikidata_id is not None:
            params["excludePersonWikidataId"] = exclude_person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if exclude_person_name is not None:
            params["excludePersonName"] = exclude_person_name
        if company_id is not None:
            params["companyId"] = company_id
        if exclude_company_id is not None:
            params["excludeCompanyId"] = exclude_company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if exclude_company_domain is not None:
            params["excludeCompanyDomain"] = exclude_company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if exclude_company_symbol is not None:
            params["excludeCompanySymbol"] = exclude_company_symbol
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if prefix_taxonomy is not None:
            params["prefixTaxonomy"] = prefix_taxonomy

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return QuerySearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

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
        return StandardSearchResult.model_validate(resp.json())

    # ----------------- search_stories (sync) ----------------- #
    def search_stories(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        cluster_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[str] = None,
        to: Optional[str] = None,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        taxonomy: Optional[str] = None,
        source: Optional[str] = None,
        source_group: Optional[str] = None,
        min_unique_sources: Optional[int] = None,
        person_wikidata_id: Optional[str] = None,
        person_name: Optional[str] = None,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        company_symbol: Optional[str] = None,
        country: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        area: Optional[str] = None,
        min_cluster_size: Optional[int] = None,
        max_cluster_size: Optional[str] = None,
        name_exists: Optional[str] = None,
        positive_sentiment_from: Optional[str] = None,
        positive_sentiment_to: Optional[str] = None,
        neutral_sentiment_from: Optional[str] = None,
        neutral_sentiment_to: Optional[str] = None,
        negative_sentiment_from: Optional[str] = None,
        negative_sentiment_to: Optional[str] = None,
        initialized_from: Optional[str] = None,
        initialized_to: Optional[str] = None,
        updated_from: Optional[str] = None,
        updated_to: Optional[str] = None,
        show_story_page_info: Optional[bool] = None,
        show_num_results: Optional[str] = None,
        show_duplicates: Optional[str] = None,
        exclude_cluster_id: Optional[str] = None,
    ) -> StandardSearchResult:
        """Stories"""
        path = "/v1/stories/all"

        # --- build query dict on the fly ---
        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if min_unique_sources is not None:
            params["minUniqueSources"] = min_unique_sources
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if company_id is not None:
            params["companyId"] = company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if country is not None:
            params["country"] = country
        if state is not None:
            params["state"] = state
        if city is not None:
            params["city"] = city
        if area is not None:
            params["area"] = area
        if min_cluster_size is not None:
            params["minClusterSize"] = min_cluster_size
        if max_cluster_size is not None:
            params["maxClusterSize"] = max_cluster_size
        if name_exists is not None:
            params["nameExists"] = name_exists
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if initialized_from is not None:
            params["initializedFrom"] = initialized_from
        if initialized_to is not None:
            params["initializedTo"] = initialized_to
        if updated_from is not None:
            params["updatedFrom"] = updated_from
        if updated_to is not None:
            params["updatedTo"] = updated_to
        if show_story_page_info is not None:
            params["showStoryPageInfo"] = show_story_page_info
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if show_duplicates is not None:
            params["showDuplicates"] = show_duplicates
        if exclude_cluster_id is not None:
            params["excludeClusterId"] = exclude_cluster_id

        resp = self.api_client.request("GET", path, params=params)
        resp.raise_for_status()
        return StandardSearchResult.model_validate(resp.json())

    # ---------------- search_stories_async ------------------- #
    async def search_stories_async(
        self,
        q: Optional[str] = None,
        name: Optional[str] = None,
        cluster_id: Optional[str] = None,
        sort_by: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        var_from: Optional[str] = None,
        to: Optional[str] = None,
        topic: Optional[str] = None,
        category: Optional[str] = None,
        taxonomy: Optional[str] = None,
        source: Optional[str] = None,
        source_group: Optional[str] = None,
        min_unique_sources: Optional[int] = None,
        person_wikidata_id: Optional[str] = None,
        person_name: Optional[str] = None,
        company_id: Optional[str] = None,
        company_name: Optional[str] = None,
        company_domain: Optional[str] = None,
        company_symbol: Optional[str] = None,
        country: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        area: Optional[str] = None,
        min_cluster_size: Optional[int] = None,
        max_cluster_size: Optional[str] = None,
        name_exists: Optional[str] = None,
        positive_sentiment_from: Optional[str] = None,
        positive_sentiment_to: Optional[str] = None,
        neutral_sentiment_from: Optional[str] = None,
        neutral_sentiment_to: Optional[str] = None,
        negative_sentiment_from: Optional[str] = None,
        negative_sentiment_to: Optional[str] = None,
        initialized_from: Optional[str] = None,
        initialized_to: Optional[str] = None,
        updated_from: Optional[str] = None,
        updated_to: Optional[str] = None,
        show_story_page_info: Optional[bool] = None,
        show_num_results: Optional[str] = None,
        show_duplicates: Optional[str] = None,
        exclude_cluster_id: Optional[str] = None,
    ) -> StandardSearchResult:
        """Stories (async)"""
        path = "/v1/stories/all"

        params: Dict[str, Any] = {}
        if q is not None:
            params["q"] = q
        if name is not None:
            params["name"] = name
        if cluster_id is not None:
            params["clusterId"] = cluster_id
        if sort_by is not None:
            params["sortBy"] = sort_by
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if var_from is not None:
            params["from"] = var_from
        if to is not None:
            params["to"] = to
        if topic is not None:
            params["topic"] = topic
        if category is not None:
            params["category"] = category
        if taxonomy is not None:
            params["taxonomy"] = taxonomy
        if source is not None:
            params["source"] = source
        if source_group is not None:
            params["sourceGroup"] = source_group
        if min_unique_sources is not None:
            params["minUniqueSources"] = min_unique_sources
        if person_wikidata_id is not None:
            params["personWikidataId"] = person_wikidata_id
        if person_name is not None:
            params["personName"] = person_name
        if company_id is not None:
            params["companyId"] = company_id
        if company_name is not None:
            params["companyName"] = company_name
        if company_domain is not None:
            params["companyDomain"] = company_domain
        if company_symbol is not None:
            params["companySymbol"] = company_symbol
        if country is not None:
            params["country"] = country
        if state is not None:
            params["state"] = state
        if city is not None:
            params["city"] = city
        if area is not None:
            params["area"] = area
        if min_cluster_size is not None:
            params["minClusterSize"] = min_cluster_size
        if max_cluster_size is not None:
            params["maxClusterSize"] = max_cluster_size
        if name_exists is not None:
            params["nameExists"] = name_exists
        if positive_sentiment_from is not None:
            params["positiveSentimentFrom"] = positive_sentiment_from
        if positive_sentiment_to is not None:
            params["positiveSentimentTo"] = positive_sentiment_to
        if neutral_sentiment_from is not None:
            params["neutralSentimentFrom"] = neutral_sentiment_from
        if neutral_sentiment_to is not None:
            params["neutralSentimentTo"] = neutral_sentiment_to
        if negative_sentiment_from is not None:
            params["negativeSentimentFrom"] = negative_sentiment_from
        if negative_sentiment_to is not None:
            params["negativeSentimentTo"] = negative_sentiment_to
        if initialized_from is not None:
            params["initializedFrom"] = initialized_from
        if initialized_to is not None:
            params["initializedTo"] = initialized_to
        if updated_from is not None:
            params["updatedFrom"] = updated_from
        if updated_to is not None:
            params["updatedTo"] = updated_to
        if show_story_page_info is not None:
            params["showStoryPageInfo"] = show_story_page_info
        if show_num_results is not None:
            params["showNumResults"] = show_num_results
        if show_duplicates is not None:
            params["showDuplicates"] = show_duplicates
        if exclude_cluster_id is not None:
            params["excludeClusterId"] = exclude_cluster_id

        resp = await self.api_client.request_async("GET", path, params=params)
        resp.raise_for_status()
        return StandardSearchResult.model_validate(resp.json())

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
        return TableSearchResult.model_validate(resp.json())

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
        return TableSearchResult.model_validate(resp.json())

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
        return SearchResult.model_validate(resp.json())

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
        return SearchResult.model_validate(resp.json())
