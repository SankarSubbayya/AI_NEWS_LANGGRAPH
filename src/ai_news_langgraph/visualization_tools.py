"""
Visualization tools for generating charts, diagrams, and images for newsletters.
"""

import os
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class NewsletterVisualizer:
    """Generate charts and diagrams for newsletter content."""

    def __init__(self, output_dir: str = "outputs/images"):
        """
        Initialize the visualizer.

        Args:
            output_dir: Directory to save generated images
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Try importing visualization libraries
        self._check_dependencies()

    def _check_dependencies(self):
        """Check if visualization libraries are available."""
        self.has_matplotlib = False
        self.has_plotly = False
        self.has_pillow = False

        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            self.has_matplotlib = True
        except ImportError:
            logger.warning("matplotlib not available")

        try:
            import plotly
            self.has_plotly = True
        except ImportError:
            logger.warning("plotly not available")

        try:
            from PIL import Image
            self.has_pillow = True
        except ImportError:
            logger.warning("Pillow not available")

    def create_topic_trends_chart(
        self,
        topic_name: str,
        trends: List[str],
        article_count: int
    ) -> Optional[str]:
        """
        Create a simple trends visualization chart.

        Args:
            topic_name: Name of the topic
            trends: List of trend descriptions
            article_count: Number of articles analyzed

        Returns:
            Path to generated chart image or None
        """
        if not self.has_matplotlib:
            logger.warning("Cannot create chart: matplotlib not available")
            return None

        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches

            # Create figure
            fig, ax = plt.subplots(figsize=(10, 6))

            # Create a simple bar chart showing trend importance
            trend_labels = [f"Trend {i+1}" for i in range(len(trends[:5]))]
            trend_scores = [1.0 - (i * 0.15) for i in range(len(trends[:5]))]

            colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
            bars = ax.barh(trend_labels, trend_scores, color=colors[:len(trend_labels)])

            # Styling
            ax.set_xlabel('Relevance Score', fontsize=12)
            ax.set_title(f'{topic_name} - Key Trends Analysis', fontsize=14, fontweight='bold')
            ax.set_xlim(0, 1.0)

            # Add grid
            ax.grid(axis='x', alpha=0.3, linestyle='--')

            # Add text annotation
            ax.text(
                0.5, -0.15, f'Based on {article_count} articles analyzed',
                transform=ax.transAxes,
                ha='center',
                fontsize=10,
                style='italic',
                color='gray'
            )

            plt.tight_layout()

            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trends_{topic_name.replace(' ', '_')}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)

            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Created trends chart: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to create trends chart: {e}")
            return None

    def create_topic_distribution_chart(
        self,
        topics_data: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Create a chart showing distribution of articles across topics.

        Args:
            topics_data: List of topic information with article counts

        Returns:
            Path to generated chart or None
        """
        if not self.has_matplotlib:
            return None

        try:
            import matplotlib.pyplot as plt

            # Extract data
            topic_names = [t.get('name', 'Unknown')[:20] for t in topics_data[:8]]
            article_counts = [len(t.get('articles', [])) for t in topics_data[:8]]

            # Create pie chart
            fig, ax = plt.subplots(figsize=(10, 8))

            colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c',
                     '#9b59b6', '#1abc9c', '#34495e', '#e67e22']

            wedges, texts, autotexts = ax.pie(
                article_counts,
                labels=topic_names,
                autopct='%1.1f%%',
                colors=colors[:len(topic_names)],
                startangle=90
            )

            # Styling
            ax.set_title('Article Distribution by Topic', fontsize=14, fontweight='bold', pad=20)

            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_weight('bold')

            plt.tight_layout()

            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"distribution_{timestamp}.png")

            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Created distribution chart: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to create distribution chart: {e}")
            return None

    def create_quality_metrics_chart(
        self,
        topics_data: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Create a chart showing quality scores across topics.

        Args:
            topics_data: List of topic information with quality scores

        Returns:
            Path to generated chart or None
        """
        if not self.has_matplotlib:
            return None

        try:
            import matplotlib.pyplot as plt
            import numpy as np

            # Extract data
            topic_names = [t.get('name', 'Unknown')[:15] for t in topics_data[:8]]
            quality_scores = [t.get('quality_score', 0.5) * 100 for t in topics_data[:8]]

            # Create bar chart
            fig, ax = plt.subplots(figsize=(12, 6))

            # Color bars based on quality
            colors = ['#2ecc71' if s >= 80 else '#f39c12' if s >= 60 else '#e74c3c'
                     for s in quality_scores]

            bars = ax.bar(topic_names, quality_scores, color=colors)

            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom',
                    fontsize=9, fontweight='bold'
                )

            # Styling
            ax.set_ylabel('Quality Score (%)', fontsize=12)
            ax.set_title('Content Quality by Topic', fontsize=14, fontweight='bold')
            ax.set_ylim(0, 100)
            ax.grid(axis='y', alpha=0.3, linestyle='--')

            # Rotate x-axis labels
            plt.xticks(rotation=45, ha='right')

            # Add quality thresholds
            ax.axhline(y=80, color='#2ecc71', linestyle='--', alpha=0.5, linewidth=1)
            ax.axhline(y=60, color='#f39c12', linestyle='--', alpha=0.5, linewidth=1)

            plt.tight_layout()

            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"quality_{timestamp}.png")

            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close()

            logger.info(f"Created quality metrics chart: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to create quality chart: {e}")
            return None

    def create_header_image(
        self,
        title: str = "AI in Cancer Care Newsletter",
        subtitle: str = None
    ) -> Optional[str]:
        """
        Create a simple header image for the newsletter.

        Args:
            title: Main title text
            subtitle: Subtitle text

        Returns:
            Path to generated header image or None
        """
        if not self.has_pillow:
            return None

        try:
            from PIL import Image, ImageDraw, ImageFont

            # Create image
            width, height = 800, 200
            img = Image.new('RGB', (width, height), color='#2c3e50')
            draw = ImageDraw.Draw(img)

            # Try to use a default font
            try:
                # Try to load a nice font
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
            except:
                # Fallback to default
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()

            # Draw title
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 60), title, fill='#ecf0f1', font=title_font)

            # Draw subtitle if provided
            if subtitle:
                subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
                subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
                subtitle_x = (width - subtitle_width) // 2
                draw.text((subtitle_x, 120), subtitle, fill='#3498db', font=subtitle_font)

            # Add decorative line
            draw.rectangle([(50, 40), (750, 42)], fill='#3498db')
            draw.rectangle([(50, 158), (750, 160)], fill='#3498db')

            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"header_{timestamp}.png")

            img.save(filepath, 'PNG')

            logger.info(f"Created header image: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to create header image: {e}")
            return None

    def create_infographic_summary(
        self,
        total_articles: int,
        total_topics: int,
        avg_quality: float,
        duration_seconds: float
    ) -> Optional[str]:
        """
        Create an infographic summarizing key metrics.

        Args:
            total_articles: Total number of articles processed
            total_topics: Total number of topics covered
            avg_quality: Average quality score
            duration_seconds: Processing duration

        Returns:
            Path to generated infographic or None
        """
        if not self.has_matplotlib:
            return None

        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.axis('off')

            # Create boxes for metrics
            metrics = [
                ("Articles Analyzed", str(total_articles), '#3498db'),
                ("Topics Covered", str(total_topics), '#2ecc71'),
                ("Avg Quality Score", f"{avg_quality:.1%}", '#f39c12'),
                ("Processing Time", f"{duration_seconds:.1f}s", '#9b59b6')
            ]

            y_pos = 0.8
            for label, value, color in metrics:
                # Draw box
                box = mpatches.FancyBboxPatch(
                    (0.1, y_pos - 0.08), 0.8, 0.15,
                    boxstyle="round,pad=0.01",
                    edgecolor=color,
                    facecolor=color,
                    alpha=0.3,
                    linewidth=2
                )
                ax.add_patch(box)

                # Add text
                ax.text(0.5, y_pos + 0.05, value,
                       ha='center', va='center',
                       fontsize=24, fontweight='bold',
                       color=color)
                ax.text(0.5, y_pos - 0.02, label,
                       ha='center', va='center',
                       fontsize=12,
                       color='#34495e')

                y_pos -= 0.23

            # Title
            ax.text(0.5, 0.95, 'Newsletter Metrics',
                   ha='center', va='center',
                   fontsize=18, fontweight='bold',
                   color='#2c3e50')

            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.output_dir, f"infographic_{timestamp}.png")

            plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
            plt.close()

            logger.info(f"Created infographic: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to create infographic: {e}")
            return None
