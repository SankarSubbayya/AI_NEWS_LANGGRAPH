"""Plotly visualization generators for AI News newsletter."""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
from pathlib import Path
import json


class NewsletterVisualizations:
    """Generate interactive and static visualizations for newsletters."""
    
    @staticmethod
    def create_topic_distribution_chart(
        topic_summaries: List[Dict[str, Any]],
        output_path: str = None
    ) -> str:
        """Create a bar chart showing article distribution by topic.
        
        Args:
            topic_summaries: List of topic summary dicts
            output_path: Optional path to save the chart
            
        Returns:
            Path to saved chart image
        """
        topics = [t.get('topic_name', 'Unknown') for t in topic_summaries]
        article_counts = [len(t.get('top_articles', [])) for t in topic_summaries]
        
        fig = go.Figure(data=[
            go.Bar(
                x=topics,
                y=article_counts,
                marker=dict(
                    color=article_counts,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Articles")
                ),
                text=article_counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=dict(
                text='<b>Article Distribution by Topic</b>',
                font=dict(size=20, color='#333')
            ),
            xaxis_title='Topics',
            yaxis_title='Number of Articles',
            template='plotly_white',
            height=500,
            font=dict(family="Arial, sans-serif", size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        if output_path:
            fig.write_image(output_path, width=1000, height=500)
            return output_path
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_quality_metrics_chart(
        topic_summaries: List[Dict[str, Any]],
        output_path: str = None
    ) -> str:
        """Create a gauge chart showing quality metrics.
        
        Args:
            topic_summaries: List of topic summary dicts
            output_path: Optional path to save the chart
            
        Returns:
            Path to saved chart image or HTML
        """
        # Calculate average quality
        quality_scores = [t.get('quality_score', 0.75) for t in topic_summaries]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.75
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_quality * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "<b>Overall Content Quality</b>", 'font': {'size': 24}},
            delta={'reference': 70, 'suffix': "%"},
            gauge={
                'axis': {'range': [None, 100], 'ticksuffix': "%"},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffcccb"},
                    {'range': [50, 70], 'color': "#ffffcc"},
                    {'range': [70, 100], 'color': "#90ee90"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            template='plotly_white',
            font=dict(family="Arial, sans-serif"),
        )
        
        if output_path:
            fig.write_image(output_path, width=600, height=400)
            return output_path
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_quality_by_topic_chart(
        topic_summaries: List[Dict[str, Any]],
        output_path: str = None
    ) -> str:
        """Create a horizontal bar chart showing quality scores by topic.
        
        Args:
            topic_summaries: List of topic summary dicts
            output_path: Optional path to save the chart
            
        Returns:
            Path to saved chart image or HTML
        """
        topics = [t.get('topic_name', 'Unknown')[:30] for t in topic_summaries]
        quality_scores = [t.get('quality_score', 0.75) * 100 for t in topic_summaries]
        
        # Color based on quality threshold
        colors = ['#90ee90' if q >= 70 else '#ffffcc' if q >= 50 else '#ffcccb' 
                  for q in quality_scores]
        
        fig = go.Figure(data=[
            go.Bar(
                y=topics,
                x=quality_scores,
                orientation='h',
                marker=dict(color=colors),
                text=[f"{q:.1f}%" for q in quality_scores],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=dict(
                text='<b>Quality Score by Topic</b>',
                font=dict(size=20, color='#333')
            ),
            xaxis_title='Quality Score (%)',
            yaxis_title='Topics',
            template='plotly_white',
            height=400,
            xaxis=dict(range=[0, 100]),
            font=dict(family="Arial, sans-serif", size=12),
        )
        
        if output_path:
            fig.write_image(output_path, width=800, height=400)
            return output_path
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_timeline_chart(
        topic_summaries: List[Dict[str, Any]],
        output_path: str = None
    ) -> str:
        """Create a timeline showing research progression.
        
        Args:
            topic_summaries: List of topic summary dicts
            output_path: Optional path to save the chart
            
        Returns:
            Path to saved chart image or HTML
        """
        topics = [t.get('topic_name', 'Unknown') for t in topic_summaries]
        article_counts = [len(t.get('top_articles', [])) for t in topic_summaries]
        
        # Create scatter plot with size based on article count
        fig = go.Figure()
        
        for idx, (topic, count) in enumerate(zip(topics, article_counts)):
            fig.add_trace(go.Scatter(
                x=[idx],
                y=[count],
                mode='markers+text',
                marker=dict(
                    size=count * 5,
                    color=idx,
                    colorscale='Viridis',
                    showscale=False,
                    line=dict(width=2, color='white')
                ),
                text=topic,
                textposition='top center',
                name=topic,
                hovertemplate=f'<b>{topic}</b><br>Articles: {count}<extra></extra>'
            ))
        
        fig.update_layout(
            title=dict(
                text='<b>Research Coverage Timeline</b>',
                font=dict(size=20, color='#333')
            ),
            xaxis=dict(
                title='Research Areas',
                showgrid=False,
                showticklabels=False
            ),
            yaxis_title='Number of Articles',
            template='plotly_white',
            height=500,
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=12),
        )
        
        if output_path:
            fig.write_image(output_path, width=1000, height=500)
            return output_path
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    @staticmethod
    def create_summary_dashboard(
        topic_summaries: List[Dict[str, Any]],
        metrics: Dict[str, Any],
        output_path: str = None
    ) -> str:
        """Create a comprehensive dashboard with multiple charts.
        
        Args:
            topic_summaries: List of topic summary dicts
            metrics: Metrics dictionary
            output_path: Optional path to save the chart
            
        Returns:
            Path to saved chart image or HTML
        """
        from plotly.subplots import make_subplots
        
        topics = [t.get('topic_name', 'Unknown')[:20] for t in topic_summaries]
        article_counts = [len(t.get('top_articles', [])) for t in topic_summaries]
        quality_scores = [t.get('quality_score', 0.75) * 100 for t in topic_summaries]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                '<b>Article Distribution</b>',
                '<b>Quality Scores</b>',
                '<b>Average Quality</b>',
                '<b>Coverage Metrics</b>'
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "indicator"}, {"type": "table"}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Article distribution
        fig.add_trace(
            go.Bar(x=topics, y=article_counts, marker=dict(color='#667eea'), name='Articles'),
            row=1, col=1
        )
        
        # Quality scores
        colors = ['#90ee90' if q >= 70 else '#ffffcc' if q >= 50 else '#ffcccb' 
                  for q in quality_scores]
        fig.add_trace(
            go.Bar(x=topics, y=quality_scores, marker=dict(color=colors), name='Quality'),
            row=1, col=2
        )
        
        # Average quality gauge
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 75
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=avg_quality,
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#667eea"}},
                domain={'x': [0, 1], 'y': [0, 1]}
            ),
            row=2, col=1
        )
        
        # Metrics table
        fig.add_trace(
            go.Table(
                header=dict(
                    values=['<b>Metric</b>', '<b>Value</b>'],
                    fill_color='#667eea',
                    font=dict(color='white', size=14),
                    align='left'
                ),
                cells=dict(
                    values=[
                        ['Total Articles', 'Total Topics', 'Avg Quality', 'Duration'],
                        [
                            metrics.get('total_articles', 0),
                            metrics.get('total_topics', 0),
                            f"{avg_quality:.1f}%",
                            f"{metrics.get('duration_seconds', 0):.0f}s"
                        ]
                    ],
                    fill_color='white',
                    align='left'
                )
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title=dict(
                text='<b>Newsletter Analytics Dashboard</b>',
                font=dict(size=24, color='#333'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            height=800,
            template='plotly_white',
            font=dict(family="Arial, sans-serif", size=12),
        )
        
        fig.update_xaxes(tickangle=-45, row=1, col=1)
        fig.update_xaxes(tickangle=-45, row=1, col=2)
        
        if output_path:
            fig.write_image(output_path, width=1200, height=800)
            return output_path
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')


def generate_all_charts(
    topic_summaries: List[Dict[str, Any]],
    metrics: Dict[str, Any],
    output_dir: str = "outputs/charts"
) -> Dict[str, str]:
    """Generate all newsletter charts.
    
    Args:
        topic_summaries: List of topic summary dicts
        metrics: Metrics dictionary
        output_dir: Directory to save charts
        
    Returns:
        Dictionary mapping chart names to file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    viz = NewsletterVisualizations()
    chart_paths = {}
    
    try:
        # Try to generate PNG images (requires kaleido)
        chart_paths['distribution'] = viz.create_topic_distribution_chart(
            topic_summaries, 
            str(output_path / "topic_distribution.png")
        )
        
        chart_paths['quality_gauge'] = viz.create_quality_metrics_chart(
            topic_summaries,
            str(output_path / "quality_gauge.png")
        )
        
        chart_paths['quality_by_topic'] = viz.create_quality_by_topic_chart(
            topic_summaries,
            str(output_path / "quality_by_topic.png")
        )
        
        chart_paths['dashboard'] = viz.create_summary_dashboard(
            topic_summaries,
            metrics,
            str(output_path / "dashboard.png")
        )
        
    except Exception as e:
        # Fall back to HTML if image generation fails
        print(f"Warning: Could not generate PNG charts: {e}")
        print("Generating HTML charts instead...")
        
        chart_paths['distribution'] = viz.create_topic_distribution_chart(topic_summaries)
        chart_paths['quality_gauge'] = viz.create_quality_metrics_chart(topic_summaries)
        chart_paths['quality_by_topic'] = viz.create_quality_by_topic_chart(topic_summaries)
        chart_paths['dashboard'] = viz.create_summary_dashboard(topic_summaries, metrics)
    
    return chart_paths



