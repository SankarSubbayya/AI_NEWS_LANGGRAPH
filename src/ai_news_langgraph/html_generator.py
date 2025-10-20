"""HTML Newsletter Generator with modern templates."""

from typing import Dict, List, Any
from datetime import datetime
import base64
from pathlib import Path
import re


class HTMLNewsletterGenerator:
    """Generate beautiful HTML newsletters with embedded styles."""
    
    @staticmethod
    def _convert_markdown_to_html(text: str) -> str:
        """Convert basic Markdown formatting to HTML.
        
        Converts:
        - **text** to <strong>text</strong>
        - ## Heading to styled h3
        - ### Heading to styled h4
        """
        if not text:
            return text
        
        # Convert ## Headings (at start of line)
        text = re.sub(r'^## (.+)$', r'<h3 style="color: #667eea; font-size: 1.3em; margin: 20px 0 10px 0;">\1</h3>', text, flags=re.MULTILINE)
        
        # Convert ### Headings (at start of line)
        text = re.sub(r'^### (.+)$', r'<h4 style="color: #764ba2; font-size: 1.1em; margin: 15px 0 8px 0;">\1</h4>', text, flags=re.MULTILINE)
        
        # Convert **bold** to <strong>
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50;">\1</strong>', text)
        
        # Convert line breaks to <br> tags
        text = text.replace('\n\n', '</p><p style="margin: 10px 0;">')
        
        return text
    
    @staticmethod
    def generate_newsletter_html(
        executive_summary: str,
        topic_summaries: List[Dict[str, Any]],
        main_topic: str = "AI in Cancer Care",
        metrics: Dict[str, Any] = None,
        chart_images: Dict[str, str] = None,
        cover_image: str = None,
        glossary: Dict[str, Any] = None,
        knowledge_graph: Dict[str, Any] = None
    ) -> str:
        """Generate a complete HTML newsletter.

        Args:
            executive_summary: Overall summary text
            topic_summaries: List of topic summary dicts
            main_topic: Main newsletter topic
            metrics: Optional metrics dict
            chart_images: Optional dict of chart image paths
            cover_image: Optional cover image (base64 or URL)
            glossary: Optional glossary dict with entries
            knowledge_graph: Optional knowledge graph data

        Returns:
            Complete HTML string
        """
        date_str = datetime.now().strftime("%B %d, %Y")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{main_topic} Newsletter - {date_str}</title>
    <style>
        {HTMLNewsletterGenerator._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {HTMLNewsletterGenerator._generate_header(main_topic, date_str, cover_image)}
        
        {HTMLNewsletterGenerator._generate_metrics_section(metrics) if metrics else ''}
        
        {HTMLNewsletterGenerator._generate_executive_summary(executive_summary)}
        
        {HTMLNewsletterGenerator._generate_charts_section(chart_images) if chart_images else ''}
        
        {HTMLNewsletterGenerator._generate_topics_section(topic_summaries)}

        {HTMLNewsletterGenerator._generate_glossary_section(glossary) if glossary else ''}

        {HTMLNewsletterGenerator._generate_footer()}
    </div>
</body>
</html>"""
        
        return html
    
    @staticmethod
    def _get_css_styles() -> str:
        """Get modern CSS styles for the newsletter."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header .date {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 3px solid #667eea;
        }
        
        .metric-card {
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .section {
            padding: 40px;
        }
        
        .section-title {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        
        .executive-summary {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-left: 4px solid #667eea;
            padding: 30px;
            margin: 20px 0;
            border-radius: 8px;
            font-size: 1.1em;
            line-height: 1.8;
        }
        
        .topic-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .topic-card:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .topic-title {
            font-size: 1.6em;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .topic-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: white;
            font-weight: bold;
        }
        
        .quality-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            margin-left: 10px;
        }
        
        .quality-badge.medium {
            background: #ffc107;
        }
        
        .quality-badge.low {
            background: #dc3545;
        }
        
        .topic-overview {
            margin: 20px 0;
            line-height: 1.8;
            color: #555;
        }
        
        .key-findings {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .key-findings h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .key-findings ul {
            list-style: none;
            padding-left: 0;
        }
        
        .key-findings li {
            padding: 10px 0 10px 30px;
            position: relative;
            border-bottom: 1px solid #eee;
        }
        
        .key-findings li:last-child {
            border-bottom: none;
        }
        
        .key-findings li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .trends {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .trends h4 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        .trends ul {
            list-style: none;
            padding-left: 20px;
        }
        
        .trends li:before {
            content: "▶";
            color: #ffc107;
            margin-right: 10px;
        }
        
        .articles-section {
            background: #f0f4ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .articles-section h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        
        .articles-list {
            list-style: none;
            counter-reset: article-counter;
            padding-left: 0;
        }
        
        .article-item {
            counter-increment: article-counter;
            padding: 12px 0;
            border-bottom: 1px solid #d0d7e5;
            position: relative;
            padding-left: 35px;
        }
        
        .article-item:before {
            content: counter(article-counter);
            position: absolute;
            left: 0;
            top: 12px;
            background: #667eea;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .article-item:last-child {
            border-bottom: none;
        }
        
        .article-link {
            color: #2c3e50;
            text-decoration: none;
            display: block;
            margin-bottom: 5px;
            transition: color 0.2s;
        }
        
        .article-link:hover {
            color: #667eea;
            text-decoration: underline;
        }
        
        .article-link strong {
            font-size: 1.05em;
        }
        
        .article-meta {
            color: #666;
            font-size: 0.85em;
            display: block;
        }
        
        .footer {
            background: #2c3e50;
            color: white;
            padding: 30px 40px;
            text-align: center;
        }
        
        .footer p {
            margin: 10px 0;
            opacity: 0.8;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            margin: 20px 0;
            transition: transform 0.2s;
        }
        
        .cta-button:hover {
            transform: scale(1.05);
        }
        
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background: white;
            border-radius: 8px;
            text-align: center;
        }
        
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }

        .cover-image {
            width: 100%;
            margin: 0;
            padding: 0;
            line-height: 0;
        }

        .cover-image img {
            width: 100%;
            height: auto;
            display: block;
            object-fit: cover;
            max-height: 400px;
        }

        .glossary-section {
            background: linear-gradient(135deg, #f5f7fa 0%, #e8ebf5 100%);
            padding: 40px;
            margin-top: 40px;
            border-top: 3px solid #667eea;
        }

        .glossary-title {
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            text-align: center;
        }

        .glossary-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-style: italic;
        }

        .glossary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .glossary-item {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .glossary-term {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }

        .glossary-type {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75em;
            margin-left: 10px;
            text-transform: uppercase;
        }

        .glossary-definition {
            color: #555;
            line-height: 1.6;
            margin-top: 10px;
        }

        .glossary-related {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #888;
        }

        .glossary-related strong {
            color: #667eea;
        }

        @media (max-width: 600px) {
            .header h1 {
                font-size: 1.8em;
            }

            .section {
                padding: 20px;
            }

            .metrics {
                grid-template-columns: 1fr;
            }

            .cover-image img {
                max-height: 250px;
            }
        }
        """
    
    @staticmethod
    def _generate_header(main_topic: str, date_str: str, cover_image: str = None) -> str:
        """Generate newsletter header with optional cover image.

        Args:
            main_topic: Main newsletter topic
            date_str: Formatted date string
            cover_image: Base64 encoded cover image or file path (optional)
        """
        cover_html = ""
        if cover_image:
            # Check if it's a file path or already base64
            if cover_image.startswith('data:image') or cover_image.startswith('http'):
                # Already base64 or URL
                image_src = cover_image
            else:
                # It's a file path, convert to base64
                try:
                    import base64
                    from pathlib import Path

                    image_path = Path(cover_image)
                    if image_path.exists():
                        with open(image_path, 'rb') as img_file:
                            img_data = base64.b64encode(img_file.read()).decode()
                            image_src = f"data:image/png;base64,{img_data}"
                    else:
                        print(f"Warning: Cover image not found at {cover_image}")
                        image_src = None
                except Exception as e:
                    print(f"Error embedding cover image: {e}")
                    image_src = None

            if image_src:
                # Place cover image OUTSIDE and ABOVE the header for full-width display
                cover_html = f"""
                <div class="cover-image" style="width: 100%; margin: 0; padding: 0;">
                    <img src="{image_src}" alt="AI in Cancer Care Newsletter Cover"
                         style="width: 100%; height: auto; display: block; border-radius: 12px 12px 0 0;">
                </div>
                """

        # Return cover image BEFORE the header so it displays at the top
        return f"""
        {cover_html}
        <div class="header">
            <h1>🔬 {main_topic}</h1>
            <p class="date">Newsletter • {date_str}</p>
        </div>
        """
    
    @staticmethod
    def _generate_metrics_section(metrics: Dict[str, Any]) -> str:
        """Generate metrics dashboard."""
        total_articles = metrics.get('total_articles', 0)
        total_topics = metrics.get('total_topics', 0)
        avg_quality = metrics.get('average_quality', 0)
        
        return f"""
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{total_articles}</div>
                <div class="metric-label">Articles Analyzed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{total_topics}</div>
                <div class="metric-label">Topics Covered</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_quality:.1%}</div>
                <div class="metric-label">Avg Quality</div>
            </div>
        </div>
        """
    
    @staticmethod
    def _generate_executive_summary(summary: str) -> str:
        """Generate executive summary section."""
        # Convert Markdown to HTML
        html_summary = HTMLNewsletterGenerator._convert_markdown_to_html(summary)
        
        return f"""
        <div class="section">
            <h2 class="section-title">📋 Executive Summary</h2>
            <div class="executive-summary">
                <p style="margin: 10px 0;">{html_summary}</p>
            </div>
        </div>
        """
    
    @staticmethod
    def _generate_charts_section(chart_images: Dict[str, str]) -> str:
        """Generate charts section with embedded images."""
        if not chart_images:
            return ""
        
        html = """
        <div class="section">
            <h2 class="section-title">📊 Analytics Dashboard</h2>
        """
        
        # Add dashboard chart if available
        if chart_images.get('dashboard'):
            chart_path = chart_images['dashboard']
            try:
                with open(chart_path, 'rb') as img_file:
                    import base64
                    img_data = base64.b64encode(img_file.read()).decode()
                    html += f"""
            <div class="chart-container">
                <img src="data:image/png;base64,{img_data}" alt="Analytics Dashboard" />
            </div>
            """
            except Exception as e:
                html += f"""
            <div class="chart-container">
                <p style="color: #999;">Dashboard chart not available</p>
            </div>
            """
        
        # Add other charts in a grid
        other_charts = []
        chart_titles = {
            'distribution': '📈 Article Distribution by Topic',
            'quality_gauge': '🎯 Overall Quality Score',
            'quality_by_topic': '⭐ Quality Scores by Topic'
        }
        
        for chart_key in ['distribution', 'quality_gauge', 'quality_by_topic']:
            if chart_images.get(chart_key):
                chart_path = chart_images[chart_key]
                try:
                    with open(chart_path, 'rb') as img_file:
                        import base64
                        img_data = base64.b64encode(img_file.read()).decode()
                        html += f"""
            <div class="chart-container">
                <h3>{chart_titles.get(chart_key, 'Chart')}</h3>
                <img src="data:image/png;base64,{img_data}" alt="{chart_titles.get(chart_key, 'Chart')}" />
            </div>
            """
                except Exception as e:
                    pass
        
        html += """
        </div>
        """
        return html
    
    @staticmethod
    def _generate_topics_section(topic_summaries: List[Dict[str, Any]]) -> str:
        """Generate topics section with cards."""
        html = f"""
        <div class="section">
            <h2 class="section-title">🔍 Detailed Analysis</h2>
        """
        
        for idx, topic in enumerate(topic_summaries, 1):
            quality_score = topic.get('quality_score', 0.75)
            quality_class = 'high' if quality_score >= 0.7 else ('medium' if quality_score >= 0.5 else 'low')
            quality_text = f"{quality_score:.0%}"
            
            # Convert overview Markdown to HTML
            overview = topic.get('overview', 'No overview available')
            overview_html = HTMLNewsletterGenerator._convert_markdown_to_html(overview)
            
            html += f"""
            <div class="topic-card">
                <h3 class="topic-title">
                    <span class="topic-icon">{idx}</span>
                    {topic.get('topic_name', 'Unknown Topic')}
                    <span class="quality-badge {quality_class}">Quality: {quality_text}</span>
                </h3>
                
                <div class="topic-overview">
                    <p style="margin: 10px 0;">{overview_html}</p>
                </div>
                
                <div class="key-findings">
                    <h4>🎯 Key Findings</h4>
                    <ul>
            """
            
            for finding in topic.get('key_findings', [])[:5]:
                # Convert each finding's Markdown to HTML
                finding_html = HTMLNewsletterGenerator._convert_markdown_to_html(finding)
                html += f"<li>{finding_html}</li>\n"
            
            html += """
                    </ul>
                </div>
            """
            
            # Add trends if available
            trends = topic.get('notable_trends', [])
            if trends:
                html += """
                <div class="trends">
                    <h4>📈 Notable Trends</h4>
                    <ul>
                """
                for trend in trends[:3]:
                    # Convert each trend's Markdown to HTML
                    trend_html = HTMLNewsletterGenerator._convert_markdown_to_html(trend)
                    html += f"<li>{trend_html}</li>\n"
                html += """
                    </ul>
                </div>
                """
            
            # Add top articles with links
            articles = topic.get('top_articles', [])
            if articles:
                html += """
                <div class="articles-section">
                    <h4>📚 Top Articles</h4>
                    <ol class="articles-list">
                """
                for article in articles[:5]:
                    title = article.get('title', 'Untitled')
                    # Convert any Markdown in title to HTML (remove ** formatting)
                    title_html = HTMLNewsletterGenerator._convert_markdown_to_html(title)
                    url = article.get('url', '#')
                    source = article.get('source', 'Unknown Source')
                    relevance = article.get('relevance_score', 0)
                    
                    html += f"""
                    <li class="article-item">
                        <a href="{url}" target="_blank" class="article-link">
                            {title_html}
                        </a>
                        <span class="article-meta">
                            {source} • Relevance: {relevance:.0%}
                        </span>
                    </li>
                    """
                html += """
                    </ol>
                </div>
                """
            
            html += "</div>\n"
        
        html += "</div>"
        return html
    
    @staticmethod
    def _generate_glossary_section(glossary: Dict[str, Any]) -> str:
        """Generate glossary section with AI-powered definitions."""
        if not glossary or not glossary.get('entries'):
            return ""

        entries = glossary.get('entries', [])
        if not entries:
            return ""

        html = """
        <div class="glossary-section">
            <h2 class="glossary-title">📖 Medical Glossary</h2>
            <p class="glossary-subtitle">Key medical and AI terms from this cancer research newsletter</p>
            <div class="glossary-grid">
        """

        for entry in entries[:15]:  # Limit to 15 terms
            term = entry.get('term', 'Unknown')
            entity_type = entry.get('entity_type', 'term').replace('_', ' ').title()
            definition = entry.get('definition', 'Definition not available.')
            related_terms = entry.get('related_terms', [])

            html += f"""
            <div class="glossary-item">
                <div class="glossary-term">
                    {term}
                    <span class="glossary-type">{entity_type}</span>
                </div>
                <div class="glossary-definition">
                    {definition}
                </div>
            """

            if related_terms:
                html += """
                <div class="glossary-related">
                    <strong>Related:</strong> """
                html += ", ".join(related_terms[:3])
                html += """
                </div>
                """

            html += """
            </div>
            """

        html += """
            </div>
        </div>
        """
        return html

    @staticmethod
    def _generate_footer() -> str:
        """Generate newsletter footer."""
        year = datetime.now().year
        return f"""
        <div class="footer">
            <p><strong>Stay Informed. Stay Ahead.</strong></p>
            <p>Powered by AI • Generated with LangGraph</p>
            <p>© {year} AI in Cancer Care Research Initiative</p>
        </div>
        """


def save_html_newsletter(
    html_content: str,
    output_path: str
) -> str:
    """Save HTML newsletter to file.
    
    Args:
        html_content: HTML string
        output_path: Path to save the file
        
    Returns:
        Path to saved file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return str(output_file)



