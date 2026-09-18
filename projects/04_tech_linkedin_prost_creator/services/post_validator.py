# services/post_validator.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import TechnicalAnalysis, ValidationResult
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


def validate_linkedin_post(
    generated_post: str, analysis: TechnicalAnalysis
) -> ValidationResult:
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.0,
    )

    parser = PydanticOutputParser(pydantic_object=ValidationResult)

    template = """
System: You are an extremely strict Principal Data Architect and Content Quality Auditor.
Audit the generated LinkedIn post against platform constraints and quality standards.

INPUT CONTEXT:
1. ORIGINAL TECHNICAL ANALYSIS:
   - Topic: {topic}
   - Core Lesson: {core_lesson}
   - Practical Takeaway: {practical_takeaway}

2. GENERATED LINKEDIN POST TO AUDIT:
{generated_post}

==================================================
EVALUATION CHECKLIST:
==================================================
1. Useful Hook (`has_useful_hook`): Scroll-stopping line 1. FAIL if generic ("Hey network"), alarm emojis (🚨), or weak rhetorical questions ("Assuming OLTP can...?").
2. Technical Accuracy (`is_technically_accurate`): Factually sound systems architecture principles.
3. Understandable & Scannable (`is_understandable_and_scannable`):
   - AUTOMATIC FAIL: Contains Markdown tables (`|---|`), multi-line ASCII diagrams (`+---+`, `|`, `--->`), or Markdown headers (`###`).
4. Free of Fluff (`is_free_of_fluff`): Zero conversational filler ("Let's dive in").
5. Teaches Something Concrete (`teaches_concrete_lesson`): Explains storage/system mechanics (row pages vs columnar groups, buffer pools, CDC).
6. Clear Takeaway & Hashtags (`has_clear_takeaway`):
   - Includes practical rule of thumb + open engineering question.
   - MUST contain EXACTLY 3 to 5 technical hashtags at the bottom. Less than 3 or more than 5 hashtags is a FAIL.

==================================================
STRICT SCORING RULES:
==================================================
- If ANY AUTOMATIC FAIL trigger is hit (tables, ASCII, headers, bad hook, <3 or >5 hashtags):
  -> `passed` MUST be FALSE.
  -> `score` MUST NOT exceed 6.5.
- `passed` = TRUE ONLY if `score >= 7.0` AND all criteria pass.

{format_instructions}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["topic", "core_lesson", "practical_takeaway", "generated_post"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    return chain.invoke({
        "topic": analysis.topic,
        "core_lesson": analysis.core_lesson,
        "practical_takeaway": analysis.practical_takeaway,
        "generated_post": generated_post,
    })


# ==========================================
# Standalone Test Execution
# ==========================================
if __name__ == "__main__":
    from services.technical_analyzer import analyze_technical_notes
    from services.content_strategist import plan_content_strategy
    from services.post_writer import generate_final_post
    from shared.path_utils import get_project_root

    sample_file = get_project_root() / "documents/linkedin/raw/oltp_vs_olap.txt"

    if sample_file.exists():
        raw_text = sample_file.read_text(encoding="utf-8")
        analysis = analyze_technical_notes(raw_text)
        strategy = plan_content_strategy(analysis)
        post = generate_final_post(analysis, strategy)

        print("--- Running Post Validator ---")
        validation = validate_linkedin_post(post, analysis)

        print(f"\nScore: {validation.score} / 10.0")
        print(f"Passed: {validation.passed}")
        print("\nCriteria Breakdown:")
        print(validation.criteria.model_dump_json(indent=2))

        if validation.issues:
            print("\nIssues Identified:")
            for issue in validation.issues:
                print(f"• {issue}")

        if validation.improvement_suggestions:
            print("\nSuggested Improvements:")
            for suggestion in validation.improvement_suggestions:
                print(f"• {suggestion}")