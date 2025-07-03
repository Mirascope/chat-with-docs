import argparse
import asyncio
import json
import os
from typing import Annotated, cast

import lilypad
from dotenv import load_dotenv
from lilypad.generated.types.span_more_details import SpanMoreDetails
from lilypad.generated.types.span_public import SpanPublic
from mirascope import llm, prompt_template
from mirascope.core import FromCallArgs
from pydantic import BaseModel, Field

load_dotenv()
lilypad.configure()


class JudgeResults(BaseModel):
    question_md: Annotated[str, FromCallArgs()]
    answer_md: Annotated[str, FromCallArgs()]
    docs: Annotated[list[str], FromCallArgs()]
    reasoning: str = Field(description="The reasoning process of the judge")
    is_correct: bool = Field(description="Whether the answer is correct")


@lilypad.trace(versioning="automatic")
@llm.call(provider="openai", model="gpt-4o-mini", response_model=JudgeResults)
@prompt_template("""SYSTEM: You are a helpful assistant that judges the correctness of an answer to a question.

<criteria>
- Correct answers should be based on provided documents.
</criteria>

<question>
{question_md}
</question>
<answer>
{answer_md}
</answer>
<docs>
{docs}
</docs>
""")
async def judge(question_md: str, answer_md: str, docs: list[str]): ...  # noqa: ANN201


async def get_child_span_by_name(
    trace: SpanPublic, name: str, client: lilypad.AsyncLilypad
) -> SpanMoreDetails:
    span = next(
        t for t in trace.child_spans if getattr(t.function, "name", None) == name
    )
    return await client.spans.get(span.uuid_)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--function_uuid", type=str, default="dd75bac5-bde0-4e55-9bf6-7c9437e8b3a2"
    )
    parser.add_argument("--trace_id", type=str, required=True)
    args = parser.parse_args()

    client = lilypad.AsyncLilypad(
        base_url="https://lilypad-api.mirascope.com/v0",
        api_key=os.environ["LILYPAD_API_KEY"],
    )
    traces = await client.projects.functions.spans.list_paginated(
        os.environ["LILYPAD_PROJECT_ID"], args.function_uuid
    )
    trace = next(t for t in traces.items if t.trace_id == args.trace_id)
    docs_span = await get_child_span_by_name(trace, "get_docs", client)
    docs = json.loads(docs_span.output or "[]")
    annotation = (trace.annotations or [])[0]
    question_md: str = cast(str, (annotation.span.arg_values or {})["user_message"])
    answer_md: str = annotation.span.output or ""

    result = await judge(question_md, answer_md, docs)
    print(result.reasoning, "\n", f"Is correct: {result.is_correct}")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
