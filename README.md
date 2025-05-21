# Chat with Docs

Building a "Chat with Docs" solution for Mirascope, demonstrating how to build an AI application with best practices.

## Quick Start

Start the chat application with:

```bash
uv run chat_with_docs/main.py
```

## Project Philosophy

Building AI can feel overwhelming, but it doesn't have to be. This project demonstrates how to incrementally build a real AI system using evaluation-driven development:

- Run experiments to improve the system
- Improve the fidelity/coverage of evaluation
- Improve the automation of evaluation

We'll focus on making many small, quick steps instead of trying to do too much too fast. Our approach will prevent the common pitfall of implementing too much complexity without proper process and methodology.

## Development Workflow

1. **Issue Creation**: An issue is opened on the GitHub project describing in detail what should be done, with references to techniques planned for use
2. **Feedback Collection**: Mirascope team provides feedback on the item
3. **Development Preparation**: After feedback is addressed, development will commence
4. **Live Streaming**: Development will generally be livestreamed on a schedule (2 days a week for 2-3 hours at a time)
5. **Next Issue Planning**: The next issue should be prepared by the end of the live stream day to allow time for feedback
6. **Development Process**: Each live stream will begin by reviewing the issue and briefly discussing the techniques to be used

## Implementation Strategy

We'll follow this incremental approach:

1. Create minimal scaffolding without any AI to verify instrumentation
2. Start with a small set of test queries (about 3)
3. Implement the simplest AI solution possible
4. Run evaluations with the small test set
5. Plan experiments focusing on simple interventions:
   - Basic prompt engineering
   - Retrieval-Augmented Generation (RAG)
6. Expand evaluation fidelity with new queries
7. Continue experimenting and iterating
8. Scale evaluation with AI judges and active learning when needed

Throughout the development process, we'll link to relevant "Effective AI Engineering" tips and best practices.