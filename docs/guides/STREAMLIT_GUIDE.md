# 🌐 Streamlit Web Application Guide

## Overview

The AI News Research System now includes a beautiful web interface built with Streamlit. This provides an intuitive way to configure topics, run the multi-agent workflow, and view results without using the command line.

## Features

### 🏠 Home Dashboard
- System overview and metrics
- Quick access to documentation
- Real-time status of generated outputs

### 📝 Topic Configuration
- Visual editor for research topics
- Add, edit, and remove topics easily
- JSON preview and validation
- Save/load topic configurations

### 🚀 Workflow Execution
- Pre-flight checks for API keys and configuration
- One-click workflow execution
- Real-time progress tracking
- Agent performance metrics
- Error reporting and debugging

### 📊 Results Viewer
- Browse all generated newsletters and reports
- Interactive HTML newsletter preview
- Markdown report rendering
- Download files (HTML, Markdown, JSON)

## Getting Started

### 1. Install Dependencies

Make sure Streamlit is installed:

```bash
uv pip install streamlit
```

Or reinstall the package with updated dependencies:

```bash
uv pip install -e .
```

### 2. Configure Environment

Ensure your `.env` file has the required API keys:

```bash
# Required
OPENAI_API_KEY=sk-your-actual-key-here

# Optional (at least one recommended)
TAVILY_API_KEY=tvly-your-key-here
SERPER_API_KEY=your-serper-key-here

# Optional configuration
PREFERRED_SEARCH_API=serper  # or tavily
OPENAI_MODEL=gpt-4-turbo-preview
```

### 3. Run the Application

From the project root directory:

```bash
streamlit run app.py
```

Or using the `uv` tool:

```bash
uv run streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### Configuring Topics

1. **Navigate to "Configure Topics" tab**
2. **Set Main Topic**: Enter the overarching research theme (e.g., "AI in Cancer Care")
3. **Add Sub-Topics**:
   - Click "➕ Add New Topic"
   - Enter topic name, description, and keywords
   - Click "Add Topic"
4. **Edit Existing Topics**:
   - Expand any topic card
   - Modify name, description, or keywords
   - Click 🗑️ to remove unwanted topics
5. **Save Configuration**: Click "💾 Save Topics"

**Example Topic Configuration:**

```json
{
  "main_topic": "AI in Cancer Care",
  "topics": [
    {
      "name": "Cancer Research",
      "description": "Latest AI applications in cancer research",
      "keywords": ["AI", "oncology", "research", "genomics"]
    },
    {
      "name": "Cancer Prevention",
      "description": "AI in cancer risk prediction and prevention",
      "keywords": ["AI", "prevention", "risk prediction"]
    }
  ]
}
```

### Running the Workflow

1. **Navigate to "Run Workflow" tab**
2. **Check Pre-flight Status**:
   - ✅ OpenAI API Key configured
   - ✅ Topics file loaded
3. **Click "▶️ Run Workflow"**
4. **Monitor Progress**:
   - Watch the progress indicator
   - View execution time
   - Check agent performance metrics
5. **Review Results**:
   - See topics processed
   - View summaries created
   - Check for any errors

### Viewing Results

1. **Navigate to "Results" tab**
2. **Select a Result**: Choose from the dropdown of generated newsletters
3. **View Content**:
   - **Newsletter Tab**: Interactive HTML preview
   - **Report Tab**: Rendered Markdown report
   - **Download Tab**: Get files for offline use
4. **Download Files**:
   - Click download buttons for HTML, Markdown, or JSON formats

## Sidebar Configuration

### 🔑 API Key Status
- Shows which API keys are configured
- Click "🔄 Reload .env" to refresh after updating keys

### 🔍 Search API Selection
- Choose between Serper (Google Search) or Tavily (AI-optimized)
- Serper provides more results, Tavily provides AI-focused content

### 📋 Topics Configuration
- Set the path to your topics JSON file
- Default: `src/ai_news_langgraph/config/topics_cancer.json`

## Tips & Best Practices

### Performance Optimization
- **Start Small**: Test with 2-3 topics before running larger batches
- **Monitor Resources**: The workflow can be resource-intensive
- **Use Caching**: Streamlit caches results for faster reloads

### Topic Configuration
- **Be Specific**: Add detailed keywords for better search results
- **Balanced Descriptions**: Provide enough context without being too verbose
- **Test Iteratively**: Run with one topic first, then expand

### Troubleshooting
- **API Key Issues**: Check the sidebar for API key status
- **Workflow Errors**: Review the error details in the expandable section
- **Slow Loading**: Large HTML newsletters may take time to render

## Advanced Features

### Custom Topics File
You can create multiple topic configurations:

```bash
# Create a new topics file
cp src/ai_news_langgraph/config/topics_cancer.json my_custom_topics.json

# Edit the file with your topics
# Then in the sidebar, set the path to your custom file
```

### Environment Variables
The app respects all environment variables from `.env`:

- `OPENAI_API_KEY`: Required for LLM operations
- `TAVILY_API_KEY`: Optional, for Tavily search
- `SERPER_API_KEY`: Optional, for Google search
- `PREFERRED_SEARCH_API`: Choose default search API
- `OPENAI_MODEL`: Specify GPT model (default: gpt-4-turbo-preview)

### Multiple Sessions
You can run multiple Streamlit sessions on different ports:

```bash
# Session 1 (default port 8501)
streamlit run app.py

# Session 2 (custom port)
streamlit run app.py --server.port 8502
```

## Keyboard Shortcuts

- `R` or `Ctrl+R`: Rerun the app
- `C`: Clear cache
- `Ctrl+C` (in terminal): Stop the server

## File Structure

After running the workflow, files are organized as:

```
outputs/
├── newsletter_YYYYMMDD_HHMMSS.html  # HTML newsletter
├── report_YYYYMMDD_HHMMSS.md        # Markdown report
├── data_YYYYMMDD_HHMMSS.json        # Structured data
└── run_results_YYYYMMDD_HHMMSS.json # Execution metadata
```

## Comparison: CLI vs Streamlit

| Feature | Command Line | Streamlit Web UI |
|---------|--------------|------------------|
| Setup Complexity | Medium | Easy |
| Topic Configuration | Manual file editing | Visual editor |
| Progress Tracking | Terminal logs | Real-time UI |
| Results Viewing | External tools | Built-in preview |
| User Friendliness | Technical users | All users |
| Automation | Scriptable | Interactive |

## Common Issues

### Port Already in Use
```bash
# Find and kill the process
lsof -ti:8501 | xargs kill -9

# Or use a different port
streamlit run app.py --server.port 8502
```

### Module Import Errors
```bash
# Reinstall the package
uv pip install -e .

# Or add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Browser Not Opening
```bash
# Run with explicit browser
streamlit run app.py --browser.serverAddress localhost
```

## Next Steps

1. **Explore**: Try different topic configurations
2. **Customize**: Modify the Streamlit app to fit your needs
3. **Automate**: Schedule workflows using the CLI for production
4. **Share**: Deploy the app to Streamlit Cloud for team access

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Project Architecture](ARCHITECTURE.md)
- [Task Management Guide](TASKS_GUIDE.md)

## Deployment

To deploy the Streamlit app to the cloud:

```bash
# Option 1: Streamlit Community Cloud (free)
# 1. Push your code to GitHub
# 2. Go to https://share.streamlit.io/
# 3. Connect your repository
# 4. Deploy!

# Option 2: Docker
# Create a Dockerfile and deploy to any cloud provider
```

---

**Need Help?** Check the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide or open an issue on GitHub.

