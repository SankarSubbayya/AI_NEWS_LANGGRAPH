# LangGraph Workflow Visualization

## Workflow Graph

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	fetch_news_for_topic(fetch_news_for_topic)
	summarize_topic_news(summarize_topic_news)
	create_executive_summary(create_executive_summary)
	generate_newsletter(generate_newsletter)
	__end__([<p>__end__</p>]):::last
	__start__ --> fetch_news_for_topic;
	create_executive_summary --> generate_newsletter;
	fetch_news_for_topic --> summarize_topic_news;
	summarize_topic_news -.-> create_executive_summary;
	summarize_topic_news -.-> fetch_news_for_topic;
	generate_newsletter --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc

```

## Graph Description

The workflow consists of the following nodes:

1. **fetch_news**: Fetches news articles for each topic
2. **summarize_news**: Summarizes articles for each topic
3. **create_summary**: Creates an executive summary across all topics
4. **generate_newsletter**: Generates HTML newsletter and markdown report

### Flow:

1. Start → fetch_news
2. fetch_news → summarize_news
3. summarize_news → (conditional)
   - If more topics remain: → fetch_news (loop)
   - If all topics done: → create_summary
4. create_summary → generate_newsletter
5. generate_newsletter → END

### Key Features:

- **Iterative Processing**: The workflow loops through topics one by one
- **State Management**: Full state is maintained throughout the workflow
- **Error Handling**: Each node handles errors gracefully
- **Conditional Routing**: Decision point after summarization
