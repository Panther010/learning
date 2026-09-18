import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path
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
    """Evaluates a generated LinkedIn post against 8 strict technical and platform quality criteria."""
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.0,  # Zero temperature for strict, deterministic evaluation
    )

    parser = PydanticOutputParser(pydantic_object=ValidationResult)

    template = """
System: You are an extremely strict Principal Data Architect and Content Quality Auditor.
Your job is to evaluate a generated LinkedIn post against 8 explicit quality dimensions and platform rendering constraints.

INPUT CONTEXT:
1. ORIGINAL TECHNICAL ANALYSIS:
   - Topic: {topic}
   - Core Lesson: {core_lesson}
   - Common Misconception: {common_misconception}
   - Practical Takeaway: {practical_takeaway}

2. GENERATED LINKEDIN POST TO AUDIT:
{generated_post}

==================================================
EVALUATION CHECKLIST (YOU MUST AUDIT ALL 8 POINTS):
==================================================
1. Useful Hook (`has_useful_hook`):
   - MUST be scroll-stopping and directly target data engineers.
   - AUTOMATIC FAIL: Opens with generic greetings, alarm emojis (🚨), or weak rhetorical questions ("Assuming OLTP can...?", "Did you know...?").

2. Technical Accuracy (`is_technically_accurate`):
   - Facts MUST be accurate to real-world database/data systems engineering.
   - MUST match the input analysis without hallucinating flawed advice.

3. Understandable & Mobile-Scannable (`is_understandable_and_scannable`):
   - MUST use clean line breaks, concise paragraphs, and mobile-friendly bullet points.
   - AUTOMATIC FAIL: Contains Markdown tables (`|---|`), multi-line ASCII flow diagrams (`+---+`, `|`, `--->`), or Markdown headers (`###`, `##`). LinkedIn CANNOT render these properly.

4. Free of Fluff (`is_free_of_fluff`):
   - MUST omit conversational filler (e.g., "Here is a breakdown", "Let's dive in", "In today's fast-paced world").
   - Every sentence must deliver concrete value.

5. Teaches Something Concrete (`teaches_concrete_lesson`):
   - MUST explain "why" or "how" at a storage/mechanics level (e.g., 8KB row pages vs columnar row groups, disk I/O, lock contention, CDC design).
   - AUTOMATIC FAIL: Reads like a superficial textbook definition list.

6. Clear Takeaway (`has_clear_takeaway`):
   - MUST end with a practical, actionable rule of thumb and an engaging CTA question for data engineers.

7. Reasonable Hashtags (Audited in general checks):
   - MUST include 3-5 relevant, non-spammy technical hashtags at the very bottom (e.g., #DataEngineering #SystemDesign).

8. Adds Real Value / Knowledge:
   - Would a Senior Data Engineer or Lead Architect find this insightful enough to bookmark, share, or comment on?

==================================================
STRICT SCORING & FAIL RULES:
==================================================
- If ANY AUTOMATIC FAIL trigger is hit (Markdown tables, ASCII diagrams, Markdown headers, alarm emoji hook, surface textbook writing):
  -> `passed` MUST be set to FALSE.
  -> `score` MUST NOT exceed 6.5.
- Overall `passed` MUST be set to TRUE ONLY if `score >= 7.0` AND all 8 criteria are satisfied.
- `issues`: You MUST list every single failed point as an actionable bullet point explaining why it failed.
- `improvement_suggestions`: Provide explicit instructions on how to rewrite or fix the post.

{format_instructions}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=[
            "topic",
            "core_lesson",
            "common_misconception",
            "practical_takeaway",
            "generated_post",
        ],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    chain = prompt | llm | parser

    result: ValidationResult = chain.invoke({
        "topic": analysis.topic,
        "core_lesson": analysis.core_lesson,
        "common_misconception": analysis.common_misconception,
        "practical_takeaway": analysis.practical_takeaway,
        "generated_post": generated_post,
    })

    print("--- GENERATED POST TO VALIDATE ---\n", post, "\n" + "=" * 50)

    return result


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