"""services/visual_prompt_generator.py

Stage 5: Visual Prompt Generator Service.
Translates a verified LinkedIn post into a structured VisualBrief JSON output.
"""

import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
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
    model_name: str = "openai/gpt-oss-20b",
) -> VisualBrief:
    """Generates a structured VisualBrief from a verified LinkedIn post."""
    parser = JsonOutputParser(pydantic_object=VisualBrief)

    # Format base system prompt
    formatted_system_prompt = VISUAL_GENERATOR_SYSTEM_TEMPLATE.format(
        brand_constraints=FIXED_BRAND_PROMPT_BLOCK,
        negative_prompt=GLOBAL_NEGATIVE_PROMPT,
    )

    # Escape curly braces in format instructions so ChatPromptTemplate doesn't treat them as f-string variables
    format_instructions = parser.get_format_instructions().replace("{", "{{").replace("}", "}}")
    formatted_system_prompt += f"\n\n{format_instructions}"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", formatted_system_prompt),
            (
                "human",
                "Generate the visual brief for the following verified post:\n\n{final_post}",
            ),
        ]
    )

    llm = ChatGroq(
        model=model_name,
        temperature=0.2,
        max_tokens=1024,
        model_kwargs={"response_format": {"type": "json_object"}},
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chain = prompt | llm | parser

    # Parses directly into the VisualBrief Pydantic model
    raw_dict = chain.invoke({"final_post": final_post})
    return VisualBrief(**raw_dict)


if __name__ == "__main__":
    # Sanity check / manual test run
    sample_post = (
        "OLTP databases handle high-frequency transactional writes, but running "
        "heavy analytical queries on them causes lock contention.\n\n"
        "By setting up Change Data Capture (CDC), operational writes are decoupled "
        "from analytical reads. Data flows seamlessly from OLTP to OLAP without impacting production."
    )

    brief = generate_visual_brief(sample_post)
    print("\n=== GENERATED VISUAL BRIEF ===")
    print(f"Visual Concept:\n{brief.visual_concept}\n")
    print(f"Image Prompt:\n{brief.image_prompt}\n")
    print(f"Negative Prompt:\n{brief.negative_prompt}\n")
    print(f"Alt Text:\n{brief.accessibility_alt_text}\n")