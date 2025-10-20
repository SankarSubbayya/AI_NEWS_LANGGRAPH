"""
Node implementations with centralized prompts following metamorphosis pattern.

This module replaces agent classes with direct LLM calls using
the centralized prompt registry, implementing the metamorphosis
pattern of direct tool and prompt access.
"""

from typing import Dict, Any, List, Optional
import time
from datetime import datetime
import logging
import os
from dateutil import parser as date_parser

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Try to import from state.py, fallback to state_base.py
try:
    from .state import (
        WorkflowState,
        ArticleModel,
        TopicSearchResultModel,
        TopicSummaryModel,
        AgentTaskResultModel,
        NewsletterContentModel
    )
except ImportError:
    from .state_base import (
        WorkflowState,
        ArticleModel,
        TopicSearchResultModel,
        TopicSummaryModel,
        AgentTaskResultModel,
        NewsletterContentModel
    )
from .prompts import prompt_registry, get_prompt
from .tools import NewsSearchTool, DocumentProcessor, FileManager
from .tools_direct import DirectToolRegistry
from .task_loader import load_task_config
from .visualization_tools import NewsletterVisualizer

# Initialize logger first (before using it)
logger = logging.getLogger(__name__)

# Import Phoenix observability
try:
    from .observability import phoenix_observer, trace_node
    PHOENIX_ENABLED = True
    logger.info("Phoenix observability enabled")
except ImportError:
    logger.warning("Phoenix observability not available. Install with: pip install arize-phoenix")
    PHOENIX_ENABLED = False
    # Create dummy decorator if Phoenix not available
    def trace_node(name):
        def decorator(func):
            return func
        return decorator


class WorkflowNodesV2:
    """
    Centralized node implementations using direct prompt access.
    Replaces agent classes with direct LLM calls for better control.
    """

    def __init__(self, model: str = None, temperature: float = 0.7):
        """
        Initialize the workflow nodes with LLM and tools.

        Args:
            model: OpenAI model to use (defaults to env var or gpt-4o-mini)
            temperature: LLM temperature setting
        """
        # Store LLM configuration (lazy initialization)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = temperature
        self._llm = None  # Will be initialized on first use

        # Initialize tools
        self.news_tool = NewsSearchTool()
        self.doc_processor = DocumentProcessor()
        self.file_manager = FileManager()

        # Initialize direct tool registry
        self.tool_registry = DirectToolRegistry()

        # Initialize visualizer
        self.visualizer = NewsletterVisualizer()

        # Load prompts - Use COSTAR prompts for better quality
        try:
            from .costar_prompts import EnhancedPromptRegistry
            self.prompts = EnhancedPromptRegistry(use_costar=True)
            logger.info("✅ Using COSTAR enhanced prompts for all operations")
        except Exception as e:
            logger.warning(f"Failed to load COSTAR prompts: {e}, using standard prompts")
            self.prompts = prompt_registry

        logger.info(f"Initialized WorkflowNodesV2 with model: {self.model}")
    
    @property
    def llm(self):
        """Lazy initialization of LLM (only when needed)."""
        if self._llm is None:
            if not os.getenv('OPENAI_API_KEY'):
                raise ValueError(
                    "OPENAI_API_KEY environment variable must be set to use the workflow. "
                    "Set it with: export OPENAI_API_KEY='your-key-here'"
                )
            self._llm = ChatOpenAI(model=self.model, temperature=self.temperature)
            logger.info(f"LLM initialized: {self.model}")
        return self._llm

    @trace_node("initializer")
    def initialize_workflow(self, state: dict) -> dict:
        """
        Initialize the workflow state with configuration.

        Synchronous version for LangGraph compatibility.
        LangGraph passes state as dict, not Pydantic model.

        Args:
            state: Current workflow state (dict)

        Returns:
            Updated workflow state (dict)
        """
        try:
            logger.info("Initializing workflow")

            # Load topics configuration
            topics_path = state.get("topics_path", "src/ai_news_langgraph/config/tasks.yaml")
            topics_config = self._load_topics_config(topics_path)

            state["topics_config"] = topics_config
            state["main_topic"] = topics_config.get("main_topic", "AI in Cancer Care")
            state["current_stage"] = "initialized"
            state["current_topic_index"] = 0

            logger.info(f"Workflow initialized with {len(topics_config.get('topics', []))} topics")

            return state

        except Exception as e:
            error_msg = f"Initialization failed: {str(e)}"
            logger.error(error_msg)
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(error_msg)
            state["current_stage"] = "failed"
            return state
    
    async def initialize_workflow_async(self, state: WorkflowState) -> WorkflowState:
        """
        Async version of initialize_workflow.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated workflow state
        """
        return self.initialize_workflow(state)

    @trace_node("research_agent")
    async def fetch_news_for_topic(self, state: dict) -> dict:
        """
        Fetch news articles for the current topic using direct prompt access.
        
        LangGraph passes state as dict, not Pydantic model.

        Args:
            state: Current workflow state (dict)

        Returns:
            Updated workflow state (dict)
        """
        task_config = load_task_config('fetch_ai_news')
        start_time = time.time()
        
        try:
            # Work with dict directly
            topics_config = state.get("topics_config", {})
            topics = topics_config.get("topics", [])
            current_index = state.get("current_topic_index", 0)

            if current_index >= len(topics):
                logger.warning(f"No more topics to fetch (index {current_index})")
                if "warnings" not in state:
                    state["warnings"] = []
                state["warnings"].append(f"No more topics to fetch (index {current_index})")
                return state

            current_topic = topics[current_index]
            logger.info(f"Fetching news for topic: {current_topic['name']}")

            # Generate optimized search query using LLM
            query = await self._generate_search_query(current_topic)

            # Search for articles
            articles_data = self.news_tool.search(query, max_results=15)

            # Score articles using direct prompt
            articles = []
            for article_data in articles_data:
                relevance = await self._analyze_relevance(article_data, current_topic)

                # Handle invalid published_date formats gracefully
                published_date_value = None
                raw_date = article_data.get("published_date")
                
                if raw_date:
                    try:
                        # Try to parse various date formats
                        if isinstance(raw_date, str):
                            # Handle empty strings
                            if raw_date.strip():
                                published_date_value = date_parser.parse(raw_date)
                            else:
                                published_date_value = None
                        elif isinstance(raw_date, datetime):
                            published_date_value = raw_date
                        else:
                            published_date_value = None
                    except (ValueError, TypeError, date_parser.ParserError) as e:
                        logger.debug(f"Could not parse date '{raw_date}': {e}")
                        published_date_value = None
                
                try:
                    article = ArticleModel(
                        title=article_data.get("title", ""),
                        url=article_data.get("url", ""),
                        source=article_data.get("source"),
                        content=article_data.get("content"),
                        summary=article_data.get("summary"),
                        published_date=published_date_value,
                        relevance_score=relevance
                    )
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Error creating article model: {e}")
                    # Create article without problematic fields
                    article = ArticleModel(
                        title=article_data.get("title", ""),
                        url=article_data.get("url", ""),
                        source=article_data.get("source"),
                        content=article_data.get("content"),
                        summary=article_data.get("summary"),
                        published_date=None,
                        relevance_score=relevance
                    )
                    articles.append(article)

            # Sort by relevance
            articles.sort(key=lambda x: x.relevance_score or 0, reverse=True)
            top_articles = articles[:10]

            # Create topic result as dict
            topic_result = {
                "topic_name": current_topic["name"],
                "topic_description": current_topic["description"],
                "search_query": query,
                "articles": [a.model_dump() for a in top_articles]
            }

            # Update state
            if "topic_results" not in state:
                state["topic_results"] = []
            state["topic_results"].append(topic_result)
            
            state["total_articles_fetched"] = state.get("total_articles_fetched", 0) + len(top_articles)

            # Record agent result as dict
            agent_result = {
                "task_name": "fetch_news_for_topic",
                "agent_name": "research_node",
                "status": "success",
                "output": f"Fetched {len(top_articles)} articles for {current_topic['name']}",
                "execution_time": time.time() - start_time
            }
            
            if "agent_results" not in state:
                state["agent_results"] = []
            state["agent_results"].append(agent_result)

            state["current_stage"] = "fetching"
            logger.info(f"Successfully fetched {len(top_articles)} articles")

            return state

        except Exception as e:
            logger.error(f"Failed to fetch news: {str(e)}")
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Failed to fetch news: {str(e)}")
            return state

    async def _generate_search_query(self, topic: Dict[str, Any]) -> str:
        """Generate optimized search query for a topic."""
        if topic.get("query"):
            return topic["query"]

        # Simple query generation without LLM for now
        query = f"AI {topic['name']} {topic.get('description', '')} latest news research 2024"
        return query

    async def _analyze_relevance(self, article: Dict[str, Any], topic: Dict[str, Any]) -> float:
        """
        Analyze article relevance using direct prompt.

        Args:
            article: Article data
            topic: Topic information

        Returns:
            Relevance score (0-1)
        """
        try:
            # Get the relevance analysis prompt
            prompt = self.prompts.get_prompt("research_agent", "analyze_relevance")

            # Create the chain
            chain = prompt | self.llm | StrOutputParser()

            # Run the analysis
            result = await chain.ainvoke({
                "topic_name": topic["name"],
                "topic_description": topic.get("description", ""),
                "title": article.get("title", ""),
                "content": article.get("content", article.get("summary", ""))[:500]
            })

            # Parse the score
            try:
                score = float(result.strip())
                return max(0.0, min(1.0, score))  # Ensure between 0 and 1
            except:
                return 0.5  # Default score if parsing fails

        except Exception as e:
            logger.warning(f"Relevance analysis failed: {e}")
            return 0.5

    @trace_node("editor_agent")
    async def summarize_topic(self, state: dict) -> dict:
        """Create comprehensive summary using direct prompt access (dict-based)."""
        task_config = load_task_config('summarize_ai_news')
        start_time = time.time()
        
        try:
            current_index = state.get("current_topic_index", 0)
            topic_results = state.get("topic_results", [])

            if current_index >= len(topic_results):
                logger.warning("No topic result to summarize")
                if "warnings" not in state:
                    state["warnings"] = []
                state["warnings"].append("No topic result to summarize")
                state["current_topic_index"] = current_index + 1
                return state

            latest_result = topic_results[current_index]
            logger.info(f"Summarizing topic: {latest_result.get('topic_name', 'Unknown')}")

            # Get the summarization prompt (now using COSTAR prompts)
            prompt = self.prompts.get_prompt("editor_agent", "summarize_topic")

            # Prepare articles for summarization
            articles = latest_result.get("articles", [])[:5]

            # Format articles as structured JSON for COSTAR prompt
            # The prompt expects {articles_json} with title, summary, source, relevance
            import json
            articles_data = []
            for article in articles:
                articles_data.append({
                    "title": article.get("title", "Untitled"),
                    "source": article.get("source", "Unknown source"),
                    "summary": (article.get("summary") or article.get("content", "")[:300]) if (article.get("summary") or article.get("content")) else "No content available",
                    "relevance_score": f"{article.get('relevance_score', 0):.2f}"
                })

            articles_json = json.dumps(articles_data, indent=2)

            # Create the chain
            chain = prompt | self.llm | StrOutputParser()

            # Generate summary with variable names matching COSTAR prompt
            summary_result = await chain.ainvoke({
                "topic_name": latest_result.get("topic_name", "Unknown"),
                "topic_description": latest_result.get("topic_description", ""),
                "articles_json": articles_json  # Matches prompt variable name
            })

            # Extract key points using direct tool
            key_points_result = self.tool_registry.execute_tool(
                "extract_key_points",
                text=summary_result,
                max_points=5
            )
            key_points = key_points_result.output if key_points_result.success else []

            # Create topic summary as dict
            topic_summary = {
                "topic_name": latest_result.get("topic_name", "Unknown"),
                "overview": summary_result,
                "key_findings": key_points[:5],
                "notable_trends": self._extract_trends(summary_result),
                "top_articles": articles[:5],
                "quality_score": 0.75  # Default, will be updated in review
            }

            # Update state
            if "topic_summaries" not in state:
                state["topic_summaries"] = []
            state["topic_summaries"].append(topic_summary)
            
            state["total_topics_processed"] = state.get("total_topics_processed", 0) + 1

            # Record agent result
            agent_result = {
                "task_name": "summarize_topic",
                "agent_name": "editor_node",
                "status": "success",
                "output": f"Summarized {latest_result.get('topic_name', 'Unknown')}",
                "execution_time": time.time() - start_time
            }
            if "agent_results" not in state:
                state["agent_results"] = []
            state["agent_results"].append(agent_result)

            # Move to next topic
            state["current_topic_index"] = current_index + 1
            state["current_stage"] = "summarizing"

            logger.info(f"Successfully summarized topic {current_index + 1}")
            return state

        except Exception as e:
            logger.error(f"Failed to summarize topic: {e}")
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Failed to summarize: {str(e)}")
            # Increment to avoid infinite loop
            state["current_topic_index"] = state.get("current_topic_index", 0) + 1
            return state

    @trace_node("quality_reviewer")
    async def review_quality(self, state: dict) -> dict:
        """Review the quality of summaries using self-reviewer prompts (dict-based)."""
        start_time = time.time()

        try:
            logger.info("Reviewing summary quality")
            topic_summaries = state.get("topic_summaries", [])
            
            if not topic_summaries:
                logger.warning("No summaries to review")
                state["current_stage"] = "reviewing"
                return state

            # Get the quality evaluation prompt
            prompt = self.prompts.get_prompt("self_reviewer", "evaluate_quality")
            chain = prompt | self.llm | StrOutputParser()

            # Review each summary
            review_feedback = []
            for summary in topic_summaries:
                # Evaluate quality
                quality_result = await chain.ainvoke({
                    "content": summary.get("overview", "")
                })

                # Parse quality score (simplified)
                try:
                    if "score" in quality_result.lower():
                        import re
                        score_match = re.search(r'(\d+(?:\.\d+)?)', quality_result)
                        if score_match:
                            score = float(score_match.group(1))
                            # Normalize to 0-1 range if it's 0-100
                            if score > 1:
                                score = score / 100
                            summary["quality_score"] = score
                except:
                    summary["quality_score"] = 0.75  # Default score

                # Add feedback if quality is low
                if summary.get("quality_score", 0) < 0.7:
                    feedback = f"Low quality summary for {summary.get('topic_name', 'Unknown')}: score {summary.get('quality_score', 0):.2f}"
                    review_feedback.append(feedback)
                    logger.warning(feedback)

            # Calculate overall quality
            avg_quality = sum(s.get("quality_score", 0) for s in topic_summaries) / max(len(topic_summaries), 1)

            state["quality_reviews"] = {
                "average_quality": avg_quality,
                "reviewed_at": datetime.now().isoformat(),
                "feedback_count": len(review_feedback)
            }
            
            if "review_feedback" not in state:
                state["review_feedback"] = []
            state["review_feedback"].extend(review_feedback)

            # Record result
            agent_result = {
                "task_name": "review_quality",
                "agent_name": "self_reviewer_node",
                "status": "success",
                "output": f"Reviewed {len(topic_summaries)} summaries, avg quality: {avg_quality:.2f}",
                "execution_time": time.time() - start_time
            }
            if "agent_results" not in state:
                state["agent_results"] = []
            state["agent_results"].append(agent_result)

            state["current_stage"] = "reviewing"
            logger.info(f"Quality review complete: avg score {avg_quality:.2f}")

            return state

        except Exception as e:
            logger.error(f"Failed to review quality: {e}")
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Failed to review quality: {str(e)}")
            return state
    
    async def _review_quality_full(self, state: dict) -> dict:
        """
        Full review quality implementation (temporarily disabled).
        
        LangGraph passes state as dict, not Pydantic model.

        Args:
            state: Current workflow state (dict)

        Returns:
            Updated workflow state (dict)
        """
        start_time = time.time()
        
        try:
            # Convert dict to Pydantic model for easier manipulation
            state_obj = WorkflowState(**state)
            logger.info("Reviewing summary quality")

            # Get the quality evaluation prompt
            prompt = self.prompts.get_prompt("self_reviewer", "evaluate_quality")
            chain = prompt | self.llm | StrOutputParser()

            # Review each summary
            for summary in state_obj.topic_summaries:
                # Evaluate quality
                quality_result = await chain.ainvoke({
                    "content": summary.overview
                })

                # Parse quality score (simplified)
                try:
                    # Extract score from the result
                    if "score" in quality_result.lower():
                        import re
                        score_match = re.search(r'(\d+(?:\.\d+)?)', quality_result)
                        if score_match:
                            score = float(score_match.group(1))
                            # Normalize to 0-1 range if it's 0-100
                            if score > 1:
                                score = score / 100
                            summary.quality_score = score
                except:
                    summary.quality_score = 0.75  # Default score

                # Use direct tool for additional quality check
                review_result = self.tool_registry.execute_tool(
                    "evaluate_review_text",
                    text=summary.overview
                )

                if review_result.success and review_result.output:
                    # Merge scores
                    tool_score = review_result.output.get("quality_score", 0.75)
                    summary.quality_score = (summary.quality_score + tool_score) / 2

                # Add feedback if quality is low
                if summary.quality_score < 0.7:
                    feedback = f"Low quality summary for {summary.topic_name}: score {summary.quality_score:.2f}"
                    state_obj.review_feedback.append(feedback)
                    logger.warning(feedback)

            # Calculate overall quality
            avg_quality = sum(s.quality_score for s in state_obj.topic_summaries) / len(state_obj.topic_summaries)

            state_obj.quality_reviews = {
                "average_quality": avg_quality,
                "reviewed_at": datetime.now().isoformat(),
                "feedback_count": len(state_obj.review_feedback)
            }

            # Record result
            agent_result = AgentTaskResultModel(
                task_name="review_quality",
                agent_name="self_reviewer_node",
                status="success",
                output=f"Reviewed {len(state_obj.topic_summaries)} summaries, avg quality: {avg_quality:.2f}",
                execution_time=time.time() - start_time
            )
            state_obj.add_agent_result(agent_result)

            state_obj.current_stage = "reviewing"
            logger.info(f"Quality review complete: avg score {avg_quality:.2f}")

            return state_obj.model_dump()

        except Exception as e:
            logger.error(f"Quality review failed: {str(e)}")
            # Handle error even if state_obj wasn't created yet
            try:
                if 'state_obj' in locals():
                    error_msg = f"Quality review failed: {str(e)}"
                    state_obj.add_error(error_msg)
                    agent_result = AgentTaskResultModel(
                        task_name="review_quality",
                        agent_name="self_reviewer_node",
                        status="failed",
                        error=str(e),
                        execution_time=time.time() - start_time
                    )
                    state_obj.add_agent_result(agent_result)
                    return state_obj.model_dump()
                else:
                    # State conversion failed, work with dict directly
                    if "errors" not in state:
                        state["errors"] = []
                    state["errors"].append(f"Quality review failed: {str(e)}")
                    return state
            except Exception as inner_e:
                logger.error(f"Error handling error: {inner_e}")
                return state

    @trace_node("chief_editor")
    async def generate_newsletter(self, state: dict) -> dict:
        """Generate the final newsletter with HTML, visualizations, and COSTAR prompts."""
        task_config = load_task_config('draft_html_newsletter')
        start_time = time.time()

        try:
            logger.info("Generating enhanced newsletter with HTML and visualizations")
            topic_summaries = state.get("topic_summaries", [])

            if not topic_summaries:
                logger.warning("No topics available for newsletter generation")
                if "warnings" not in state:
                    state["warnings"] = []
                state["warnings"].append("No topics available for newsletter generation")
                state["current_stage"] = "completed"
                return state

            logger.info(f"Generating newsletter with {len(topic_summaries)} topics")

            # Create executive summary using COSTAR prompts (already loaded in __init__)
            exec_prompt = self.prompts.get_prompt("editor_agent", "create_executive_summary")
            exec_chain = exec_prompt | self.llm | StrOutputParser()

            topics_summaries = "\n\n".join([
                f"**{s.get('topic_name', 'Unknown')}**\n{s.get('overview', '')[:200]}..."
                for s in topic_summaries
            ])

            # Get current date for the newsletter
            current_date = datetime.now().strftime("%B %d, %Y")

            exec_summary = await exec_chain.ainvoke({
                "topics_summaries": topics_summaries,
                "current_date": current_date
            })

            state["executive_summary"] = exec_summary

            # Calculate metrics
            metrics = {
                "total_articles": state.get("total_articles_fetched", 0),
                "total_topics": len(topic_summaries),
                "average_quality": sum(s.get('quality_score', 0.75) for s in topic_summaries) / max(len(topic_summaries), 1),
                "duration_seconds": time.time() - start_time
            }

            # Generate visualizations using Plotly
            logger.info("Generating visualizations...")
            chart_paths = {}
            try:
                from .visualizations import generate_all_charts
                chart_paths = generate_all_charts(topic_summaries, metrics)
                logger.info(f"Generated {len(chart_paths)} visualization charts")
            except Exception as e:
                logger.warning(f"Failed to generate visualizations: {e}")

            # Generate Cover Images (DALL-E + Flux) and Flux Prompts
            logger.info("Generating cover images (DALL-E + Flux) and prompts...")
            cover_image_path = None
            flux_image_path = None
            flux_prompts_data = None

            try:
                from .cover_image_generator import CoverImageGenerator
                from .flux_prompt_generator import FluxPromptGenerator
                from .flux_image_generator import FluxImageGenerator

                topic_names = [s.get('topic_name', '') for s in topic_summaries]

                # Log topics being used for cover image
                logger.info(f"🎨 Cover image generation starting...")
                logger.info(f"  Main topic: {state.get('main_topic', 'AI in Cancer Care')}")
                logger.info(f"  Topics found: {len(topic_names)}")
                if topic_names:
                    logger.info(f"  Topic names: {', '.join(topic_names[:5])}")
                else:
                    logger.warning("  ⚠️ No topic names found in summaries!")
                logger.info(f"  Executive summary length: {len(exec_summary)} chars")
                logger.info(f"  First 100 chars of summary: {exec_summary[:100]}...")

                # Generate DALL-E image automatically
                cover_gen = CoverImageGenerator()
                cover_image_path = cover_gen.generate_cover_image(
                    executive_summary=exec_summary,
                    main_topic=state.get("main_topic", "AI in Cancer Care"),
                    topics=topic_names,
                    output_dir="outputs/images",
                    style="professional"  # Options: professional, modern, abstract, scientific
                )

                if cover_image_path:
                    logger.info(f"✓ DALL-E cover image generated: {cover_image_path}")
                else:
                    logger.warning("DALL-E cover image generation skipped or failed")

                # Generate Flux image automatically (if API token available)
                flux_img_gen = FluxImageGenerator()
                if flux_img_gen.enabled:
                    logger.info("🎨 Generating Flux cover image (this may take 10-30 seconds)...")
                    flux_image_path = flux_img_gen.generate_cover_image(
                        executive_summary=exec_summary,
                        main_topic=state.get("main_topic", "AI in Cancer Care"),
                        topics=topic_names,
                        output_dir="outputs/images",
                        style="professional"
                    )

                    if flux_image_path:
                        logger.info(f"✓ Flux cover image generated: {flux_image_path}")
                    else:
                        logger.warning("Flux cover image generation failed")
                else:
                    logger.info("⏭️  Flux image generation skipped (no REPLICATE_API_TOKEN)")
                    logger.info("   Get your token at: https://replicate.com/account/api-tokens")

                # Generate Flux prompts for manual use (always generate these as backup)
                flux_gen = FluxPromptGenerator()
                flux_prompts = flux_gen.generate_newsletter_cover_prompt(
                    executive_summary=exec_summary,
                    main_topic=state.get("main_topic", "AI in Cancer Care"),
                    topics=topic_names,
                    style="professional"
                )

                # Save Flux prompts to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                flux_output_dir = "outputs/flux_prompts"
                import os
                os.makedirs(flux_output_dir, exist_ok=True)

                flux_prompt_file = f"{flux_output_dir}/flux_prompts_{timestamp}.txt"
                with open(flux_prompt_file, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("FLUX AI IMAGE GENERATION PROMPTS\n")
                    f.write("=" * 80 + "\n\n")
                    f.write("Instructions:\n")
                    f.write("1. These prompts were used to auto-generate the Flux image\n")
                    f.write("2. You can also use them manually on CivitAI or Replicate\n")
                    f.write("3. For manual generation:\n")
                    f.write("   - Go to https://civitai.com/generate or https://replicate.com\n")
                    f.write("   - Copy POSITIVE PROMPT into main prompt field\n")
                    f.write("   - Copy NEGATIVE PROMPT into negative prompt field\n")
                    f.write("   - Select Flux Schnell (fast) or Flux Dev (quality)\n")
                    f.write("   - Generate and download\n\n")
                    f.write("=" * 80 + "\n")
                    f.write("POSITIVE PROMPT:\n")
                    f.write("=" * 80 + "\n")
                    f.write(flux_prompts['positive'] + "\n\n")
                    f.write("=" * 80 + "\n")
                    f.write("NEGATIVE PROMPT:\n")
                    f.write("=" * 80 + "\n")
                    f.write(flux_prompts['negative'] + "\n\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Topics: {', '.join(topic_names)}\n")
                    if flux_image_path:
                        f.write(f"Auto-Generated Image: {flux_image_path}\n")
                    f.write("=" * 80 + "\n")

                flux_prompts_data = {
                    'prompt_file': flux_prompt_file,
                    'positive': flux_prompts['positive'],
                    'negative': flux_prompts['negative'],
                    'flux_image_path': flux_image_path  # May be None if not generated
                }

                logger.info(f"✓ Flux prompts saved: {flux_prompt_file}")
                if not flux_image_path:
                    logger.info("  → Use these prompts on CivitAI for manual ultra-high-quality Flux images")

            except Exception as e:
                logger.warning(f"Failed to generate cover image/prompts: {e}")
                import traceback
                traceback.print_exc()

            # Generate Knowledge Graph and Glossary
            logger.info("Generating knowledge graph and glossary...")
            knowledge_graph_data = None
            glossary_data = None

            try:
                from .cancer_research_knowledge_graph import CancerResearchKnowledgeGraph
                from .glossary_generator import GlossaryGenerator

                # Build knowledge graph from newsletter content
                kg_builder = CancerResearchKnowledgeGraph()

                # Build the graph from executive summary and topic summaries
                kg_stats = kg_builder.build_from_newsletter(
                    executive_summary=exec_summary,
                    topic_summaries=topic_summaries
                )
                logger.info(f"Knowledge Graph: {kg_stats['total_entities']} entities, {kg_stats['total_relationships']} relationships")

                # Export knowledge graph
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                kg_output_dir = "outputs/knowledge_graphs"
                import os
                os.makedirs(kg_output_dir, exist_ok=True)

                kg_json_path = f"{kg_output_dir}/kg_{timestamp}.json"

                # Use the export method that actually exists
                kg_builder.export_to_json(kg_json_path)

                knowledge_graph_data = {
                    'stats': kg_stats,
                    'json_path': kg_json_path,
                    'graph_data': kg_stats  # Include the full graph data for Streamlit
                }

                logger.info(f"Knowledge graph exported to {kg_json_path}")

                # Generate glossary from knowledge graph with AI-powered definitions
                logger.info("Generating AI-powered glossary definitions...")
                importance_scores = kg_builder._calculate_entity_importance()

                # Use GlossaryGenerator to create AI-powered definitions
                glossary_gen = GlossaryGenerator(model="gpt-4o-mini", temperature=0.3)

                glossary_entries = []
                for entity, score, entity_type in importance_scores[:15]:  # Top 15 by importance
                    try:
                        # Get contexts where this entity appears
                        contexts = kg_builder.entity_contexts.get(entity, [])

                        # Get related terms from knowledge graph
                        related_terms = []
                        if entity in kg_builder.graph:
                            for targets in kg_builder.graph[entity].values():
                                related_terms.extend(targets[:3])  # Top 3 per relationship

                        # Generate AI-powered definition
                        definition = glossary_gen._generate_definition(
                            term=entity,
                            related_terms=related_terms[:5],  # Max 5 related terms
                            context=f"{state.get('main_topic', 'AI in Cancer Care')} - {entity_type.replace('_', ' ')}",
                            frequency=len(contexts)
                        )

                        glossary_entries.append({
                            'term': entity,
                            'entity_type': entity_type,
                            'importance_score': round(score, 2),
                            'definition': definition,
                            'related_terms': related_terms[:5],
                            'contexts': len(contexts)
                        })

                        logger.debug(f"  ✓ Generated definition for '{entity}' ({entity_type})")

                    except Exception as e:
                        logger.warning(f"Failed to generate definition for '{entity}': {e}")
                        # Fallback to basic definition
                        glossary_entries.append({
                            'term': entity,
                            'entity_type': entity_type,
                            'importance_score': round(score, 2),
                            'definition': f"A {entity_type.replace('_', ' ')} term in cancer research with AI applications.",
                            'related_terms': [],
                            'contexts': len(kg_builder.entity_contexts.get(entity, []))
                        })

                glossary_data = {
                    'entries': glossary_entries,
                    'total_terms': len(glossary_entries)
                }

                logger.info(f"Generated glossary with {glossary_data['total_terms']} high-importance terms")
                if glossary_entries:
                    logger.info(f"  Top term: '{glossary_entries[0]['term']}' (score: {glossary_entries[0]['importance_score']})")

            except Exception as e:
                logger.warning(f"Failed to generate knowledge graph/glossary: {e}")
                import traceback
                logger.debug(traceback.format_exc())

            # Generate HTML newsletter
            logger.info("Generating HTML newsletter...")
            try:
                from .html_generator import HTMLNewsletterGenerator, save_html_newsletter
                
                html_content = HTMLNewsletterGenerator.generate_newsletter_html(
                    executive_summary=exec_summary,
                    topic_summaries=topic_summaries,
                    main_topic=state.get("main_topic", "AI in Cancer Care"),
                    metrics=metrics,
                    chart_images=chart_paths,
                    cover_image=cover_image_path,  # Add cover image
                    glossary=glossary_data,  # Add glossary
                    knowledge_graph=knowledge_graph_data  # Add knowledge graph
                )
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                outputs_dir = "outputs"
                
                import os
                os.makedirs(outputs_dir, exist_ok=True)
                
                html_path = f"{outputs_dir}/newsletter_{timestamp}.html"
                save_html_newsletter(html_content, html_path)
                logger.info(f"HTML newsletter saved to {html_path}")
                
            except Exception as e:
                logger.error(f"Failed to generate HTML newsletter: {e}")
                html_path = None

            # Generate markdown report
            markdown_content = f"""# AI in Cancer Care Newsletter
## {datetime.now().strftime('%B %Y')}

## 📊 Quick Stats
- **Articles Analyzed**: {metrics['total_articles']}
- **Topics Covered**: {metrics['total_topics']}
- **Average Quality**: {metrics['average_quality']:.1%}

## Executive Summary
{exec_summary}

## Topics Covered

"""
            for idx, summary in enumerate(topic_summaries, 1):
                quality_score = summary.get('quality_score', 0.75)
                markdown_content += f"""### {idx}. {summary.get('topic_name', 'Unknown')} (Quality: {quality_score:.0%})

{summary.get('overview', 'No overview available')}

**Key Findings:**
"""
                for finding in summary.get('key_findings', [])[:5]:
                    markdown_content += f"- {finding}\n"
                
                trends = summary.get('notable_trends', [])
                if trends:
                    markdown_content += "\n**Notable Trends:**\n"
                    for trend in trends[:3]:
                        markdown_content += f"- {trend}\n"
                
                markdown_content += "\n---\n\n"

            # Save markdown
            md_path = f"{outputs_dir}/newsletter_{timestamp}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            # Update state outputs
            state["outputs"] = {
                "markdown": md_path,
                "html": html_path if html_path else None,
                "timestamp": timestamp,
                "charts": chart_paths,
                "cover_image": cover_image_path,  # DALL-E image
                "flux_image": flux_image_path,  # Flux image (if generated)
                "flux_prompts": flux_prompts_data,  # Flux prompts for manual use
                "knowledge_graph": knowledge_graph_data,
                "glossary": glossary_data
            }

            # Store knowledge graph and glossary in state for potential use
            if knowledge_graph_data:
                state["knowledge_graph"] = knowledge_graph_data
            if glossary_data:
                state["glossary"] = glossary_data

            # Record result
            agent_result = {
                "task_name": "generate_newsletter",
                "agent_name": "chief_editor_node",
                "status": "success",
                "output": f"Generated newsletter with {len(topic_summaries)} topics, HTML, and {len(chart_paths)} charts",
                "execution_time": time.time() - start_time
            }
            if "agent_results" not in state:
                state["agent_results"] = []
            state["agent_results"].append(agent_result)

            state["current_stage"] = "completed"
            state["workflow_end_time"] = datetime.now().isoformat()

            logger.info(f"Enhanced newsletter generation complete!")
            logger.info(f"  - Markdown: {md_path}")
            if html_path:
                logger.info(f"  - HTML: {html_path}")
            if cover_image_path:
                logger.info(f"  - Cover Image (DALL-E): {cover_image_path}")
            if flux_image_path:
                logger.info(f"  - Cover Image (Flux): {flux_image_path}")
            if flux_prompts_data:
                logger.info(f"  - Flux Prompts: {flux_prompts_data['prompt_file']}")
                if not flux_image_path:
                    logger.info(f"    → Use prompts on CivitAI for manual generation")
            logger.info(f"  - Charts: {len(chart_paths)} visualizations")
            if knowledge_graph_data:
                logger.info(f"  - Knowledge Graph: {knowledge_graph_data['stats']['total_entities']} entities, {knowledge_graph_data['stats']['total_relationships']} relationships")
                logger.info(f"    - JSON: {knowledge_graph_data['json_path']}")
            if glossary_data:
                logger.info(f"  - Glossary: {glossary_data['total_terms']} terms")

            return state

        except Exception as e:
            logger.error(f"Failed to generate newsletter: {e}")
            if "errors" not in state:
                state["errors"] = []
            state["errors"].append(f"Failed to generate newsletter: {str(e)}")
            state["current_stage"] = "failed"
            return state
    
    async def _generate_newsletter_full(self, state: dict) -> dict:
        """
        Full newsletter generation implementation (temporarily disabled).
        
        LangGraph passes state as dict, not Pydantic model.

        Args:
            state: Current workflow state (dict)

        Returns:
            Updated workflow state (dict)
        """
        task_config = load_task_config('draft_html_newsletter')
        start_time = time.time()
        
        try:
            # Convert dict to Pydantic model for easier manipulation
            state_obj = WorkflowState(**state)
            logger.info("Generating newsletter")

            # Get filtered summaries based on selection
            selected_summaries = state_obj.get_selected_summaries()

            if not selected_summaries:
                logger.warning("No topics selected for newsletter generation")
                state_obj.add_warning("No topics available for newsletter generation")
                return state_obj.model_dump()

            logger.info(f"Generating newsletter with {len(selected_summaries)} selected topics out of {len(state_obj.topic_summaries)} total")

            # Create executive summary using direct prompt
            exec_prompt = self.prompts.get_prompt("editor_agent", "create_executive_summary")
            exec_chain = exec_prompt | self.llm | StrOutputParser()

            topics_summaries = "\n\n".join([
                f"**{s.topic_name}**\n{s.overview[:200]}..."
                for s in selected_summaries
            ])

            exec_summary = await exec_chain.ainvoke({
                "topics_summaries": topics_summaries
            })

            state_obj.executive_summary = exec_summary

            # Generate overall visualizations (based on selected topics only)
            header_image = self.visualizer.create_header_image(
                title="AI in Cancer Care Newsletter",
                subtitle=datetime.now().strftime("%B %Y")
            )

            distribution_chart = self.visualizer.create_topic_distribution_chart(
                topics_data=[{
                    'name': s.topic_name,
                    'articles': s.top_articles
                } for s in selected_summaries]
            )

            quality_chart = self.visualizer.create_quality_metrics_chart(
                topics_data=[{
                    'name': s.topic_name,
                    'quality_score': s.quality_score
                } for s in selected_summaries]
            )

            # Calculate metrics for infographic (based on selected topics)
            metrics = state_obj.calculate_metrics()
            selected_articles = sum(len(s.top_articles) for s in selected_summaries)
            avg_quality = sum(s.quality_score for s in selected_summaries) / max(len(selected_summaries), 1)

            infographic = self.visualizer.create_infographic_summary(
                total_articles=selected_articles,
                total_topics=len(selected_summaries),
                avg_quality=avg_quality,
                duration_seconds=metrics.get('duration_seconds', 0)
            )

            # Prepare content for newsletter (only selected topics)
            content = {
                "executive_summary": exec_summary,
                "topics": [],
                "header_image": header_image,
                "distribution_chart": distribution_chart,
                "quality_chart": quality_chart,
                "infographic": infographic,
                "all_topics_count": len(state_obj.topic_summaries),
                "selected_topics_count": len(selected_summaries)
            }

            for summary in selected_summaries:
                topic_data = {
                    "name": summary.topic_name,
                    "summary": summary.overview,
                    "highlights": summary.key_findings,
                    "articles": [a.model_dump() for a in summary.top_articles],
                    "quality_score": summary.quality_score,
                    "chart_image": summary.chart_image_path
                }
                content["topics"].append(topic_data)

            # Generate HTML using template (simplified for now)
            html_content = self._generate_html_template(content)

            # Generate markdown report
            markdown_content = self._generate_markdown_report(content)

            # Create newsletter object
            newsletter = NewsletterContentModel(
                subject_line=f"AI in Cancer Care: {datetime.now().strftime('%B %Y')} Digest",
                preheader="Latest breakthroughs in AI-powered oncology",
                executive_summary=exec_summary,
                topics=content["topics"],
                call_to_action="Stay informed about AI advances",
                footer_text="© 2024 AI Cancer Research"
            )

            state_obj.newsletter_content = newsletter

            # Save outputs
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            outputs_dir = "outputs"

            html_path = f"{outputs_dir}/newsletter_{timestamp}.html"
            self.file_manager.save_html(html_content, html_path)

            md_path = f"{outputs_dir}/report_{timestamp}.md"
            self.file_manager.save_markdown(markdown_content, md_path)

            state_obj.outputs = {
                "html": html_path,
                "markdown": md_path
            }

            # Record result
            agent_result = AgentTaskResultModel(
                task_name="generate_newsletter",
                agent_name="chief_editor_node",
                status="success",
                output="Generated newsletter and report",
                execution_time=time.time() - start_time
            )
            state_obj.add_agent_result(agent_result)

            state_obj.current_stage = "completed"
            state_obj.workflow_end_time = datetime.now()

            logger.info("Newsletter generation complete")

            return state_obj.model_dump()

        except Exception as e:
            logger.error(f"Newsletter generation failed: {str(e)}")
            # Handle error even if state_obj wasn't created yet
            try:
                if 'state_obj' in locals():
                    error_msg = f"Newsletter generation failed: {str(e)}"
                    state_obj.add_error(error_msg)
                    agent_result = AgentTaskResultModel(
                        task_name="generate_newsletter",
                        agent_name="chief_editor_node",
                        status="failed",
                        error=str(e),
                        execution_time=time.time() - start_time
                    )
                    state_obj.add_agent_result(agent_result)
                    state_obj.current_stage = "failed"
                    return state_obj.model_dump()
                else:
                    # State conversion failed, work with dict directly
                    if "errors" not in state:
                        state["errors"] = []
                    state["errors"].append(f"Newsletter generation failed: {str(e)}")
                    state["current_stage"] = "failed"
                    return state
            except Exception as inner_e:
                logger.error(f"Error handling error: {inner_e}")
                return state

    def _load_topics_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load topics configuration from file."""
        import yaml
        import json
        import os

        # Default to JSON config if not specified
        default_path = os.path.join(
            os.path.dirname(__file__),
            "config/topics_cancer.json"
        )

        try:
            path_to_load = config_path or default_path
            logger.info(f"Loading topics configuration from: {path_to_load}")

            with open(path_to_load, "r") as f:
                if path_to_load.endswith('.json'):
                    data = json.load(f)
                else:
                    # For YAML files, extract topics section
                    yaml_data = yaml.safe_load(f)
                    # If it's tasks.yaml with nested structure
                    if 'topics' in yaml_data and 'main_topic' in yaml_data['topics']:
                        data = yaml_data['topics']
                    else:
                        data = yaml_data

            # Normalize the structure
            # Handle both 'sub_topics' and 'topics' keys
            if 'sub_topics' in data:
                topics_list = data['sub_topics']
            elif 'topics' in data:
                # Check if topics is a list or has sub_topics inside
                if isinstance(data['topics'], list):
                    topics_list = data['topics']
                elif isinstance(data['topics'], dict) and 'sub_topics' in data['topics']:
                    topics_list = data['topics']['sub_topics']
                else:
                    topics_list = []
            else:
                logger.error("No topics found in configuration")
                topics_list = []

            # Create normalized configuration
            topics_config = {
                "main_topic": data.get('main_topic', "AI in Cancer Care"),
                "topics": topics_list
            }

            logger.info(f"✓ Loaded {len(topics_list)} topics from configuration:")
            for idx, topic in enumerate(topics_list, 1):
                logger.info(f"  {idx}. {topic.get('name', 'Unknown')}")

            return topics_config

        except Exception as e:
            logger.error(f"Failed to load config from {config_path or default_path}: {e}")
            logger.warning("Using fallback configuration with 1 topic")
            return {
                "main_topic": "AI in Cancer Care",
                "topics": [
                    {
                        "name": "Cancer Research",
                        "description": "AI in oncology research",
                        "query": "AI oncology research"
                    }
                ]
            }

    def _extract_trends(self, summary_text: str) -> List[str]:
        """Extract trends from summary text."""
        trends = []

        # Simple extraction based on keywords
        trend_keywords = [
            "emerging", "trend", "growing", "increasing", "shift",
            "adoption", "development", "advancement", "progress"
        ]

        lines = summary_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in trend_keywords):
                trends.append(line.strip())

        # Return top 3 trends
        return trends[:3] if trends else ["AI adoption increasing", "Focus on precision medicine"]

    def _generate_html_template(self, content: Dict[str, Any]) -> str:
        """Generate HTML newsletter template with images."""
        # Helper function to convert file paths to embeddable format
        def get_image_tag(image_path, alt_text, max_width="100%"):
            if image_path and os.path.exists(image_path):
                return f'<img src="file://{image_path}" alt="{alt_text}" style="max-width: {max_width}; height: auto; display: block; margin: 20px auto;">'
            return ''

        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI in Cancer Care Newsletter</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header-image {{ width: 100%; margin-bottom: 30px; border-radius: 5px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        .executive-summary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 8px; margin: 20px 0; }}
        .executive-summary h2 {{ color: white; border: none; }}
        .metrics-section {{ margin: 30px 0; text-align: center; }}
        .charts-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 30px 0; }}
        .chart-container {{ text-align: center; background: #f9f9f9; padding: 15px; border-radius: 8px; }}
        .topic {{ margin: 30px 0; padding: 20px; border-left: 4px solid #3498db; background: #fafafa; border-radius: 5px; }}
        .topic-chart {{ margin: 20px 0; text-align: center; }}
        .article {{ margin: 10px 0; padding: 10px; background: white; border-radius: 5px; }}
        .quality-badge {{ display: inline-block; padding: 5px 12px; border-radius: 15px; font-size: 11px; font-weight: bold; }}
        .high-quality {{ background: #27ae60; color: white; }}
        .medium-quality {{ background: #f39c12; color: white; }}
        .low-quality {{ background: #e74c3c; color: white; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <div class="container">
"""

        # Add header image
        if content.get('header_image'):
            html += get_image_tag(content['header_image'], 'Newsletter Header', '100%')

        html += f"""
    <h1>AI in Cancer Care Newsletter</h1>

    <div class="executive-summary">
        <h2>Executive Summary</h2>
        <p>{content['executive_summary']}</p>
    </div>
"""

        # Add metrics infographic
        if content.get('infographic'):
            html += f"""
    <div class="metrics-section">
        <h2>At a Glance</h2>
        {get_image_tag(content['infographic'], 'Newsletter Metrics', '600px')}
    </div>
"""

        # Add overview charts
        if content.get('distribution_chart') or content.get('quality_chart'):
            html += """
    <div class="charts-grid">
"""
            if content.get('distribution_chart'):
                html += f"""
        <div class="chart-container">
            <h3>Topic Distribution</h3>
            {get_image_tag(content['distribution_chart'], 'Topic Distribution', '100%')}
        </div>
"""
            if content.get('quality_chart'):
                html += f"""
        <div class="chart-container">
            <h3>Quality Metrics</h3>
            {get_image_tag(content['quality_chart'], 'Quality Metrics', '100%')}
        </div>
"""
            html += """
    </div>
"""

        # Add topics with their charts
        for topic in content['topics']:
            quality_class = "high-quality" if topic.get('quality_score', 0) >= 0.8 else "medium-quality" if topic.get('quality_score', 0) >= 0.6 else "low-quality"
            html += f"""
    <div class="topic">
        <h2>{topic['name']} <span class="quality-badge {quality_class}">Quality: {topic.get('quality_score', 0):.1%}</span></h2>
        <p>{topic['summary'][:500]}...</p>
"""

            # Add topic chart if available
            if topic.get('chart_image'):
                html += f"""
        <div class="topic-chart">
            {get_image_tag(topic['chart_image'], f"{topic['name']} Trends", '600px')}
        </div>
"""

            html += """
        <h3>Key Highlights</h3>
        <ul>
"""
            for highlight in topic.get('highlights', [])[:3]:
                html += f"            <li>{highlight}</li>\n"

            html += """        </ul>
    </div>
"""

        html += """
    <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ccc; text-align: center; color: #7f8c8d;">
        <p>© 2024 AI Cancer Research Newsletter</p>
        <p style="font-size: 12px;">Generated with AI-powered analysis and visualization</p>
    </div>
    </div>
</body>
</html>"""

        return html

    def _generate_markdown_report(self, content: Dict[str, Any]) -> str:
        """Generate Markdown report."""
        md = f"""# AI in Cancer Care Research Report

## Executive Summary

{content['executive_summary']}

---

## Topics Covered

"""

        for topic in content['topics']:
            md += f"""
### {topic['name']}

**Quality Score:** {topic.get('quality_score', 0):.1%}

{topic['summary']}

**Key Highlights:**
"""
            for highlight in topic.get('highlights', []):
                md += f"- {highlight}\n"

            md += "\n**Top Articles:**\n"
            for i, article in enumerate(topic.get('articles', [])[:3], 1):
                md += f"{i}. [{article['title']}]({article.get('url', '#')})\n"

            md += "\n---\n"

        md += """
## About This Report

This report was generated using AI-powered analysis of recent publications in cancer research and AI applications.

*Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "*"

        return md