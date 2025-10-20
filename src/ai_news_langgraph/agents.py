"""Agent definitions for AI News LangGraph system."""

from typing import Dict, List, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import os

from .prompt_loader import load_prompt


class AgentConfig(BaseModel):
    """Configuration for an agent."""
    role: str
    goal: str
    backstory: str
    temperature: float = 0.7
    model: str = "gpt-4o-mini"


class ResearchAgent:
    """Agent responsible for researching AI news in cancer care."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig(
            role="Junior AI News Researcher",
            goal="Discover the most recent, relevant and trending topics on AI agent news in Cancer care",
            backstory="Diligent and efficient content researcher who loves staying updated with AI news"
        )
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", self.config.model),
            temperature=self.config.temperature
        )

    def create_search_queries(self, topics: List[Dict]) -> List[str]:
        """Generate optimized search queries for each topic."""
        queries = []
        for topic in topics:
            query = topic.get("query")
            if not query:
                query = f"AI {topic['name']} {topic['description']} latest news research 2024"
            queries.append(query)
        return queries

    def analyze_relevance(self, article: Dict, topic: Dict) -> float:
        """Score article relevance to topic (0-1)."""
        # Load prompt from YAML configuration
        prompt = load_prompt('research_agent', 'analyze_relevance')

        chain = prompt | self.llm
        try:
            response = chain.invoke({
                "role": self.config.role,
                "backstory": self.config.backstory,
                "topic_name": topic["name"],
                "topic_desc": topic["description"],
                "title": article.get("title", ""),
                "content": article.get("content", "")[:500]
            })
            score = float(response.content.strip())
            return min(max(score, 0), 1)  # Clamp between 0 and 1
        except:
            return 0.5  # Default score if parsing fails


class EditorAgent:
    """Agent responsible for editing and summarizing content."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig(
            role="Senior AI Researcher",
            goal="Curate and editorialize the week's top findings from AI agent news",
            backstory="Experienced analyst who can cut through noise and distill valuable insights"
        )
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", self.config.model),
            temperature=self.config.temperature
        )

    def summarize_articles(self, articles: List[Dict], topic: Dict) -> Dict:
        """Create a comprehensive summary of articles for a topic."""
        try:
            # Load prompt from YAML configuration
            prompt = load_prompt('editor_agent', 'summarize_articles')

            articles_text = "\n\n".join([
                f"- {a.get('title', 'Untitled')}: {(a.get('summary') or a.get('content') or 'No content available')[:200]}"
                for a in articles[:10]
            ])

            chain = prompt | self.llm
            response = chain.invoke({
                "role": self.config.role,
                "backstory": self.config.backstory,
                "topic_name": topic["name"],
                "topic_desc": topic["description"],
                "articles_text": articles_text
            })

            return {
                "topic": topic["name"],
                "summary": response.content,
                "article_count": len(articles)
            }
        except Exception as e:
            print(f"❌ Error in summarize_articles: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_executive_summary(self, all_summaries: List[Dict]) -> str:
        """Create an executive summary of all topics."""
        # Load prompt from YAML configuration
        prompt = load_prompt('editor_agent', 'executive_summary')

        topics_text = "\n".join([
            f"- {s['topic']}: {s['summary'][:200]}..."
            for s in all_summaries
        ])

        chain = prompt | self.llm
        response = chain.invoke({
            "role": self.config.role,
            "backstory": self.config.backstory,
            "topics_text": topics_text
        })
        return response.content


class ChiefEditorAgent:
    """Agent responsible for creating the final newsletter."""

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig(
            role="Chief Editor of AI Digest Weekly",
            goal="Refine, proofread, and publish the final HTML newsletter",
            backstory="Experienced editor who ensures newsletter is error-free and engaging"
        )
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", self.config.model),
            temperature=self.config.temperature
        )

    def generate_newsletter_html(self, content: Dict, include_images: bool = True) -> str:
        """Generate HTML newsletter from content with optional images."""
        # Initialize image generator
        image_generator = None
        if include_images:
            try:
                from .tools import ImageGenerator
                image_generator = ImageGenerator()
                print("🎨 Image generation enabled for newsletter")
            except Exception as e:
                print(f"⚠️ Image generation disabled: {e}")

        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI in Cancer Care Newsletter</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .executive-summary {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .topic-section {{
            margin: 30px 0;
            padding: 20px;
            background: #fafafa;
            border-radius: 8px;
        }}
        .topic-image {{
            width: 100%;
            max-width: 600px;
            height: auto;
            border-radius: 8px;
            margin: 20px auto;
            display: block;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .article-list {{
            margin-top: 15px;
        }}
        .article-item {{
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }}
        .article-title {{
            font-weight: bold;
            color: #2c3e50;
        }}
        .article-summary {{
            margin-top: 5px;
            color: #555;
            font-size: 0.95em;
        }}
        .highlights {{
            background: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .highlights ul {{
            margin: 10px 0;
        }}
        .highlights li {{
            margin: 8px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #777;
            font-size: 0.9em;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 AI in Cancer Care Newsletter</h1>

        <div class="executive-summary">
            <h2>Executive Summary</h2>
            <p>{executive_summary}</p>
        </div>

        {topic_sections}

        <div class="footer">
            <p>© 2024 AI in Cancer Care Newsletter | Generated with LangGraph + AI</p>
            <p>Stay informed about the latest AI developments in oncology and cancer research</p>
        </div>
    </div>
</body>
</html>"""

        topic_sections = ""
        for topic_data in content.get("topics", []):
            # Generate image for topic
            image_html = ""
            if image_generator:
                try:
                    image_info = image_generator.generate_topic_image(
                        topic_name=topic_data.get('name', 'Topic'),
                        topic_description=topic_data.get('summary', ''),
                        use_dalle=os.getenv("USE_DALLE", "true").lower() == "true"
                    )
                    if image_info and image_info.get('data_url'):
                        image_html = f'<img src="{image_info["data_url"]}" alt="{topic_data.get("name", "Topic")}" class="topic-image">'
                        # Store image info in topic_data for later use
                        topic_data['image_info'] = image_info
                except Exception as e:
                    print(f"⚠️ Failed to generate image for {topic_data.get('name', 'Topic')}: {e}")

            articles_html = ""
            for article in topic_data.get("articles", [])[:5]:
                articles_html += f"""
                <div class="article-item">
                    <div class="article-title">
                        <a href="{article.get('url', '#')}" target="_blank">{article.get('title', 'Untitled')}</a>
                    </div>
                    <div class="article-summary">{article.get('summary', '')}</div>
                </div>"""

            topic_sections += f"""
            <div class="topic-section">
                <h2>{topic_data.get('name', 'Topic')}</h2>
                {image_html}
                <p>{topic_data.get('summary', '')}</p>

                <div class="highlights">
                    <strong>Key Highlights:</strong>
                    <ul>
                        {self._generate_highlights_html(topic_data)}
                    </ul>
                </div>

                <h3>Featured Articles</h3>
                <div class="article-list">
                    {articles_html}
                </div>
            </div>"""

        return html_template.format(
            executive_summary=content.get("executive_summary", ""),
            topic_sections=topic_sections
        )

    def _generate_highlights_html(self, topic_data: Dict) -> str:
        """Generate HTML for topic highlights."""
        highlights = topic_data.get("highlights", [])
        if not highlights:
            # Extract key points from summary
            summary = topic_data.get("summary", "")
            if summary:
                highlights = ["Latest research developments", "Clinical applications", "Future directions"]

        return "\n".join([f"<li>{h}</li>" for h in highlights[:5]])

    def generate_markdown_report(self, content: Dict) -> str:
        """Generate markdown report from content."""
        markdown = f"""# AI in Cancer Care Research Report

## Executive Summary

{content.get("executive_summary", "")}

---

"""

        for topic_data in content.get("topics", []):
            markdown += f"""
## {topic_data.get('name', 'Topic')}

### Overview
{topic_data.get('summary', '')}

### Key Articles

"""
            for article in topic_data.get('articles', [])[:5]:
                markdown += f"""- **[{article.get('title', 'Untitled')}]({article.get('url', '#')})**
  {article.get('summary', '')}

"""

        markdown += """
---

*Generated with AI News LangGraph System*
"""
        return markdown