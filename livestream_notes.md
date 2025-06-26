# Livestream: Rag Implementation with Best Practices

Some notes on what we are doing:

- building a RAG application to "chat with docs" for the mirascope open source library
- starting with only minimal repository setup (pre-commit, linting, continuous integration, etc)
- will be running through the entire process live; no real preparation done. So you'll see me fumble through everything
- All open source, so you can track and watch the progress
- Eventually this will actually be deployed too!

## What I hope to show

An easy way to go from nothing to a RAG app with evaluation. I focus a lot on processes that are incremental and iterative. So no step ever feels overwhelming. This helps you build momentum and ultimately leads to better systems.

## Today

1. Build simplest chat app (static hardcoded response from the bot)
2. Add tracking/instrumentation with lilypad
3. Collect ~5 queries from mirascope slack to form an initial eval set
4. Replace the static hardcoded response with an LLM function (using mirascope)
5. Run an eval loop
6. Collect documentation
7. Create bm25 index
8. Apply RAG
9. Re-run eval
10. Collect more queries (if time)