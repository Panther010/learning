import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import ContentStrategy, TechnicalAnalysis
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


def plan_content_strategy(analysis: TechnicalAnalysis) -> ContentStrategy:
    """Takes a TechnicalAnalysis object and determines the best LinkedIn post format,

    hook angle, and visual strategy.
    """
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.3,
    )

    structured_llm = llm.with_structured_output(ContentStrategy)

    template = """
System: You are a Principal Content Strategist for Senior Data Engineers and Software Architects.
Task: Analyze the technical breakdown below and design a strategic content approach for a LinkedIn post.

Input Technical Analysis:
- Topic: {topic}
- Core Lesson: {core_lesson}
- Common Misconception: {common_misconception}
- Practical Takeaway: {practical_takeaway}
- Architecture Flow: {architecture_pattern}
- Key Tradeoffs: {useful_comparison}

Strategy Instructions:
1. Select the `post_format` that best highlights these specific insights (e.g., 'Comparison Table' for trade-offs, 'Production Post-Mortem' for mistakes).
2. Choose a `hook_angle` that creates immediate tension (e.g., pointing out a costly production mistake or a strong architectural opinion).
3. Design a `visual_concept` (such as an ASCII architecture diagram or side-by-side comparison block) to embed in the post text.
4. Provide up to 3 Title Case technical hashtags.

Format Rules:
- DO NOT suggest Markdown tables or complex ASCII diagrams (LinkedIn does not render them).
- Suggest 'Bullet Matrix', 'Production Post-Mortem', or 'Architectural Breakdown'.
- Visual concepts must rely strictly on standard text bullets (e.g., 🔹, ▪️) or simple 1-line text flows.
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
    )

    chain = prompt | structured_llm

    strategy_result: ContentStrategy = chain.invoke({
        "topic": analysis.topic,
        "core_lesson": analysis.core_lesson,
        "common_misconception": analysis.common_misconception,
        "practical_takeaway": analysis.practical_takeaway,
        "architecture_pattern": analysis.architecture_pattern,
        "useful_comparison": analysis.useful_comparison,
    })

    return strategy_result


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