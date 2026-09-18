import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from schemas import ContentStrategy, TechnicalAnalysis, ValidationResult
from services.content_strategist import plan_content_strategy
from services.post_validator import validate_linkedin_post
from services.post_writer import generate_final_post
from services.technical_analyzer import analyze_technical_notes
from shared.logger import get_logger
from shared.path_utils import get_project_root

logger = get_logger(__name__)


def sanitize_post_content(post_text: str) -> str:
    """Removes raw Markdown bold syntax (**) that LinkedIn doesn't render natively."""
    return post_text.replace("**", "")


def process_single_file(
    file_path: Path,
    output_dir: Path,
    processed_dir: Path,
    review_dir: Path,
) -> dict:
    """Orchestrates Stage 1 -> Stage 2 -> Stage 3 -> Stage 4 for a single text file

    and routes outputs based on validation pass/fail status.
    """
    logger.info(f"Starting Pipeline for: {file_path.name}")

    # Read Raw Text
    raw_text = file_path.read_text(encoding="utf-8")

    # Stage 1: Technical Analysis
    logger.info("Running Stage 1: Technical Analysis...")
    tech_analysis: TechnicalAnalysis = analyze_technical_notes(raw_text)

    # Stage 2: Content Strategy
    logger.info("Running Stage 2: Content Strategy...")
    strategy: ContentStrategy = plan_content_strategy(tech_analysis)

    # Stage 3: Post Generation
    logger.info("Running Stage 3: Post Writing...")
    raw_post = generate_final_post(tech_analysis, strategy)
    final_post = sanitize_post_content(raw_post)

    # Stage 4: Post Validation
    logger.info("Running Stage 4: Post Validation (LLM-as-a-Judge)...")
    validation: ValidationResult = validate_linkedin_post(final_post, tech_analysis)

    base_name = file_path.stem

    # ==========================================
    # ROUTE A: VALIDATION PASSED (Score >= 7.0)
    # ==========================================
    if validation.passed:
        logger.info(f"✅ Validation PASSED for {file_path.name} (Score: {validation.score}/10.0)")

        # Save copy-paste ready LinkedIn post (.txt)
        output_post_path = output_dir / f"{base_name}_post.txt"
        output_post_path.write_text(final_post, encoding="utf-8")

        # Save metadata and audit trail
        output_meta_path = output_dir / f"{base_name}_metadata.json"
        metadata = {
            "source_file": str(file_path.name),
            "processed_at": datetime.now().isoformat(),
            "validation_score": validation.score,
            "validation_criteria": validation.criteria.model_dump(),
            "technical_analysis": tech_analysis.model_dump(),
            "content_strategy": strategy.model_dump(),
        }
        output_meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        # Move source file from raw/ to processed/
        target_processed_path = processed_dir / file_path.name
        shutil.move(str(file_path), str(target_processed_path))
        logger.info(f"Moved source file to: {target_processed_path}")

        return {
            "file_name": file_path.name,
            "topic": tech_analysis.topic,
            "score": validation.score,
            "status": "PASSED",
        }

    # ==========================================
    # ROUTE B: VALIDATION FAILED (Score < 7.0)
    # ==========================================
    else:
        logger.warning(
            f"❌ Validation FAILED for {file_path.name} (Score: {validation.score}/10.0)"
        )

        # Save diagnostic fail report in review_required/ directory
        review_report_path = review_dir / f"{base_name}_FAILED.json"
        failed_report = {
            "source_file": str(file_path.name),
            "evaluated_at": datetime.now().isoformat(),
            "score": validation.score,
            "passed": validation.passed,
            "criteria_checks": validation.criteria.model_dump(),
            "issues_identified": validation.issues,
            "improvement_suggestions": validation.improvement_suggestions,
            "generated_post_draft": final_post,
        }
        review_report_path.write_text(json.dumps(failed_report, indent=2), encoding="utf-8")
        logger.info(f"Saved failure report to: {review_report_path}")

        # DO NOT move source file - leave it in raw/ for manual inspection/retry

        return {
            "file_name": file_path.name,
            "topic": tech_analysis.topic,
            "score": validation.score,
            "status": "FAILED_VALIDATION",
            "issues": validation.issues,
        }


def run_pipeline():
    """Batch processes all .txt files in the raw directory."""
    project_root = get_project_root()
    raw_dir = project_root / "documents/linkedin/raw/"
    processed_dir = project_root / "documents/linkedin/processed/"
    output_dir = project_root / "documents/linkedin/output/"
    review_dir = project_root / "documents/linkedin/review_required/"

    # Ensure all required directory structures exist
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"Raw directory not found: {raw_dir}")

    processed_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    raw_files = list(raw_dir.glob("*.txt"))
    if not raw_files:
        logger.warning(f"No .txt files found to process in {raw_dir}")
        return

    logger.info(f"Found {len(raw_files)} raw file(s) to process.\n")

    summary = []
    for file_path in raw_files:
        try:
            result = process_single_file(
                file_path=file_path,
                output_dir=output_dir,
                processed_dir=processed_dir,
                review_dir=review_dir,
            )
            summary.append(result)
            logger.info(f"Finished processing {file_path.name}\n")
        except Exception as e:
            logger.error(f"Execution Error on {file_path.name}: {e}", exc_info=True)
            summary.append(
                {"file_name": file_path.name, "status": "EXECUTION_ERROR", "error": str(e)}
            )

    # Print Summary Console Alert
    print("\n" + "=" * 60)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    for item in summary:
        if item["status"] == "PASSED":
            print(f"✅ PASSED | File: {item['file_name']} | Score: {item['score']}/10.0")
            print(f"   Topic: {item['topic']}")
            print(f"   Artifacts saved to: documents/linkedin/output/\n")
        elif item["status"] == "FAILED_VALIDATION":
            print(f"❌ REJECTED | File: {item['file_name']} | Score: {item['score']}/10.0")
            print(f"   Topic: {item['topic']}")
            print("   Issues Identified:")
            for issue in item.get("issues", []):
                print(f"   • {issue}")
            print(f"   Diagnostic saved to: documents/linkedin/review_required/\n")
        else:
            print(f"💥 ERROR | File: {item['file_name']} | Exception: {item.get('error')}\n")


if __name__ == "__main__":
    run_pipeline()