# Agent Guide

## Project purpose

This project turns technical source notes into LinkedIn posts and supporting visual briefs. Keep generation topic-agnostic: the same pipeline must work for subjects such as ETL vs ELT and OLTP vs OLAP without carrying facts or examples from one topic into another.

## Project flow

`pipeline.py` processes each `.txt` file in `documents/linkedin/raw/`:

1. **Technical analysis** (`services/technical_analyzer.py`) extracts a structured topic, lesson, misconception, takeaway, architecture pattern, and trade-offs.
2. **Content strategy** (`services/content_strategist.py`) selects one format, angle, hook, visual concept, and relevant hashtags.
3. **Post writing** (`services/post_writer.py`) drafts from the analysis and original source notes.
4. **Sanitization and validation** (`pipeline.py`, `services/post_validator.py`) convert the draft to copy-ready text, validate it, and make one targeted revision attempt if needed.
5. **Visual brief generation** (`services/visual_prompt_generator.py`) runs for validated posts.

On a passing post, the pipeline writes `_post.txt`, `_visual.json`, and `_metadata.json` under `documents/linkedin/output/`, then moves the input to `documents/linkedin/processed/`. On validation failure, it writes a draft and diagnostic report under `documents/linkedin/review_required/` and moves the source to `documents/linkedin/failed/`. Execution errors are logged in the pipeline summary; the source is not moved by that error path.

Run the pipeline from the project root with:

```bash
python pipeline.py
```

The pipeline requires `GROQ_API_KEY` in the environment (a local `.env` is loaded by the services). Stage 1 currently uses `openai/gpt-oss-20b` with an 800-token output cap to keep structured responses within the configured Groq output-token budget. Keep requested structured fields concise if changing this configuration.

## Writing and prompt guidance

- Keep prompts generic. Never put topic-specific facts, lists, examples, trade-offs, or terminology in a shared writer or validator prompt as if they applied to every topic.
- Use the source notes and technical analysis as the factual boundary. Include OLTP/OLAP concepts only when the supplied topic or notes support them; apply the same rule to every other subject.
- Make the first sentence name the topic or compared options and state the central decision or tension. The reader should know the subject before continuing.
- Carry a source-supported example through the explanation and trade-offs. Do not invent incidents, outcomes, metrics, systems, or vendors.
- Preserve all distinct, useful details from the source: named technologies, capabilities, examples, comparisons, constraints, and trade-offs. Combine repetition, but do not compress detailed notes into a brief summary or silently drop whole categories of facts.
- When the source has multiple sections, named examples, or capability/trade-off lists, aim for 300-420 words, expanding when needed to preserve its details. Let genuinely short sources produce shorter posts; never pad with unsupported claims.
- Do not replace a general source term with a specific product, service, or implementation detail unless the source names it. Preserve lists of distinct capabilities and trade-offs instead of collapsing them into vague summaries.
- Validation must compare the draft with the original source notes as well as the condensed analysis. Report useful omissions as non-blocking suggestions; technical accuracy should fail for incorrect or unsupported claims, not omitted details alone. Confirm semantic paraphrases before reporting omissions.
- Keep the post easy to read and paste into LinkedIn: organize it into at least five short blocks separated by blank lines. Prefer one short sentence per line and one idea per bullet; use `•` for main bullets and `◦` for needed sub-points, without indentation. Split long ideas where it improves scanning and preserves natural phrasing. These are preferences, not word-count limits or validation failure conditions.
- Keep opening sentences clear about the topic. Short plain-text labels such as `Trade-offs:` or `Rule of thumb:` may be used where they help scanning.
- LinkedIn-friendly Unicode such as `→`, `•`, `◦`, and appropriate emoji is allowed. Do not penalize it as a special-character or readability issue. Unicode bold is allowed sparingly for the hook or one or two key phrases; the sanitizer converts `**...**` markers. Avoid Markdown tables and decorative symbol clutter. Retain final hashtags, which are part of the post.
- Preserve useful technical detail without turning every post into a glossary or checklist. Keep risks qualified unless the source confirms they happened.
- The validator must assess the supplied topic, not require mechanics from unrelated subjects.
- Pass original source notes to `post_validator.py` so it can assess factual coverage, not just the condensed technical analysis. Keep `post_writer.py`, `post_validator.py`, and `ValidationCriteria` aligned on source coverage, opening clarity, paragraph length, blank lines, labels, and bullet expectations. If one prompt changes, update the matching validator and schema descriptions.
- Keep validation reasons inspectable: use deterministic line-level checks for prose and bullet length as non-blocking suggestions, with exact line numbers and content. The pipeline summary should print these separately from blocking issues.
- Sentence-boundary checks must account for common comparison abbreviations such as `vs.` so a valid topic hook is not falsely counted as multiple sentences.
- Store a 0-10 score for each validation criterion and calculate the overall score as their arithmetic mean. Keep numeric scores consistent with failed criteria. Persist the breakdown, source audit (omitted details and unsupported claims), and non-blocking warnings in pass metadata and failure reports.

## Code and data dos and don'ts

- Use type hints and keep functions focused; follow the repository's Python and Ruff conventions.
- Keep output formatting in `sanitize_post_content()` consistent with the writer's formatting contract. Normalize text with NFC, preserve useful Unicode (including bullets, arrows, and emoji), normalize `->` to `→`, collapse repeated spaces, and keep blank lines. Convert sparse `**bold**` markers to Unicode bold. Write post files as UTF-8 with LF newlines. The sanitizer runs before validation and before saving both passing and review drafts.
- Keep pipeline paths resolved through the existing project path utilities rather than hardcoding machine-specific absolute paths.
- Keep source examples small and factual. Do not commit credentials, generated output, large datasets, or environment files.
- Avoid broad refactors of legacy learning material unless the task requires them.
- Do not overwrite or move user source files or generated artifacts as part of a prompt/code-only change. The pipeline itself moves source files according to its pass/fail route.
- Do not add or run tests unless asked. When verification is requested, prefer focused checks for the changed behavior before broader project commands.
