import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import TechnicalAnalysis, ContentStrategy
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


def generate_final_post(analysis: TechnicalAnalysis, strategy: ContentStrategy) -> str:
    """Takes TechnicalAnalysis and ContentStrategy objects to write a high-value,
    scannable LinkedIn post tailored for senior data engineers.
    """
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-20b",
        temperature=0.7,  # Temperature balance for engaging, fluid copywriting
    )

    template = """
System: You are a Principal Data Architect sharing practical, production-grade engineering insights on LinkedIn.
Task: Write an engaging, high-value technical LinkedIn post that WILL PASS strict platform rendering and quality validation.

==================================================
STRICTLY BANNED ELEMENTS (VIOLATIONS CAUSE AUTOMATIC REJECTION):
==================================================
1. NO Markdown tables (`|---|`). Replace comparisons with bold bullet points.
2. NO multi-line ASCII diagrams or boxes (`+---+`, `|`, `--->`). Flatten workflows into single-line bulleted sequences (e.g., `Step A -> Step B -> Step C`).
3. NO Markdown headers (`###`, `##`). Use ALL CAPS inline section titles instead (e.g., `THE ARCHITECTURE PATTERN:`).
4. NO weak hooks: NEVER open with generic greetings ("Hey network"), alarm emojis (🚨), or rhetorical questions ("Have you ever wondered...?", "Assuming OLTP can...?").
5. NO fluff or conversational filler ("Let's dive in", "Here is a breakdown").

==================================================
INPUT CONTEXT:
==================================================
1. TECHNICAL INSIGHTS:
   - Topic: {topic}
   - Core Lesson: {core_lesson}
   - Common Misconception: {common_misconception}
   - Practical Takeaway: {practical_takeaway}
   - Architecture Pattern: {architecture_pattern}
   - Key Tradeoffs: {useful_comparison}

2. CONTENT STRATEGY:
   - Chosen Post Format: {post_format}
   - Post Angle: {angle}
   - Hook Trigger: {hook_angle}
   - Visual Layout Concept:
{visual_concept}

==================================================
WRITING & STRUCTURAL GUIDELINES:
==================================================
1. HOOK (Line 1): Start with a direct, bold statement derived from the Hook Trigger that immediately calls out a real production pain point.
2. RE-HOOK (Line 2-3): State the exact operational consequence or failure mode (e.g., lock contention, spike in p99 latency, disk I/O thrashing).
3. BODY: Present technical mechanics tailored for Senior Engineers (focus on row pages vs columnar row groups, memory buffer pools, CDC, or query execution):
   - Keep paragraphs to 1-2 short sentences max.
   - Use double line breaks between lines for mobile readability.
   - Use simple bullet points (• or 🔹).
   - If expressing a sequence from the Visual Layout Concept, convert it to a single-line flow: `Source -> Component -> Destination`.
4. TAKEAWAY & CTA:
   - End with the Practical Takeaway framed as a 1-line rule of thumb.
   - Follow with 1 open-ended, technical question asking senior data engineers for their real-world experience.
5. EMOJIS: Use 3-5 tasteful emojis max.

Output ONLY the raw text of the generated LinkedIn post.
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
            "post_format",
            "angle",
            "hook_angle",
            "visual_concept",
        ],
    )

    chain = prompt | llm

    # Execute chain
    response = chain.invoke({
        "topic": analysis.topic,
        "core_lesson": analysis.core_lesson,
        "common_misconception": analysis.common_misconception,
        "practical_takeaway": analysis.practical_takeaway,
        "architecture_pattern": analysis.architecture_pattern,
        "useful_comparison": analysis.useful_comparison,
        "post_format": strategy.post_format,
        "angle": strategy.angle,
        "hook_angle": strategy.hook_angle,
        "visual_concept": strategy.visual_concept,
    })

    # Format tags as hashtags and append to the end
    hashtags = " ".join([f"#{tag.replace('#', '').replace(' ', '')}" for tag in strategy.tags])
    final_post = f"{response.content.strip()}\n\n{hashtags}"

    return final_post


# ==========================================
# End-to-End Test Entry Point (Stages 1 -> 2 -> 3)
# ==========================================
if __name__ == "__main__":
    from services.technical_analyzer import analyze_technical_notes
    from services.content_strategist import plan_content_strategy
    from shared.path_utils import get_project_root

    sample_file = get_project_root() / "documents/linkedin/raw/oltp_vs_olap.txt"

    if sample_file.exists():
        raw_text = sample_file.read_text(encoding="utf-8")

        print("--- Running Stage 1: Technical Analyzer ---")
        tech_analysis = analyze_technical_notes(raw_text)

        print("--- Running Stage 2: Content Strategist ---")
        strategy = plan_content_strategy(tech_analysis)

        print("--- Running Stage 3: Post Writer ---")
        final_linkedin_post = generate_final_post(tech_analysis, strategy)

        print("\n" + "=" * 50)
        print("GENERATED LINKEDIN POST:")
        print("=" * 50 + "\n")
        print(final_linkedin_post)