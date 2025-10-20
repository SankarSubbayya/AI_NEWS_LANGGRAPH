# Running the App

## Prerequisites

- Python 3.9+
- OpenAI API Key
- Optional: LangSmith API Key for observability

## Installation

```bash
cd AI_NEWS_LANGGRAPH
pip install -r requirements.txt
# or
uv sync
```

## Starting the App

```bash
uv run streamlit run final_newsletter_app.py --server.port 8501
```

Or with Python directly:

```bash
python -m streamlit run final_newsletter_app.py --server.port 8501
```

## Accessing the App

Open your browser to:
```
http://localhost:8501
```

## Stopping the App

Press `Ctrl+C` in the terminal where Streamlit is running.

Or kill the process:
```bash
pkill -f streamlit
```

## Using a Custom Port

```bash
uv run streamlit run final_newsletter_app.py --server.port 9000
```

Then access at: `http://localhost:9000`

## Troubleshooting

**"Port 8501 already in use"**
```bash
pkill -f streamlit
sleep 2
uv run streamlit run final_newsletter_app.py
```

**"OPENAI_API_KEY not found"**
```bash
export OPENAI_API_KEY="sk-proj-..."
```

See [Troubleshooting](../troubleshooting/common-issues.md) for more help.
