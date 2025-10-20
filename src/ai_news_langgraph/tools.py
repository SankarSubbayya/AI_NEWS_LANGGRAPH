"""Tools for AI News LangGraph system."""

from typing import List, Dict, Optional, Any
import os
import json
from datetime import datetime, timedelta
from tavily import TavilyClient
from langchain_core.tools import tool
import requests
import base64
from pathlib import Path


class NewsSearchTool:
    """Tool for searching news and research articles."""

    def __init__(self):
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.preferred_api = os.getenv("PREFERRED_SEARCH_API", "cancer_sources").lower()
        self.tavily_client = None
        if self.tavily_api_key:
            self.tavily_client = TavilyClient(api_key=self.tavily_api_key)

        # Initialize cancer-specific news API
        self.use_cancer_sources = os.getenv("USE_CANCER_SOURCES", "true").lower() == "true"
        if self.use_cancer_sources:
            try:
                from .tools_cancer_news import CancerNewsToolIntegration
                self.cancer_news = CancerNewsToolIntegration()
                print("🔍 Search API: Cancer-specific sources (PubMed, NEJM, JCO, etc.) with fallback")
            except Exception as e:
                print(f"⚠️  Could not load cancer sources: {e}")
                self.cancer_news = None
                self.use_cancer_sources = False
        else:
            self.cancer_news = None

        # Log which API will be used
        if not self.use_cancer_sources:
            if self.preferred_api == "serper" and self.serper_api_key:
                print("🔍 Search API: Serper (Google Search) with Tavily fallback")
            elif self.preferred_api == "tavily" and self.tavily_api_key:
                print("🔍 Search API: Tavily (AI-optimized) with Serper fallback")
            elif self.serper_api_key:
                print("🔍 Search API: Serper (primary)")
            elif self.tavily_api_key:
                print("🔍 Search API: Tavily (primary)")
            else:
                print("⚠️  Warning: No search API keys configured!")

    def search(self, query: str, max_results: int = 10, days_back: int = 7, prefer_serper: bool = None) -> List[Dict]:
        """Search for news articles using available search APIs.

        Args:
            query: Search query
            max_results: Maximum number of results
            days_back: Only return articles from last N days
            prefer_serper: If True, use Serper first, else use Tavily first.
                          If None, uses PREFERRED_SEARCH_API env var (default: cancer_sources)
        """
        results = []

        # Try cancer-specific sources first if enabled
        if self.use_cancer_sources and self.cancer_news:
            try:
                print(f"🏥 Searching cancer-specific sources: {query[:50]}...")
                results = self.cancer_news.search(query, max_results, days_back)
                if results:
                    print(f"✅ Cancer sources returned {len(results)} results")
                    return results
            except Exception as e:
                print(f"⚠️  Cancer sources error: {e}")
                print(f"   Falling back to general search APIs...")

        # Determine which API to prefer
        if prefer_serper is None:
            prefer_serper = (self.preferred_api == "serper")

        # Try Serper first if preferred and available
        if prefer_serper and self.serper_api_key:
            try:
                print(f"🔍 Searching with Serper API: {query[:50]}...")
                results = self._search_with_serper(query, max_results)
                if results:
                    print(f"✅ Serper returned {len(results)} results")
                    return results
            except Exception as e:
                print(f"⚠️  Serper search error: {e}")
                print(f"   Falling back to Tavily...")

        # Try Tavily (either as primary or fallback)
        if self.tavily_client and not results:
            try:
                print(f"🔍 Searching with Tavily API: {query[:50]}...")
                response = self.tavily_client.search(
                    query=query,
                    max_results=max_results,
                    search_depth="advanced",
                    include_raw_content=True,
                    include_domains=["pubmed.gov", "nature.com", "sciencedirect.com",
                                   "nejm.org", "cancer.gov", "nih.gov", "arxiv.org"],
                    days=days_back
                )

                if isinstance(response, dict):
                    results = response.get("results", [])
                else:
                    results = response if response else []

                # Normalize results
                normalized = []
                for item in results:
                    normalized.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "content": item.get("content", item.get("raw_content", ""))[:1000],
                        "source": item.get("source", ""),
                        "published_date": item.get("published_date", ""),
                        "score": item.get("score", 0.5)
                    })
                
                if normalized:
                    print(f"✅ Tavily returned {len(normalized)} results")
                return normalized

            except Exception as e:
                print(f"⚠️  Tavily search error: {e}")

        # Try Serper as final fallback if not already tried
        if not prefer_serper and self.serper_api_key and not results:
            try:
                print(f"🔍 Falling back to Serper API...")
                results = self._search_with_serper(query, max_results)
                if results:
                    print(f"✅ Serper returned {len(results)} results")
            except Exception as e:
                print(f"⚠️  Serper search error: {e}")

        if not results:
            print(f"❌ No results found from any search API")

        return results

    def _search_with_serper(self, query: str, max_results: int) -> List[Dict]:
        """Search using Serper API."""
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": query,
            "num": max_results,
            "gl": "us",
            "hl": "en"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            organic = data.get("organic", [])

            normalized = []
            for item in organic:
                normalized.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "content": item.get("snippet", ""),
                    "source": item.get("source", ""),
                    "published_date": item.get("date", ""),
                    "score": 0.5
                })
            return normalized
        return []

    def search_academic(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search specifically for academic papers and research."""
        # Try cancer-specific academic sources first (PubMed focus)
        if self.use_cancer_sources and self.cancer_news:
            try:
                print(f"🎓 Searching academic sources via PubMed: {query[:50]}...")
                results = self.cancer_news.search_academic(query, max_results)
                if results:
                    print(f"✅ Academic sources returned {len(results)} results")
                    return results
            except Exception as e:
                print(f"⚠️  Academic search error: {e}")

        # Fallback to general academic search
        # Add academic search terms
        academic_query = f"{query} research paper study clinical trial meta-analysis systematic review"

        results = self.search(academic_query, max_results * 2)  # Get more results to filter

        # Filter for academic sources
        academic_domains = ["pubmed", "nature", "science", "nejm", "lancet", "cell", "arxiv", "nih", ".edu"]
        filtered = []

        for result in results:
            url = result.get("url", "").lower()
            if any(domain in url for domain in academic_domains):
                filtered.append(result)
                if len(filtered) >= max_results:
                    break

        return filtered if filtered else results[:max_results]


class DocumentProcessor:
    """Tool for processing and analyzing documents."""

    def extract_key_points(self, text: str, max_points: int = 5) -> List[str]:
        """Extract key points from text."""
        # Simple extraction based on sentence importance
        sentences = text.split(". ")

        # Filter short sentences
        sentences = [s for s in sentences if len(s.split()) > 5]

        # Score sentences based on keyword presence
        keywords = ["AI", "artificial intelligence", "cancer", "treatment", "diagnosis",
                   "research", "study", "found", "showed", "demonstrated", "improved",
                   "novel", "breakthrough", "significant", "clinical"]

        scored = []
        for sentence in sentences:
            score = sum(1 for kw in keywords if kw.lower() in sentence.lower())
            scored.append((sentence, score))

        # Sort by score and return top points
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:max_points]]

    def categorize_content(self, text: str, categories: List[str]) -> Dict[str, float]:
        """Categorize content based on predefined categories."""
        scores = {}
        text_lower = text.lower()

        category_keywords = {
            "diagnosis": ["diagnosis", "diagnostic", "detection", "screening", "imaging", "biomarker"],
            "treatment": ["treatment", "therapy", "drug", "medication", "chemotherapy", "radiation"],
            "prevention": ["prevention", "preventive", "risk", "lifestyle", "screening", "early"],
            "research": ["research", "study", "trial", "investigation", "analysis", "finding"],
            "technology": ["AI", "machine learning", "deep learning", "algorithm", "model", "system"]
        }

        for category in categories:
            if category.lower() in category_keywords:
                keywords = category_keywords[category.lower()]
                score = sum(1 for kw in keywords if kw in text_lower)
                scores[category] = min(score / 10.0, 1.0)  # Normalize to 0-1
            else:
                scores[category] = 0.0

        return scores


class FileManager:
    """Tool for managing file outputs."""

    @staticmethod
    def save_json(data: Dict, filepath: str):
        """Save data as JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    @staticmethod
    def save_html(content: str, filepath: str):
        """Save content as HTML file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)

    @staticmethod
    def save_markdown(content: str, filepath: str):
        """Save content as Markdown file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)

    @staticmethod
    def load_json(filepath: str) -> Dict:
        """Load JSON file."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}


# LangChain tool wrappers for use in agents
@tool
def search_news(query: str, max_results: int = 10) -> List[Dict]:
    """Search for news articles about a given topic.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of article dictionaries with title, url, content, etc.
    """
    searcher = NewsSearchTool()
    return searcher.search(query, max_results)


@tool
def search_academic_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Search for academic papers and research articles.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of paper dictionaries with title, url, content, etc.
    """
    searcher = NewsSearchTool()
    return searcher.search_academic(query, max_results)


@tool
def extract_key_points(text: str, max_points: int = 5) -> List[str]:
    """Extract key points from a text document.

    Args:
        text: Input text to analyze
        max_points: Maximum number of key points to extract

    Returns:
        List of key point strings
    """
    processor = DocumentProcessor()
    return processor.extract_key_points(text, max_points)


@tool
def save_output_file(content: str, filepath: str, file_type: str = "markdown"):
    """Save content to a file.

    Args:
        content: Content to save
        filepath: Path to save file
        file_type: Type of file (markdown, html, json)
    """
    manager = FileManager()
    if file_type == "json":
        import json
        data = json.loads(content) if isinstance(content, str) else content
        manager.save_json(data, filepath)
    elif file_type == "html":
        manager.save_html(content, filepath)
    else:
        manager.save_markdown(content, filepath)


class ImageGenerator:
    """Tool for generating images and diagrams for topics."""

    def __init__(self):
        """Initialize the image generator."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.output_dir = Path("outputs/images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_topic_image(
        self,
        topic_name: str,
        topic_description: str,
        use_dalle: bool = True
    ) -> Optional[Dict[str, str]]:
        """
        Generate an image for a topic.

        Args:
            topic_name: Name of the topic
            topic_description: Description of the topic
            use_dalle: If True, use DALL-E, otherwise create a simple diagram

        Returns:
            Dict with image path and data URL, or None if failed
        """
        try:
            if use_dalle and self.openai_api_key:
                return self._generate_with_dalle(topic_name, topic_description)
            else:
                return self._generate_placeholder_image(topic_name, topic_description)
        except Exception as e:
            print(f"⚠️ Error generating image for {topic_name}: {e}")
            return self._generate_placeholder_image(topic_name, topic_description)

    def _generate_with_dalle(
        self,
        topic_name: str,
        topic_description: str
    ) -> Optional[Dict[str, str]]:
        """Generate image using OpenAI DALL-E."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)

            # Create a descriptive prompt for medical/scientific visualization
            prompt = self._create_image_prompt(topic_name, topic_description)

            print(f"🎨 Generating image for '{topic_name}' using DALL-E...")

            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url

            # Download and save the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = topic_name.lower().replace(" ", "_").replace("/", "_")
                filename = f"{safe_name}_{timestamp}.png"
                filepath = self.output_dir / filename

                with open(filepath, 'wb') as f:
                    f.write(image_response.content)

                # Create data URL for embedding
                img_data = base64.b64encode(image_response.content).decode()
                data_url = f"data:image/png;base64,{img_data}"

                print(f"✅ Image saved: {filepath}")

                return {
                    "path": str(filepath),
                    "data_url": data_url,
                    "filename": filename,
                    "prompt": prompt
                }

        except Exception as e:
            print(f"❌ DALL-E generation failed: {e}")
            return None

    def _create_image_prompt(self, topic_name: str, topic_description: str) -> str:
        """Create an effective prompt for DALL-E image generation."""
        # Base prompt for medical/scientific style
        base_style = (
            "Create a professional, modern scientific illustration in a clean, "
            "minimalist style with a blue and teal color scheme. "
        )

        # Topic-specific prompts
        topic_prompts = {
            "cancer research": "Show abstract representation of cancer cells, DNA strands, and AI neural networks analyzing genomic data. Include microscope imagery and data visualization elements.",
            "cancer prevention": "Illustrate preventive healthcare with AI monitoring health metrics, lifestyle factors, and early warning systems. Show wellness and proactive health management.",
            "early detection": "Depict AI-powered medical imaging analysis with highlighted areas of interest, diagnostic tools, and pattern recognition. Include radiology and pathology elements.",
            "treatment planning": "Show personalized medicine concept with patient data, treatment pathways, and AI optimization algorithms. Include molecular targeting and precision therapy visualization.",
            "clinical trials": "Illustrate clinical trial design with patient matching, data collection, and AI-driven analysis. Show diverse patient groups and research workflow."
        }

        # Find best matching topic
        topic_lower = topic_name.lower()
        specific_prompt = next(
            (prompt for key, prompt in topic_prompts.items() if key in topic_lower),
            f"Illustrate the concept of {topic_name} in healthcare with AI technology, showing data analysis and medical innovation."
        )

        full_prompt = (
            f"{base_style}{specific_prompt} "
            f"Style: Clean, professional medical illustration with technology elements. "
            f"No text, no people's faces, abstract and conceptual."
        )

        return full_prompt

    def _generate_placeholder_image(
        self,
        topic_name: str,
        topic_description: str
    ) -> Dict[str, str]:
        """Generate a simple SVG placeholder image."""
        # Create SVG with gradient and topic name
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e3a8a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0891b2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="400" fill="url(#grad1)"/>
  <text x="400" y="180" font-family="Arial, sans-serif" font-size="48"
        fill="white" text-anchor="middle" font-weight="bold">
    {topic_name}
  </text>
  <text x="400" y="240" font-family="Arial, sans-serif" font-size="20"
        fill="#e0f2fe" text-anchor="middle" font-weight="300">
    AI in Cancer Care
  </text>
</svg>'''

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = topic_name.lower().replace(" ", "_").replace("/", "_")
        filename = f"{safe_name}_{timestamp}.svg"
        filepath = self.output_dir / filename

        with open(filepath, 'w') as f:
            f.write(svg_content)

        # Create data URL
        svg_b64 = base64.b64encode(svg_content.encode()).decode()
        data_url = f"data:image/svg+xml;base64,{svg_b64}"

        return {
            "path": str(filepath),
            "data_url": data_url,
            "filename": filename,
            "type": "svg"
        }