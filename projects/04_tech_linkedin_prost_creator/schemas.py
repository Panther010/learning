from typing import List, Literal
from pydantic import BaseModel, Field


# ==========================================
# STAGE 1: Technical Analysis Contract
# ==========================================
class TechnicalAnalysis(BaseModel):
    """Represents a deep technical understanding of raw notes prior to content creation."""

    topic: str = Field(description="Short, specific title of the technical topic (1-5 words, e.g., 'OLTP vs OLAP').")
    core_lesson: str = Field(description="The fundamental technical principle or rule (15-25 words).")
    common_misconception: str = Field(description="A common mistake, anti-pattern, or misunderstanding engineers have about this subject.")
    practical_takeaway: str = Field(description="Direct production guidance or rule of thumb to avoid failure.")
    architecture_pattern: str = Field(description="A concise string or flow showing systems and data movement (e.g., 'OLTP -> CDC -> Warehouse -> BI').")
    useful_comparison: str = Field(description="Key side-by-side technical trade-offs (e.g., 'Row storage & low latency vs Columnar & high throughput').")


# ==========================================
# STAGE 2: Content Strategy Contract
# ==========================================
class ContentStrategy(BaseModel):
    """Defines the narrative format and positioning strategy for LinkedIn."""

    post_format: Literal[
        "Comparison Table",
        "Production Post-Mortem",
        "Architecture Deep-Dive",
        "Debunking a Myth",
        "Practical Checklist",
    ] = Field(description="The structural style best suited to present these specific insights.")

    angle: str = Field(description="Perspective or tone (e.g., 'Opinionated Lead Engineer', 'Tutorial', 'Production Lesson Learned').")

    hook_angle: str = Field(description="The emotional or logical trigger for the opening line (e.g., 'Production outage scenario', 'Contrarian statement', 'Common architectural mistake').")

    visual_concept: str = Field(description="Idea or text layout for a visual element in the post (e.g., ASCII flow, key metric matrix, side-by-side bullet block).")

    tags: List[str] = Field(
        description="List of 3 to 5 relevant technical hashtags without spaces",
        min_items=3,
        max_items=5)


# ==========================================
# Stage 4: Validation Schemas
# ==========================================
class ValidationCriteria(BaseModel):
    has_useful_hook: bool = Field(description="True if hook is scroll-stopping and avoids generic clichés/alarm emojis.")
    is_technically_accurate: bool = Field(description="True if facts match TechnicalAnalysis without hallucinated or flawed advice.")
    is_understandable_and_scannable: bool = Field(description="True if layout uses clean line breaks and avoids unrenderable Markdown tables or ASCII blocks.")
    is_free_of_fluff: bool = Field(description="True if introductory fluff and filler words are removed.")
    teaches_concrete_lesson: bool = Field(description="True if it explains 'why' or 'how' (e.g., row pages vs column chunks) rather than surface definitions.")
    has_clear_takeaway: bool = Field(description="True if ending includes a crisp rule of thumb and engaging CTA.")


class ValidationResult(BaseModel):
    score: float = Field(description="Overall quality score between 0.0 and 10.0")
    passed: bool = Field(description="True if score >= 7.0 and no critical formatting/technical issues exist")
    criteria: ValidationCriteria = Field(description="Itemized evaluation checklist")
    issues: List[str] = Field(description="Actionable feedback bullet points explaining what to fix if score < 7.0")
    improvement_suggestions: List[str] = Field(description="Specific rewrite instructions to pass in the next attempt")