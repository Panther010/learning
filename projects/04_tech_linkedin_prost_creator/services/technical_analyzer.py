import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path for local module imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import TechnicalAnalysis
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()


def analyze_technical_notes(raw_post_content: str) -> TechnicalAnalysis:
    """Analyzes raw technical notes and extracts deep data engineering insights.

    Args:
        raw_post_content (str): The raw text extracted from the document.

    Returns:
        TechnicalAnalysis: Pydantic model containing core lesson, misconceptions,
          practical takeaways, and architectural flow.
    """
    # 1. Initialize LLM (Using active Groq model with low temperature for analytical precision)
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.1,
    )


    # 2. Attach Pydantic Schema directly for native structured output
    structured_llm = llm.with_structured_output(TechnicalAnalysis)

    # 3. Prompt optimized strictly for technical extraction (no social media rules)
    template = """
System: You are a Principal Data Architect and Lead Engineer analyzing raw technical notes.
Task: Deeply analyze the provided raw notes and extract technical fundamentals, architectural trade-offs, and practical failure modes.

Rules:
- Focus strictly on technical accuracy, engineering trade-offs, and real-world system behavior.
- Do NOT write social media content, hooks, or marketing prose here.
- Extract clear, punchy engineering takeaways based ONLY on the provided text.

Raw Technical Notes:
{raw_content}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["raw_content"],
    )

    # 4. Chain execution
    chain = prompt | structured_llm

    # Execute chain and return Pydantic object
    analysis_result: TechnicalAnalysis = chain.invoke(
        {"raw_content": raw_post_content}
    )
    return analysis_result


# ==========================================
# Test / Validation Entry Point
# ==========================================
if __name__ == "__main__":
    from shared.path_utils import get_project_root

    # Load sample file for testing Stage 1
    sample_file = (
        get_project_root() / "documents/linkedin/raw/oltp_vs_olap.txt"
    )

    if not sample_file.exists():
        print(f"Error: Sample file not found at {sample_file}")
    else:
        print(f"Reading sample file from: {sample_file}\n")
        content = sample_file.read_text(encoding="utf-8")

        print("--- Running Stage 1: Technical Analyzer ---")
        result: TechnicalAnalysis = analyze_technical_notes(content)

        print("\nSuccessfully parsed into TechnicalAnalysis Pydantic Object:")
        print(f"Type: {type(result)}")
        print("\nValidated Fields:")
        print(f"• Topic: {result.topic}")
        print(f"• Core Lesson: {result.core_lesson}")
        print(f"• Common Misconception: {result.common_misconception}")
        print(f"• Practical Takeaway: {result.practical_takeaway}")
        print(f"• Architecture Pattern: {result.architecture_pattern}")
        print(f"• Useful Comparison: {result.useful_comparison}")

        print("\nJSON Dump:")
        print(result.model_dump_json(indent=2))