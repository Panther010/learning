"""services/visual_prompt_generator.py

Stage 5: Visual Prompt Generator Service.
Translates a verified LinkedIn post into a structured VisualBrief JSON output.
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from schemas import VisualBrief
from shared.brand_guide import (
    FIXED_BRAND_PROMPT_BLOCK,
    GLOBAL_NEGATIVE_PROMPT,
    VISUAL_GENERATOR_SYSTEM_TEMPLATE,
)

load_dotenv()


def generate_visual_brief(
    final_post: str,
    visual_concept: str,
    model_name: str = "openai/gpt-oss-20b",
) -> VisualBrief:
    """Generates a structured VisualBrief from a verified LinkedIn post."""
    formatted_system_prompt = VISUAL_GENERATOR_SYSTEM_TEMPLATE.format(
        brand_constraints=FIXED_BRAND_PROMPT_BLOCK,
        negative_prompt=GLOBAL_NEGATIVE_PROMPT,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", formatted_system_prompt),
            (
                "human",
                "Strategist's visual concept:\n{visual_concept}\n\n"
                "Verified LinkedIn post:\n{final_post}",
            ),
        ]
    )

    llm = ChatGroq(
        model=model_name,
        temperature=0.2,
        max_tokens=512,
        reasoning_format="hidden",
        reasoning_effort="none" if model_name.startswith("qwen/") else "low",
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    structured_llm = llm.with_structured_output(
        VisualBrief,
        method="json_schema",
        strict=True,
    )
    chain = prompt | structured_llm
    return chain.invoke({
        "final_post": final_post,
        "visual_concept": visual_concept,
    })


if __name__ == "__main__":
    # Sanity check / manual test run
    sample_post = (
        "OLTP databases handle high-frequency transactional writes, but running "
        "heavy analytical queries on them causes lock contention.\n\n"
        "By setting up Change Data Capture (CDC), operational writes are decoupled "
        "from analytical reads. Data flows seamlessly from OLTP to OLAP without impacting production."
    )

    brief = generate_visual_brief(sample_post, visual_concept="OLTP database -> CDC pipeline -> OLAP warehouse",)
    print("\n=== GENERATED VISUAL BRIEF ===")
    print(f"Visual Concept:\n{brief.visual_concept}\n")
    print(f"Image Prompt:\n{brief.image_prompt}\n")
    print(f"Negative Prompt:\n{brief.negative_prompt}\n")
    print(f"Alt Text:\n{brief.accessibility_alt_text}\n")
