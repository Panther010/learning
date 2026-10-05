# services/post_validator.py
import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import TechnicalAnalysis, ValidationResult
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


MAX_PROSE_WORDS_PER_LINE = 18
MAX_BULLET_WORDS = 15


def _is_line_length_only_note(note: str) -> bool:
    normalized = note.casefold()
    mentions_length = any(
        term in normalized
        for term in (
            "word limit", "word maximum", "maximum", "limit", "too long", "exceeds",
            "over ", "more than", "multiple sentences", "long line", "long bullet",
            "line length", "multiple ideas", "packed onto one line",
        )
    )
    mentions_layout_unit = any(term in normalized for term in ("line", "bullet", "sentence"))
    return mentions_length and mentions_layout_unit


def _is_source_omission_note(note: str) -> bool:
    normalized = note.casefold()
    return (
        "omitt" in normalized
        or "source omission" in normalized
        or "missing source detail" in normalized
        or "source coverage" in normalized
    )


def _post_format_issues(generated_post: str) -> list[str]:
    """Return deterministic, non-blocking line-level layout suggestions."""
    issues = []
    sentence_boundary = re.compile(
        r"(?<=[.!?])\s+(?=\S)",
        flags=re.IGNORECASE,
    )

    for line_number, raw_line in enumerate(generated_post.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        is_bullet = line.startswith(("• ", "◦ ", "- ", "* "))
        if is_bullet:
            bullet_text = line[2:].strip()
            word_count = len(bullet_text.split())
            if word_count > MAX_BULLET_WORDS:
                issues.append(
                    f"Line {line_number}: bullet has {word_count} words "
                    f"(suggested maximum {MAX_BULLET_WORDS}): {line}"
                )
            continue

        # ``vs.`` is common in comparison hooks and its period is not a sentence end.
        # Protect it before splitting so a valid one-sentence hook is not reported twice.
        split_line = re.sub(r"\bvs\.(?=\s)", "vs<ABBR>", line, flags=re.IGNORECASE)
        sentences = [
            part.replace("vs<ABBR>", "vs.").strip()
            for part in sentence_boundary.split(split_line)
            if part.strip()
        ]
        if len(sentences) > 1:
            issues.append(
                f"Line {line_number}: contains {len(sentences)} sentences; "
                f"put each sentence on its own line: {line}"
            )
        for sentence_number, sentence in enumerate(sentences, start=1):
            word_count = len(sentence.split())
            if word_count > MAX_PROSE_WORDS_PER_LINE:
                issues.append(
                    f"Line {line_number}, sentence {sentence_number}: has {word_count} words "
                    f"(suggested maximum {MAX_PROSE_WORDS_PER_LINE}): {sentence}"
                )

    return issues


def _finalize_validation(
    validation: ValidationResult, generated_post: str
) -> ValidationResult:
    """Collect non-blocking layout/coverage feedback and calculate the final score."""
    issues = []
    suggestions = list(validation.improvement_suggestions)
    warnings = list(validation.warnings)
    scores = validation.score_breakdown.model_dump()
    criteria = validation.criteria.model_dump()

    for issue in validation.issues:
        if _is_line_length_only_note(issue) or _is_source_omission_note(issue):
            warnings.append(issue)
        else:
            issues.append(issue)

    format_issues = _post_format_issues(generated_post)
    if format_issues:
        warnings.extend(format_issues)

    omitted_details = validation.source_audit.omitted_source_details
    unsupported_claims = validation.source_audit.unsupported_post_claims
    if omitted_details:
        warnings.append("Source details to consider including: " + "; ".join(omitted_details))
    if unsupported_claims:
        criteria["is_technically_accurate"] = False
        scores["is_technically_accurate"] = min(scores["is_technically_accurate"], 4.0)
        issues.append("Unsupported post claims: " + "; ".join(unsupported_claims))
        suggestions.append("Remove or qualify these unsupported claims: " + "; ".join(unsupported_claims))

    if omitted_details and not unsupported_claims:
        accuracy_notes = [
            issue for issue in issues
            if any(term in issue.casefold() for term in ("technical accuracy", "source coverage", "source detail"))
        ]
        accuracy_blockers = [
            issue for issue in issues
            if any(term in issue.casefold() for term in (
                "factual error", "incorrect", "inaccurate", "unsupported", "hallucinated",
                "contradicts", "false claim", "wrong claim",
            ))
        ]
        if not accuracy_blockers:
            issues = [issue for issue in issues if issue not in accuracy_notes]
            warnings.extend(accuracy_notes)
            criteria["is_technically_accurate"] = True
            scores["is_technically_accurate"] = max(scores["is_technically_accurate"], 7.0)

    if format_issues:
        readability_feedback = [
            issue for issue in issues
            if any(term in issue.casefold() for term in (
                "readability", "scannability", "layout", "formatting", "line", "bullet", "sentence",
            ))
        ]
        layout_blockers = [
            issue for issue in readability_feedback
            if not _is_line_length_only_note(issue)
            and "validation criterion failed" not in issue.casefold()
        ]
        if not layout_blockers:
            issues = [issue for issue in issues if issue not in readability_feedback]
            warnings.extend(readability_feedback)
            criteria["is_understandable_and_scannable"] = True
            scores["is_understandable_and_scannable"] = max(
                scores["is_understandable_and_scannable"], 7.0
            )

    score_to_criterion = {
        "has_useful_hook": "has_useful_hook",
        "is_technically_accurate": "is_technically_accurate",
        "is_understandable_and_scannable": "is_understandable_and_scannable",
        "is_free_of_fluff": "is_free_of_fluff",
        "teaches_concrete_lesson": "teaches_concrete_lesson",
        "has_clear_takeaway": "has_clear_takeaway",
    }
    for score_name, criterion_name in score_to_criterion.items():
        if not criteria[criterion_name]:
            scores[score_name] = min(scores[score_name], 5.0)
        elif scores[score_name] < 7.0:
            criteria[criterion_name] = False

    criterion_labels = {
        "has_useful_hook": "hook clarity",
        "is_technically_accurate": "technical accuracy",
        "is_understandable_and_scannable": "readability and formatting",
        "is_free_of_fluff": "conciseness",
        "teaches_concrete_lesson": "concrete lesson",
        "has_clear_takeaway": "takeaway and hashtags",
    }
    for criterion_name, label in criterion_labels.items():
        if not criteria[criterion_name] and not any(
            label in issue.casefold() for issue in issues
        ):
            issues.append(f"Validation criterion failed: {label}.")

    unique_issues = list(dict.fromkeys(issues))
    unique_suggestions = list(dict.fromkeys(suggestions))
    unique_warnings = list(dict.fromkeys(warnings))
    final_score = round(sum(scores.values()) / len(scores), 1)
    passed = final_score >= 7.0 and all(criteria.values())

    return validation.model_copy(update={
        "score": final_score,
        "score_breakdown": validation.score_breakdown.model_copy(update=scores),
        "criteria": validation.criteria.model_copy(update=criteria),
        "issues": unique_issues,
        "improvement_suggestions": unique_suggestions,
        "warnings": unique_warnings,
        "passed": passed,
    })


def validate_linkedin_post(
    generated_post: str, analysis: TechnicalAnalysis, source_notes: str = ""
) -> ValidationResult:
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="openai/gpt-oss-120b",
        temperature=0.0,
        max_tokens=2048,
        reasoning_format="hidden",
        reasoning_effort="low",
    )

    structured_llm = llm.with_structured_output(
        ValidationResult,
        method="json_schema",
        strict=True,
    )

    template = """
System: You are an extremely strict Principal Data Architect and Content Quality Auditor.
Audit the generated LinkedIn post against platform constraints and quality standards.

INPUT CONTEXT:
1. ORIGINAL TECHNICAL ANALYSIS:
   - Topic: {topic}
   - Core Lesson: {core_lesson}
   - Practical Takeaway: {practical_takeaway}

2. ORIGINAL SOURCE NOTES (authoritative details to preserve):
{source_notes}

3. GENERATED LINKEDIN POST TO AUDIT:
{generated_post}

Return `source_audit.omitted_source_details` as specific supported details missing from the post, and `source_audit.unsupported_post_claims` as specific claims the notes do not support. Use empty lists when none are found. Check the post carefully before marking a detail omitted; semantic paraphrases count as present. Put omissions and preferred line-break suggestions in `warnings`, never in `issues`, and never fail or reduce accuracy/readability scores because a source detail is omitted or a line is long. Unsupported or incorrect claims remain blocking issues. Return an empty `warnings` list when there are no such suggestions.

==================================================
EVALUATION CHECKLIST:
==================================================
1. Useful Hook (`has_useful_hook`): Scroll-stopping line 1 that clearly names the topic or compared options immediately. FAIL if readers cannot tell the subject from the opening sentence, or if it uses generic greetings ("Hey network"), alarm emojis (🚨), or weak rhetorical questions.
2. Technical Accuracy (`is_technically_accurate`): Score factual correctness only. Do not add implementation details or narrow a general source term to a specific product unless the source supports it. Missing source details are non-blocking feedback: report them in `source_audit.omitted_source_details` and `warnings`, but do not fail the accuracy criterion or reduce its score for omissions alone.
3. Understandable & Scannable (`is_understandable_and_scannable`):
   - AUTOMATIC FAIL: Contains Markdown tables (`|---|`), multi-line ASCII diagrams (`+---+`, `|`, `--->`), or Markdown headers (`###`).
   - Inline Unicode arrows (`→`), visible Unicode bullets (`•`, `◦`), limited Unicode bold, and appropriate emoji are allowed; do not lower the score solely for using them.
   - Assess mobile readability by its actual visual scan: short blocks with blank lines, readable paragraphs, and bullets where lists/comparisons benefit from them.
   - Prefer short lines, one sentence per line, and one idea per bullet. These are writing preferences, not hard limits; do not fail or lower the score for line or bullet length alone. Mark this criterion FALSE only when the layout is genuinely difficult to scan, such as dense unbroken paragraphs, missing useful structure, or confusing presentation.
   - Short plain-text labels (for example, `Trade-offs:`) are allowed.
4. Free of Fluff (`is_free_of_fluff`): Zero conversational filler ("Let's dive in").
5. Teaches Something Concrete (`teaches_concrete_lesson`): Explains a relevant mechanism, decision, or practical detail for the supplied topic; do not require examples from unrelated topics.
6. Clear Takeaway & Hashtags (`has_clear_takeaway`):
   - Includes practical rule of thumb + open engineering question.
    - MUST contain EXACTLY 3 to 5 technical hashtags at the bottom. Less than 3 or more than 5 hashtags is a FAIL.
7. Numeric scores: Give each field in `score_breakdown` a 0-10 score that matches its corresponding criterion. Do not deduct for source omissions or line lengths alone. The application calculates the final score as the arithmetic mean.

==================================================
STRICT SCORING RULES:
==================================================
- If ANY AUTOMATIC FAIL trigger is hit (tables, ASCII, headers, bad hook, <3 or >5 hashtags):
  -> `passed` MUST be FALSE.
  -> Score the affected criterion at 5.0 or below. The overall score remains the arithmetic mean and may still be 7.0 or higher; the post must still fail.
- Report useful source omissions as non-blocking `warnings`; assess factual correctness separately.
- If the source contains multiple sections or lists and the post is under 280 words, check carefully for useful omitted details and report them as non-blocking warnings. Never fail on post length or omissions alone.
- Improvement suggestions MUST address the most important content omissions before minor style issues.
- `passed` = TRUE if `score >= 7.0` AND all blocking criteria pass. Source omissions and line-length preferences are not blocking criteria.

"""

    prompt = PromptTemplate(
        template=template,
        input_variables=[
            "topic",
            "core_lesson",
            "practical_takeaway",
            "source_notes",
            "generated_post",
        ],
    )

    chain = prompt | structured_llm

    validation = chain.invoke({
        "topic": analysis.topic,
        "core_lesson": analysis.core_lesson,
        "practical_takeaway": analysis.practical_takeaway,
        "source_notes": source_notes,
        "generated_post": generated_post,
    })
    return _finalize_validation(validation, generated_post)


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
        post = generate_final_post(analysis, strategy, source_notes=raw_text)

        print("--- Running Post Validator ---")
        validation = validate_linkedin_post(post, analysis, source_notes=raw_text)

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
