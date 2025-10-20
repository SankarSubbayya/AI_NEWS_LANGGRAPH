#!/usr/bin/env python3
"""
Generate visual representations of the LangGraph workflow.
Creates both a graph diagram and a flow chart.
"""

import os
from pathlib import Path


def create_graphviz_workflow():
    """Create a Graphviz DOT representation of the workflow."""

    dot_content = """
digraph AINewsWorkflow {
    rankdir=TB;
    node [shape=box, style="rounded,filled", fontname="Arial"];
    edge [fontname="Arial"];

    // Define node styles
    start [label="START", shape=circle, fillcolor="#90EE90"];
    end [label="END", shape=doublecircle, fillcolor="#FFB6C1"];

    // Main workflow nodes
    init [label="Initialize Workflow\\n• Load configuration\\n• Set up state", fillcolor="#87CEEB"];
    fetch [label="Fetch News\\n• Search articles\\n• Score relevance", fillcolor="#DDA0DD"];
    summarize [label="Summarize Topic\\n• Extract key points\\n• Create overview", fillcolor="#F0E68C"];
    review [label="Review Quality\\n• Assess summaries\\n• Generate feedback", fillcolor="#FFA07A"];
    generate [label="Generate Newsletter\\n• Create HTML/MD\\n• Save outputs", fillcolor="#98FB98"];

    // Decision node
    decision [label="More Topics?", shape=diamond, fillcolor="#FFE4B5"];

    // Define edges
    start -> init [label="begin"];
    init -> fetch [label="initialized"];
    fetch -> summarize [label="articles fetched"];
    summarize -> decision;
    decision -> fetch [label="Yes\\n(next topic)", style=dashed];
    decision -> review [label="No\\n(all done)"];
    review -> generate [label="quality checked"];
    generate -> end [label="completed"];

    // Add subgraph for parallel processing
    subgraph cluster_parallel {
        label="Parallel Mode (Optional)";
        style=dashed;
        color=gray;

        pfetch1 [label="Fetch Topic 1", fillcolor="#E0E0E0"];
        pfetch2 [label="Fetch Topic 2", fillcolor="#E0E0E0"];
        pfetch3 [label="Fetch Topic 3", fillcolor="#E0E0E0"];
        pmerge [label="Merge Results", shape=invtrapezium, fillcolor="#E0E0E0"];

        pfetch1 -> pmerge;
        pfetch2 -> pmerge;
        pfetch3 -> pmerge;
    }

    // Legend
    subgraph cluster_legend {
        label="Legend";
        style=solid;
        color=black;

        leg1 [label="Process Node", fillcolor="#87CEEB"];
        leg2 [label="Decision Point", shape=diamond, fillcolor="#FFE4B5"];
        leg3 [label="Loop Back", style=dashed];
    }
}
    """

    return dot_content


def create_mermaid_workflow():
    """Create a Mermaid diagram of the workflow."""

    mermaid_content = """
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
    """

    return mermaid_content


def create_state_flow_diagram():
    """Create a diagram showing state evolution through the workflow."""

    state_diagram = """
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
    """

    return state_diagram


def save_diagrams():
    """Save all diagrams to files."""

    output_dir = Path("docs/diagrams")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save Graphviz DOT file
    dot_content = create_graphviz_workflow()
    dot_file = output_dir / "workflow.dot"
    dot_file.write_text(dot_content)
    print(f"✅ Saved Graphviz diagram to {dot_file}")

    # Save Mermaid diagram
    mermaid_content = create_mermaid_workflow()
    mermaid_file = output_dir / "workflow.mmd"
    mermaid_file.write_text(mermaid_content)
    print(f"✅ Saved Mermaid diagram to {mermaid_file}")

    # Save state diagram
    state_content = create_state_flow_diagram()
    state_file = output_dir / "state_flow.mmd"
    state_file.write_text(state_content)
    print(f"✅ Saved State diagram to {state_file}")

    # Create README with all diagrams
    readme_content = f"""# AI News LangGraph Workflow Diagrams

## 1. Main Workflow (Graphviz)

To render the Graphviz diagram:
```bash
dot -Tpng workflow.dot -o workflow.png
dot -Tsvg workflow.dot -o workflow.svg
```

## 2. Workflow Flow (Mermaid)

```mermaid
{mermaid_content}
```

## 3. State Evolution

```mermaid
{state_content}
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
"""

    readme_file = output_dir / "README.md"
    readme_file.write_text(readme_content)
    print(f"✅ Saved README to {readme_file}")


def generate_png_with_graphviz():
    """Try to generate PNG if graphviz is installed."""
    try:
        import subprocess

        dot_file = "docs/diagrams/workflow.dot"
        png_file = "docs/diagrams/workflow.png"

        result = subprocess.run(
            ["dot", "-Tpng", dot_file, "-o", png_file],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ Generated PNG diagram at {png_file}")
        else:
            print(f"⚠️  Could not generate PNG: {result.stderr}")
            print("   Install Graphviz to generate images: brew install graphviz")
    except FileNotFoundError:
        print("⚠️  Graphviz not installed. Install with: brew install graphviz")
    except Exception as e:
        print(f"⚠️  Error generating PNG: {e}")


def print_ascii_workflow():
    """Print a simple ASCII representation of the workflow."""

    ascii_workflow = """
    ┌─────────────────────────────────────────────────────────┐
    │                 AI News LangGraph Workflow              │
    └─────────────────────────────────────────────────────────┘

                            ┌──────┐
                            │START │
                            └───┬──┘
                                │
                        ┌───────▼────────┐
                        │   Initialize   │
                        │    Workflow    │
                        └───────┬────────┘
                                │
                ┌───────────────▼────────────────┐
                │         Fetch News             │
                │   (for current topic)          │
                └───────────────┬────────────────┘
                                │
                        ┌───────▼────────┐
                        │   Summarize    │
                        │     Topic      │
                        └───────┬────────┘
                                │
                          ┌─────▼─────┐
                          │   More    │
                      ┌───│  Topics?  │───┐
                      │   └───────────┘   │
                      │Yes                │No
                      │                   │
                      └──────────┐        │
                                 │        │
                         ┌───────▼────────▼─┐
                         │  Review Quality  │
                         │  (Self-Reviewer) │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │    Generate      │
                         │   Newsletter     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
              ┌─────▼────┐ ┌─────▼────┐ ┌─────▼────┐
              │   HTML   │ │Markdown  │ │   JSON   │
              └──────────┘ └──────────┘ └──────────┘
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                             ┌────▼────┐
                             │   END   │
                             └─────────┘
    """

    print(ascii_workflow)


def main():
    """Main function to generate all visualizations."""

    print("=" * 60)
    print("   AI News LangGraph Workflow Visualization Generator")
    print("=" * 60)
    print()

    # Print ASCII version
    print("ASCII Workflow Diagram:")
    print_ascii_workflow()

    # Save diagram files
    print("\nGenerating diagram files...")
    save_diagrams()

    # Try to generate PNG
    print("\nAttempting to generate PNG...")
    generate_png_with_graphviz()

    print("\n" + "=" * 60)
    print("✨ Visualization generation complete!")
    print("\nNext steps:")
    print("1. Open workflow_visualization.ipynb in Jupyter")
    print("2. View diagrams in docs/diagrams/")
    print("3. Generate images with Graphviz or Mermaid CLI")
    print("=" * 60)


if __name__ == "__main__":
    main()