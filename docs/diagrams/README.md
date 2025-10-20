# AI News LangGraph Workflow Diagrams

## 1. Main Workflow (Graphviz)

To render the Graphviz diagram:
```bash
dot -Tpng workflow.dot -o workflow.png
dot -Tsvg workflow.dot -o workflow.svg
```

## 2. Workflow Flow (Mermaid)

```mermaid

graph TD
    %% Main Workflow
    Start([Start]) --> Init[Initialize Workflow]
    Init --> LoadConfig[Load Configuration]
    LoadConfig --> CreateState[Create State]

    CreateState --> FetchLoop{Fetch Loop}

    FetchLoop --> FetchNews[Fetch News for Topic]
    FetchNews --> ScoreArticles[Score Article Relevance]
    ScoreArticles --> Summarize[Summarize Topic]

    Summarize --> CheckTopics{More Topics?}
    CheckTopics -->|Yes| FetchLoop
    CheckTopics -->|No| ReviewAll[Review All Summaries]

    ReviewAll --> QualityCheck[Calculate Quality Scores]
    QualityCheck --> GenerateFeedback[Generate Feedback]

    GenerateFeedback --> CreateNewsletter[Generate Newsletter]
    CreateNewsletter --> SaveHTML[Save HTML]
    CreateNewsletter --> SaveMD[Save Markdown]
    CreateNewsletter --> SaveJSON[Save JSON]

    SaveHTML --> End([End])
    SaveMD --> End
    SaveJSON --> End

    %% Styling
    classDef startEnd fill:#90EE90,stroke:#333,stroke-width:2px
    classDef process fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef decision fill:#FFE4B5,stroke:#333,stroke-width:2px
    classDef output fill:#98FB98,stroke:#333,stroke-width:2px

    class Start,End startEnd
    class Init,LoadConfig,CreateState,FetchNews,ScoreArticles,Summarize,ReviewAll,QualityCheck,GenerateFeedback,CreateNewsletter process
    class FetchLoop,CheckTopics decision
    class SaveHTML,SaveMD,SaveJSON output
    
```

## 3. State Evolution

```mermaid

stateDiagram-v2
    [*] --> Initialized: Start Workflow

    Initialized --> Fetching: Begin Topic Processing

    Fetching --> Summarizing: Articles Fetched

    Summarizing --> Fetching: More Topics
    Summarizing --> Reviewing: All Topics Done

    Reviewing --> Generating: Quality Assessed

    Generating --> Completed: Newsletter Created

    Completed --> [*]: End

    Fetching --> Failed: Error
    Summarizing --> Failed: Error
    Reviewing --> Failed: Error
    Generating --> Failed: Error

    Failed --> [*]: Workflow Failed

    note right of Fetching
        Fetches news articles
        for current topic
    end note

    note right of Summarizing
        Creates summary for
        fetched articles
    end note

    note right of Reviewing
        Self-review pattern
        Quality assessment
    end note

    note right of Generating
        Creates HTML/MD
        newsletter output
    end note
    
```

## Rendering Instructions

### For Graphviz:
1. Install Graphviz: `brew install graphviz` (macOS) or `apt-get install graphviz` (Linux)
2. Generate image: `dot -Tpng workflow.dot -o workflow.png`

### For Mermaid:
1. Use Mermaid Live Editor: https://mermaid.live/
2. Or install Mermaid CLI: `npm install -g @mermaid-js/mermaid-cli`
3. Generate image: `mmdc -i workflow.mmd -o workflow.png`

### In Jupyter Notebook:
Use the provided `workflow_visualization.ipynb` for interactive visualization.
