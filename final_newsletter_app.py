"""Final Newsletter App - Topics & Glossary on Sidebar, Executive Summary & Full Newsletter in Tabs."""

import streamlit as st
import os
import sys
import json
import re
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from dotenv import load_dotenv
load_dotenv()

# Initialize LangSmith observability
try:
    from src.ai_news_langgraph.langsmith_observability import initialize_langsmith

    if 'langsmith_initialized' not in st.session_state:
        langsmith_observer = initialize_langsmith(project_name="AI-News-LangGraph")
        st.session_state.langsmith_initialized = True
        st.session_state.langsmith_observer = langsmith_observer
except Exception as e:
    st.session_state.langsmith_initialized = False

# Page config
st.set_page_config(
    page_title="AI Cancer Newsletter",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load latest newsletter
@st.cache_data
def load_latest_newsletter():
    """Load the latest newsletter HTML."""
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        html_files = sorted(
            outputs_dir.glob("newsletter_*.html"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        if html_files:
            with open(html_files[0], 'r', encoding='utf-8') as f:
                return html_files[0], f.read()
    return None, None

# Extract topics from HTML
@st.cache_data
def extract_topics(html_content):
    """Extract topic cards from HTML."""
    topics = []
    pattern = r'<div class="topic-card">(.*?)</div>\s*</div>'
    matches = re.findall(pattern, html_content, re.DOTALL)

    for i, match in enumerate(matches[:5], 1):
        # Extract topic name
        name_match = re.search(r'<span class="topic-icon">.*?</span>\s*([^<]+?)\s*<span class="quality-badge', match)
        topic_name = name_match.group(1).strip() if name_match else f"Topic {i}"

        # Extract quality score
        quality_match = re.search(r'Quality: (\d+)%', match)
        quality = quality_match.group(1) if quality_match else "N/A"

        topics.append({
            'name': topic_name,
            'quality': quality,
            'html': match,
            'index': i
        })

    return topics

# Extract executive summary
@st.cache_data
def extract_executive_summary(html_content):
    """Extract executive summary from HTML."""
    # Find executive summary section
    pattern = r'<div class="executive-summary">(.*?)</div>'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        summary_html = match.group(1)
        # Remove HTML tags but keep some structure
        summary_html = re.sub(r'<[^>]+>', '', summary_html)
        return summary_html.strip()
    return "No executive summary found"

# Extract glossary
@st.cache_data
def extract_glossary(html_content):
    """Extract glossary from HTML."""
    # Find glossary section - need to handle nested divs properly
    glossary_start = html_content.find('<div class="glossary-section">')
    if glossary_start == -1:
        return None

    # Find the closing div for glossary-section
    # Count div opens and closes to find matching close
    div_count = 1
    pos = glossary_start + len('<div class="glossary-section">')

    while div_count > 0 and pos < len(html_content):
        if html_content[pos:pos+4] == '<div':
            div_count += 1
            pos += 4
        elif html_content[pos:pos+6] == '</div>':
            div_count -= 1
            if div_count == 0:
                return html_content[glossary_start:pos+6]
            pos += 6
        else:
            pos += 1

    return None

# Main app
st.markdown('<div class="main-header">🔬 AI Cancer Newsletter</div>', unsafe_allow_html=True)

# Load newsletter
newsletter_file, newsletter_html = load_latest_newsletter()

if not newsletter_html:
    st.info("👋 Welcome! No newsletters found yet.")
    st.markdown("""
    ### Get Started
    
    This app displays AI-generated cancer research newsletters. Since this is a fresh deployment,
    no newsletters have been generated yet.
    
    **To generate your first newsletter:**
    1. Make sure you have set up your API keys in Streamlit secrets
    2. Run the newsletter generation workflow locally first
    3. Or use the full AI workflow feature if available
    
    **Required API Keys:**
    - `OPENAI_API_KEY` - For AI generation
    - `TAVILY_API_KEY` - For research
    - `REPLICATE_API_TOKEN` (optional) - For cover images
    
    **Note:** Newsletter generation is computationally intensive and may not work well
    on Streamlit's free tier due to resource limits. This app is designed to display
    newsletters that have been generated and committed to the repository.
    """)
    
    # Show sample information
    with st.expander("📚 About This Newsletter"):
        st.write("""
        The AI Cancer Newsletter uses a multi-agent LangGraph workflow to:
        - 🔍 Research latest AI developments in cancer care
        - ✍️ Curate and summarize findings
        - 📊 Generate interactive visualizations
        - 📰 Create beautiful HTML newsletters
        - 🧠 Build cancer research knowledge graphs
        - 📖 Generate AI-powered glossaries
        """)
    
    with st.expander("🚀 Deployment Tips"):
        st.write("""
        **For Local Development:**
        ```bash
        # Run the Streamlit app locally
        streamlit run final_newsletter_app.py
        
        # Generate a newsletter first
        python -m ai_news_langgraph.main
        ```
        
        **For Production Deployment:**
        - Pre-generate newsletters and commit them to the repository
        - The app will automatically display the latest newsletter
        - Users can view but not generate new newsletters (resource intensive)
        """)
    
    st.stop()

st.success(f"✅ Displaying: {newsletter_file.name}")

# Extract data
topics = extract_topics(newsletter_html)
executive_summary = extract_executive_summary(newsletter_html)
glossary_html = extract_glossary(newsletter_html)

# SIDEBAR - NAVIGATION
with st.sidebar:
    st.markdown("### 📊 Observability")

    if st.session_state.get('langsmith_initialized'):
        observer = st.session_state.get('langsmith_observer')
        if observer and observer.is_enabled():
            st.success("✅ LangSmith Active")
            dashboard_url = observer.get_dashboard_url()
            st.markdown(f"[🔗 Dashboard](https://smith.langchain.com/)")
            st.caption("Monitor all AI operations")
        else:
            st.info("⚠️ Set LANGSMITH_API_KEY to enable")
    else:
        st.info("ℹ️ LangSmith not active")
        st.caption("Get key: https://smith.langchain.com/")

    st.divider()

    st.markdown("### 📋 TOPICS")

    for topic in topics:
        if st.button(
            f"📌 {topic['name']}\n({topic['quality']}%)",
            use_container_width=True,
            key=f"topic_{topic['index']}"
        ):
            st.session_state.selected_topic = topic['index'] - 1

    st.divider()

    if st.button("🚀 Generate New", use_container_width=True):
        st.session_state.generate = True

# MAIN CONTENT - TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Selected Topic",
    "📝 Executive Summary",
    "📖 Glossary",
    "📰 Full Newsletter",
    "📚 All Newsletters"
])

# TAB 1: Selected Topic
with tab1:
    if 'selected_topic' in st.session_state:
        idx = st.session_state.selected_topic
        if idx < len(topics):
            topic = topics[idx]

            st.markdown(f"## {topic['name']}")
            st.metric("Quality Score", f"{topic['quality']}%")
            st.divider()

            # Display topic HTML
            topic_html = f"""
            <style>
                .topic-card {{
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 20px;
                    border-radius: 8px;
                }}
                .quality-badge {{ margin-left: 10px; }}
                .key-findings, .trends, .articles-section {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                }}
            </style>
            <div class="topic-card">{topic['html']}</div>
            """
            st.components.v1.html(topic_html, height=900, scrolling=True)
    else:
        st.info("👈 Click a topic in the sidebar to view details")

# TAB 2: Executive Summary
with tab2:
    st.markdown("## 📝 Executive Summary")

    if executive_summary:
        st.markdown(executive_summary)
    else:
        st.info("No executive summary available")

# TAB 3: Glossary
with tab3:
    st.markdown("## 📖 Medical Glossary")

    if glossary_html:
        glossary_display = f"""
        <style>
            .glossary-section {{
                background: linear-gradient(135deg, #f5f7fa 0%, #e8ebf5 100%);
                padding: 20px;
                border-radius: 8px;
            }}
            .glossary-item {{
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }}
            .glossary-term {{
                font-weight: bold;
                color: #333;
                font-size: 1.1em;
                margin-bottom: 5px;
            }}
            .glossary-definition {{
                color: #555;
                line-height: 1.6;
                margin: 10px 0;
            }}
        </style>
        <div class="glossary-section">{glossary_html}</div>
        """
        st.components.v1.html(glossary_display, height=900, scrolling=True)
    else:
        st.info("No glossary available")

# TAB 4: Full Newsletter HTML
with tab4:
    st.markdown("### 📰 Full Newsletter")

    st.components.v1.html(newsletter_html, height=1200, scrolling=True)

    st.divider()

    st.download_button(
        "⬇️ Download Newsletter (HTML)",
        newsletter_html,
        file_name=newsletter_file.name,
        mime="text/html",
        use_container_width=True
    )

# TAB 5: All Newsletters
with tab5:
    st.markdown("### 📚 All Generated Newsletters")

    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        html_files = sorted(
            outputs_dir.glob("newsletter_*.html"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        if html_files:
            st.markdown(f"**Total: {len(html_files)} newsletters**")

            # Show list
            for i, file in enumerate(html_files[:10], 1):
                if st.button(f"{i}. {file.name}", use_container_width=True, key=f"nl_{i}"):
                    st.session_state.view_newsletter = str(file)

            # Show selected newsletter
            if 'view_newsletter' in st.session_state:
                st.divider()
                st.markdown(f"### {Path(st.session_state.view_newsletter).name}")

                with open(st.session_state.view_newsletter, 'r', encoding='utf-8') as f:
                    html_data = f.read()

                st.components.v1.html(html_data, height=1000, scrolling=True)
        else:
            st.info("No newsletters yet")
    else:
        st.info("No outputs directory")

