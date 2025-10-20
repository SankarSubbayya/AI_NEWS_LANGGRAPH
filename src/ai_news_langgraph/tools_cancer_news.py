"""
Cancer-specific news sources and APIs.

This module provides targeted search capabilities for cancer-related AI research
from authoritative medical and scientific sources.
"""

from typing import List, Dict, Optional, Any
import os
import requests
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import feedparser


class CancerNewsAPI:
    """
    Multi-source cancer news aggregator focusing on AI applications in oncology.

    Supported sources:
    - PubMed/NIH (via NCBI E-utilities API)
    - AI News API
    - NewsAPI.org
    - Direct RSS feeds from medical journals
    - Web scraping for specific sources
    """

    def __init__(self):
        """Initialize cancer news API clients."""
        self.ai_news_api_key = os.getenv("AI_NEWS_API_KEY")
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.pubmed_email = os.getenv("PUBMED_EMAIL", "researcher@example.com")

        # Cancer-specific news sources
        self.sources = {
            "oncology_news_central": {
                "name": "Oncology News Central",
                "rss": "https://www.onclive.com/rss",
                "base_url": "https://www.onclive.com",
                "type": "rss"
            },
            "jco": {
                "name": "Journal of Clinical Oncology",
                "rss": "https://ascopubs.org/action/showFeed?type=etoc&feed=rss&jc=jco",
                "base_url": "https://ascopubs.org/journal/jco",
                "type": "rss"
            },
            "nejm": {
                "name": "New England Journal of Medicine",
                "rss": "https://www.nejm.org/action/showFeed?type=etoc&feed=rss&jc=nejm",
                "base_url": "https://www.nejm.org",
                "type": "rss"
            },
            "pubmed": {
                "name": "PubMed/NCBI",
                "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
                "type": "api"
            },
            "cancer_gov": {
                "name": "National Cancer Institute",
                "rss": "https://www.cancer.gov/syndication/feeds/rss/news",
                "base_url": "https://www.cancer.gov",
                "type": "rss"
            },
            "asco": {
                "name": "American Society of Clinical Oncology",
                "rss": "https://www.asco.org/rss.xml",
                "base_url": "https://www.asco.org",
                "type": "rss"
            },
            "nature_cancer": {
                "name": "Nature Cancer",
                "rss": "https://www.nature.com/ncancer.rss",
                "base_url": "https://www.nature.com/ncancer",
                "type": "rss"
            },
            "stanford_pubnet": {
                "name": "Stanford Medicine PubNet",
                "base_url": "https://med.stanford.edu/news.html",
                "type": "web"
            }
        }

        print(f"🏥 Initialized Cancer News API with {len(self.sources)} sources")

    def search_all_sources(
        self,
        query: str,
        max_results_per_source: int = 5,
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Search all cancer-specific sources for relevant articles.

        Args:
            query: Search query (e.g., "AI artificial intelligence machine learning cancer")
            max_results_per_source: Max results per source
            days_back: Number of days to look back

        Returns:
            List of articles from all sources
        """
        all_results = []

        print(f"\n🔬 Searching cancer-specific sources for: {query[:60]}...")

        # Search PubMed
        try:
            pubmed_results = self._search_pubmed(query, max_results_per_source, days_back)
            all_results.extend(pubmed_results)
            print(f"   ✅ PubMed: {len(pubmed_results)} articles")
        except Exception as e:
            print(f"   ⚠️  PubMed error: {e}")

        # Search RSS feeds
        for source_id, source_info in self.sources.items():
            if source_info["type"] == "rss" and source_id != "pubmed":
                try:
                    results = self._search_rss_feed(
                        source_info,
                        query,
                        max_results_per_source,
                        days_back
                    )
                    all_results.extend(results)
                    print(f"   ✅ {source_info['name']}: {len(results)} articles")
                except Exception as e:
                    print(f"   ⚠️  {source_info['name']} error: {e}")

        # Search with AI News API if available
        if self.ai_news_api_key:
            try:
                ai_news_results = self._search_ai_news_api(query, max_results_per_source)
                all_results.extend(ai_news_results)
                print(f"   ✅ AI News API: {len(ai_news_results)} articles")
            except Exception as e:
                print(f"   ⚠️  AI News API error: {e}")

        # Search with NewsAPI.org if available
        if self.newsapi_key:
            try:
                newsapi_results = self._search_newsapi(query, max_results_per_source, days_back)
                all_results.extend(newsapi_results)
                print(f"   ✅ NewsAPI: {len(newsapi_results)} articles")
            except Exception as e:
                print(f"   ⚠️  NewsAPI error: {e}")

        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            url = result.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)

        # Sort by date (most recent first) and relevance
        unique_results.sort(
            key=lambda x: (x.get("published_date", ""), x.get("score", 0)),
            reverse=True
        )

        print(f"\n📊 Total unique articles found: {len(unique_results)}")
        return unique_results

    def _search_pubmed(
        self,
        query: str,
        max_results: int,
        days_back: int
    ) -> List[Dict[str, Any]]:
        """Search PubMed using NCBI E-utilities API."""
        # Construct PubMed query with date restriction
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y/%m/%d")
        to_date = datetime.now().strftime("%Y/%m/%d")

        # Search query
        search_url = f"{self.sources['pubmed']['base_url']}/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": f"{query} AND ({from_date}:{to_date}[dp])",
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance",
            "email": self.pubmed_email
        }

        response = requests.get(search_url, params=search_params, timeout=10)
        response.raise_for_status()
        search_data = response.json()

        id_list = search_data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return []

        # Fetch details for each article
        fetch_url = f"{self.sources['pubmed']['base_url']}/esummary.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(id_list),
            "retmode": "json",
            "email": self.pubmed_email
        }

        response = requests.get(fetch_url, params=fetch_params, timeout=10)
        response.raise_for_status()
        fetch_data = response.json()

        results = []
        for pmid in id_list:
            article = fetch_data.get("result", {}).get(pmid, {})
            if article:
                results.append({
                    "title": article.get("title", ""),
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "content": article.get("title", ""),  # Use title as content snippet
                    "source": "PubMed",
                    "published_date": article.get("pubdate", ""),
                    "score": 0.9,  # High relevance for PubMed results
                    "authors": ", ".join([a.get("name", "") for a in article.get("authors", [])[:3]]),
                    "journal": article.get("source", ""),
                    "pmid": pmid
                })

        return results

    def _search_rss_feed(
        self,
        source_info: Dict[str, str],
        query: str,
        max_results: int,
        days_back: int
    ) -> List[Dict[str, Any]]:
        """Search an RSS feed for relevant articles."""
        rss_url = source_info.get("rss")
        if not rss_url:
            return []

        feed = feedparser.parse(rss_url)
        results = []

        cutoff_date = datetime.now() - timedelta(days=days_back)
        query_terms = query.lower().split()

        for entry in feed.entries[:max_results * 3]:  # Get extra to filter
            # Parse publication date
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6])

            # Filter by date
            if pub_date and pub_date < cutoff_date:
                continue

            # Calculate relevance score based on query terms
            title = entry.get("title", "").lower()
            summary = entry.get("summary", "").lower()
            content = f"{title} {summary}"

            score = sum(1 for term in query_terms if term in content) / len(query_terms)

            # Only include if somewhat relevant
            if score > 0.2:
                results.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "content": entry.get("summary", "")[:500],
                    "source": source_info["name"],
                    "published_date": pub_date.isoformat() if pub_date else "",
                    "score": min(score, 1.0)
                })

            if len(results) >= max_results:
                break

        return results

    def _search_ai_news_api(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Search using AI News API (https://www.ainews-api.com/).

        Note: Replace with actual AI News API endpoint and parameters.
        """
        if not self.ai_news_api_key:
            return []

        # Example endpoint - adjust based on actual API documentation
        url = "https://api.ainews.com/v1/search"
        headers = {"Authorization": f"Bearer {self.ai_news_api_key}"}
        params = {
            "q": f"{query} cancer oncology",
            "limit": max_results,
            "category": "healthcare"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])

                results = []
                for article in articles:
                    results.append({
                        "title": article.get("title", ""),
                        "url": article.get("url", ""),
                        "content": article.get("description", ""),
                        "source": article.get("source", "AI News API"),
                        "published_date": article.get("publishedAt", ""),
                        "score": article.get("relevance", 0.7)
                    })

                return results
        except Exception as e:
            print(f"AI News API error: {e}")

        return []

    def _search_newsapi(
        self,
        query: str,
        max_results: int,
        days_back: int
    ) -> List[Dict[str, Any]]:
        """Search using NewsAPI.org."""
        if not self.newsapi_key:
            return []

        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": self.newsapi_key,
            "q": f"{query} cancer",
            "from": from_date,
            "sortBy": "relevancy",
            "pageSize": max_results,
            "language": "en",
            "domains": "nature.com,science.org,nejm.org,thelancet.com,cell.com"
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            results = []
            for article in articles:
                results.append({
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "content": article.get("description", ""),
                    "source": article.get("source", {}).get("name", "NewsAPI"),
                    "published_date": article.get("publishedAt", ""),
                    "score": 0.7
                })

            return results

        return []

    def search_by_topic(
        self,
        topic: str,
        subtopics: List[str],
        max_results_per_topic: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for articles organized by subtopics.

        Args:
            topic: Main topic (e.g., "AI in Cancer Care")
            subtopics: List of subtopics to search
            max_results_per_topic: Max results per subtopic

        Returns:
            Dictionary mapping subtopics to article lists
        """
        results = {}

        print(f"\n🎯 Searching for topic: {topic}")
        for subtopic in subtopics:
            query = f"AI artificial intelligence machine learning {topic} {subtopic} cancer oncology"
            articles = self.search_all_sources(query, max_results_per_topic)
            results[subtopic] = articles

        return results


class CancerNewsToolIntegration:
    """Integration layer for CancerNewsAPI with existing tool system."""

    def __init__(self):
        self.api = CancerNewsAPI()

    def search(
        self,
        query: str,
        max_results: int = 10,
        days_back: int = 30,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search cancer-specific sources (compatible with NewsSearchTool interface).

        Args:
            query: Search query
            max_results: Maximum results to return
            days_back: Number of days to look back

        Returns:
            List of articles
        """
        results_per_source = max(1, max_results // 5)  # Distribute across sources
        results = self.api.search_all_sources(query, results_per_source, days_back)
        return results[:max_results]

    def search_academic(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search academic sources (PubMed focus).

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of academic articles
        """
        results = self.api._search_pubmed(query, max_results, days_back=90)
        return results
