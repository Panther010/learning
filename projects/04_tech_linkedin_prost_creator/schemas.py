from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


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
        "Problem-Solution Flow",
        "Key-Value Tradeoff Bullets",
        "Architecture Breakdown",
        "Post-Mortem Style Lesson",
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
    is_technically_accurate: bool = Field(
        description=(
            "True if claims match the technical analysis and source notes, with no hallucinations "
            "or flawed advice. Missing optional source details are feedback, not a failure."
        )
    )
    is_understandable_and_scannable: bool = Field(
        description=(
            "True if the post is visually easy to scan, with short paragraphs, useful bullets, and blank lines between blocks. "
            "Prefer short lines and one idea per bullet, but line or bullet length alone is not a failure. "
            "Unicode bullets, arrows, emoji, and limited Unicode bold are allowed; "
            "do not mark down solely for these characters. Plain-text labels are allowed. "
            "Markdown tables and multi-line ASCII art are not allowed."
        )
    )
    is_free_of_fluff: bool = Field(description="True if introductory fluff and filler words are removed.")
    teaches_concrete_lesson: bool = Field(
        description="True if it explains a relevant mechanism, decision, or practical detail for the supplied topic."
    )
    has_clear_takeaway: bool = Field(description="True if ending includes a crisp rule of thumb and engaging CTA.")


class ValidationScoreBreakdown(BaseModel):
    has_useful_hook: float = Field(ge=0, le=10, description="Numeric score for the opening hook, from 0 to 10.")
    is_technically_accurate: float = Field(
        ge=0, le=10, description="Numeric score for factual correctness, from 0 to 10."
    )
    is_understandable_and_scannable: float = Field(
        ge=0, le=10, description="Numeric score for visual scannability and clarity, not line length alone."
    )
    is_free_of_fluff: float = Field(ge=0, le=10, description="Numeric score for concise, useful writing, from 0 to 10.")
    teaches_concrete_lesson: float = Field(
        ge=0, le=10, description="Numeric score for the relevant technical lesson, from 0 to 10."
    )
    has_clear_takeaway: float = Field(
        ge=0, le=10, description="Numeric score for the takeaway and hashtag requirements, from 0 to 10."
    )


class SourceAudit(BaseModel):
    omitted_source_details: List[str] = Field(
        description=(
            "Distinct useful source details not represented in the post's meaning; semantic paraphrases count as present. "
            "These are non-blocking suggestions, not accuracy failures."
        )
    )
    unsupported_post_claims: List[str] = Field(
        description="Claims in the post not supported by the analysis or source notes; empty when none are found."
    )


class ValidationResult(BaseModel):
    score: float = Field(
        ge=0,
        le=10,
        description="Overall score, calculated as the mean of score_breakdown by the application.",
    )
    score_breakdown: ValidationScoreBreakdown = Field(
        description="Numeric 0-10 scores for each criterion; the overall score is their arithmetic mean."
    )
    passed: bool = Field(description="True if score >= 7.0 and no critical factual or quality issues exist")
    criteria: ValidationCriteria = Field(description="Itemized evaluation checklist")
    source_audit: SourceAudit = Field(description="Explicit source omissions and unsupported-claim findings.")
    issues: List[str] = Field(
        description="Blocking factual or quality problems; do not include omissions or line length preferences."
    )
    improvement_suggestions: List[str] = Field(description="Specific rewrite instructions to pass in the next attempt")
    warnings: List[str] = Field(
        description=(
            "Non-blocking suggestions such as omitted source details or long lines; these must not make the post fail."
        )
    )


# ==========================================
# NEW MODEL: Stage 5 Visual Brief Schema
# ==========================================
class VisualBrief(BaseModel):
    visual_concept: str = Field(
        description="One concise sentence explaining the single core technical idea shown in the graphic."
    )
    image_prompt: str = Field(
        description="A complete image-generator prompt for Midjourney/Flux/DALL-E, maximum 110 words."
    )
    negative_prompt: str = Field(
        description="A concise exclusion list specifying what must not appear in the graphic."
    )
    accessibility_alt_text: str = Field(
        description="One human-readable sentence describing the diagram for screen readers / LinkedIn alt text."
    )

    @field_validator("image_prompt")
    @classmethod
    def image_prompt_max_110_words(cls, value: str) -> str:
        if len(value.split()) > 110:
            raise ValueError("image_prompt must contain no more than 110 words")
        return value
