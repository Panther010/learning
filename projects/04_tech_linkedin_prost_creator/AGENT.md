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
- Keep the post easy to read and paste into LinkedIn: short paragraphs (at most two sentences), normal blank lines, and simple ASCII hyphen bullets (`- `) for lists and comparisons. Keep each bullet to one idea and preferably under 20 words; do not nest or indent bullets.
- Use ordinary punctuation and short labels only when they help scanning. Avoid Unicode bullets, arrows, emoji, Markdown emphasis, tables, and decorative symbols. Retain final hashtags, which are part of the post.
- Preserve useful technical detail without turning every post into a glossary or checklist. Keep risks qualified unless the source confirms they happened.
- The validator must assess the supplied topic, not require mechanics from unrelated subjects.
- If a prompt is changed, update any related validation criteria so generation and validation ask for the same format and quality.

## Code and data dos and don'ts

- Use type hints and keep functions focused; follow the repository's Python and Ruff conventions.
- Keep output formatting in `sanitize_post_content()` consistent with the writer's formatting contract. It should normalize decorative Unicode and arrows but preserve plain ASCII hyphen bullets and useful line breaks. It runs before validation and before saving both passing and review drafts.
- Keep pipeline paths resolved through the existing project path utilities rather than hardcoding machine-specific absolute paths.
- Keep source examples small and factual. Do not commit credentials, generated output, large datasets, or environment files.
- Avoid broad refactors of legacy learning material unless the task requires them.
- Do not overwrite or move user source files or generated artifacts as part of a prompt/code-only change. The pipeline itself moves source files according to its pass/fail route.
- Do not add or run tests unless asked. When verification is requested, prefer focused checks for the changed behavior before broader project commands.
