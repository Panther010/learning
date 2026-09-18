# services/content_strategist.py
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import ContentStrategy, TechnicalAnalysis
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


def plan_content_strategy(analysis: TechnicalAnalysis) -> ContentStrategy:
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.2,
    )

    parser = PydanticOutputParser(pydantic_object=ContentStrategy)

    template = """
System: You are a Lead Technical Content Strategist for senior data engineering audiences.
Task: Design a content execution strategy using the provided technical analysis.

CONTRACT & FORMATTING RULES:
1. `post_format`: Select EXACTLY ONE of:
   - "Problem-Solution Flow"
   - "Key-Value Tradeoff Bullets"
   - "Architecture Breakdown"
   - "Post-Mortem Style Lesson"
   (NOTE: Markdown tables are strictly prohibited by the renderer/writer).

2. `visual_concept`: Design ONLY a single-line horizontal sequence or bulleted text workflow.
   - Example: `Producer -> Kafka -> Flink -> Iceberg`
   - STRICTLY PROHIBITED: Multi-line ASCII diagrams, box drawings (`+---+`), or vertical arrows (`|`).

3. `tags`: Generate EXACTLY 3 to 5 relevant technical hashtags (e.g. ["#DataEngineering", "#DistributedSystems", "#SystemDesign", "#Kafka"]).

INPUT ANALYSIS:
- Topic: {topic}
- Core Lesson: {core_lesson}
- Misconception: {common_misconception}
- Takeaway: {practical_takeaway}
- Architecture: {architecture_pattern}
- Tradeoffs: {useful_comparison}

{format_instructions}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=[
            "topic",
            "core_lesson",
            "common_misconception",
            "practical_takeaway",
            "architecture_pattern",
            "useful_comparison",
        ],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    chain = prompt | llm | parser

    return chain.invoke({
        "topic": analysis.topic,
        "core_lesson": analysis.core_lesson,
        "common_misconception": analysis.common_misconception,
        "practical_takeaway": analysis.practical_takeaway,
        "architecture_pattern": analysis.architecture_pattern,
        "useful_comparison": analysis.useful_comparison,
    })


# ==========================================
# Validation Entry Point
# ==========================================
if __name__ == "__main__":
    from services.technical_analyzer import analyze_technical_notes
    from shared.path_utils import get_project_root

    sample_file = (
        get_project_root() / "documents/linkedin/raw/oltp_vs_olap.txt"
    )

    if sample_file.exists():
        print("--- Stage 1: Running Analyzer ---")
        raw_text = sample_file.read_text(encoding="utf-8")
        tech_analysis = analyze_technical_notes(raw_text)

        print("\n--- Stage 2: Running Content Strategist ---")
        strategy = plan_content_strategy(tech_analysis)

        print("\nValidated Content Strategy Output:")
        print(f"• Format Selected: {strategy.post_format}")
        print(f"• Post Angle: {strategy.angle}")
        print(f"• Hook Angle: {strategy.hook_angle}")
        print(f"• Visual Concept Layout:\n{strategy.visual_concept}")
        print(f"• Hashtags: {strategy.tags}")