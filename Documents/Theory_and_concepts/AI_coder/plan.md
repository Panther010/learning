# AI for Coders — Revision Notes

## 1. The Learning Roadmap (3 Buckets)

A useful way to organize *anything* you learn in this space — every new tool/topic falls into one of these:

| Bucket                | Meaning                                                                                                                             |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| **Core Skills**       | The underlying *concepts/skills* you need regardless of tool (prompting, context management, debugging with AI, agent design, etc.) |
| **Products/Features** | The actual *tools* you use — IDEs, CLIs, plugins, and their specific features.                                                      |
| **Projects**          | Hands-on things you *build* to actually practice and cement the skill — reading about it isn't enough.                              |

> Think of it like learning to cook: Core Skills = knife skills & techniques, Products = the specific oven/gadgets you use, Projects = the actual dishes you cook to get better.

---

## 2. The Learning Journey (Weekly Progression)

A typical progression as you go deeper into AI-assisted coding:

- **Week 1 — Vibe Coding**
  The starting point: describing what you want in plain English and letting the AI write the code, with light review. Fast, fun, but can get messy on bigger projects if you're not careful.
- **Week 2 — Vibe Engineering (as a pro)**
  Leveling up — bringing *engineering discipline* into vibe coding: proper specs, testing, incremental steps, and validating results instead of just accepting whatever the AI outputs.
- **Week 3 — Agentic Engineering**
  The most advanced level — designing **systems of AI agents** (with tools, memory, and autonomy) that can handle multi-step engineering work with much less hand-holding.

> Simple way to remember: **Vibe Coding** = "let it drive", **Vibe Engineering** = "let it drive, but you're a strict backseat driver", **Agentic Engineering** = "you design the whole car and the roads it drives on."

---

## 3. The Products Landscape

AI coding tools generally come in three flavors:

| Category   | What it is                                                                   | Examples                                                      |
|------------|------------------------------------------------------------------------------|---------------------------------------------------------------|
| **IDE**    | A full code editor built *around* AI assistance from the ground up.          | Cursor, Codex, Antigravity, Windsurf                          |
| **Plugin** | An AI extension added *on top of* an existing editor you already use.        | VS Code + GitHub Copilot                                      |
| **CLI**    | A terminal-based AI coding agent — no GUI editor needed, just your terminal. | Claude Code, Cursor CLI, Codex CLI, Gemini CLI, OpenCode, Amp |

---

## 4. The 8 Stages of AI Coding Maturity

A rough "maturity ladder" of how developers progress in using AI for coding, from least to most autonomous:

1. **AI autocomplete** — e.g., ChatGPT open in another tab; you copy-paste snippets manually.
2. **Coding agent in IDE sidebar, asks permission** — agent suggests changes, but *you* approve every single one.
3. **Coding agent in IDE sidebar, YOLO mode** — agent auto-approves its own changes without asking each time.
4. **Coding agent in IDE main window, YOLO mode (check diffs)** — the agent *is* your main workspace now; you just review the diffs after the fact.
5. **Coding agent in CLI, YOLO (diffs scroll by)** — working entirely from the terminal, changes flying by; you spot-check rather than review everything.
6. **Multi-agent in CLI (3–5 agents)** — running several agents in parallel on different parts of a project.
7. **10+ agents in CLI, manually managed** — scaling up further, but still requires you to coordinate them.
8. **Agent orchestrates agents** — the top of the ladder: a "manager" AI coordinates other AI agents itself, with minimal human coordination needed.

> This isn't necessarily a "goal to reach stage 8" — it's a way to recognize *where* you (or a team) currently sit, and that higher stages need more trust, guardrails, and process maturity to use safely.

---

## 5. The 5 Principles of Successful Vibe Coding

1. **Invest in `AGENT.md`**
   Write a clear file the AI reads before working, covering:
   - **Spec** — what you're actually building
   - **Style** — coding conventions/patterns to follow
   - **Success criteria** — how to know the task is actually done
   > Example: *"This is a Next.js app. Use TailwindCSS only. A task is done when `npm test` passes and the feature works in the browser."*

2. **Start Simple**
   Don't ask for the whole complex system in one shot — begin with the smallest working version, then build up.

3. **Work Incrementally, Test Constantly, Validate Success Criteria**
   Small steps, checked often. Don't let the AI run for 30 minutes unsupervised on a huge task — you'll have a bigger mess to untangle if something's wrong.

4. **Don't Get Lazy — Challenge and Demand Evidence**
   Don't just accept "it works" — ask the AI to *prove* it (show test output, walk through the logic, show the actual running result). Treat AI claims the way you'd treat a junior dev's claims: verify.

5. **Handle Frustration With Style**
   When the AI gets stuck or loops on the same mistake, stay calm and methodical (e.g., roll back, rewrite the prompt, break the task down further) rather than getting frustrated and forcing bad fixes.

---

## 6. Claude Code — Session Management Commands

| Command                                                  | What it does                                                                                                                                                               |
|----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Checkpoint**                                           | An automatic snapshot taken before each edit / with every prompt — no setup needed, it just happens as you work.                                                           |
| **`/rewind`** (alias `/checkpoint`, or double-tap `Esc`) | Opens a menu to roll back the **code**, the **conversation**, or **both** to an earlier checkpoint — like an "undo button" for an entire agent session, not just one file. |
| **`/resume`** (or `claude --resume` / `--continue`)      | Reopen a **past saved session** (even from a previous terminal restart) and continue exactly where you left off, with full history.                                        |

> Difference to remember: **Resume** = go back to an *entire past conversation*. **Rewind** = go back to an *earlier point inside* the current/past conversation.

**Ralph Loop**
A community-popularized technique (named after Ralph Wiggum from *The Simpsons* — "keeps trying the same thing until it works") for running a coding agent **autonomously in a loop**: it reads a requirements file, picks the next unfinished task, implements it, tests it, commits, and repeats — until everything's done. Progress is tracked via files/git rather than relying on the conversation memory, and each loop iteration often starts with a clean context. Useful for unattended, long-running feature-building, but needs a very clear task list to work well (it's described by its creator as *"deterministically bad in an undeterministic world"* — good for grinding through well-defined work, not a replacement for engineering judgment).

---

## 7. MCP (Model Context Protocol) — Deeper Dive

**Architecture — Host → Client → Server**
- **Host** — the AI application the user directly interacts with (e.g., Claude Code, Claude Desktop).
- **Client** — a component *inside* the host that manages the connection to one specific MCP server (one client per server).
- **Server** — an external program that exposes capabilities (tools, data, prompts) to the AI through the MCP standard.

> Analogy: Host = your phone, Client = the specific app on it (like a banking app), Server = the bank's actual backend system the app talks to.

**Local vs Remote MCP Servers**
- **Local MCP server** — runs directly on your own machine (e.g., a filesystem server), usually communicating via `stdio` (standard input/output) — fast, no network needed.
- **Remote MCP server** — hosted elsewhere and accessed over the network (e.g., via HTTP/SSE) — useful for shared or cloud-based tools (like a company database or SaaS integration).

**`claude mcp remove`**
The CLI command to **disconnect/remove** a configured MCP server from Claude Code. (Related: `claude mcp list` to see connected servers, `claude mcp add` to connect a new one.)

---

## 8. Skills — Deeper Dive

**What are Skills?**
Lightweight, simple **instructions written as Markdown files** that teach an agent how to do a specific job — an alternative, simpler way to extend an agent compared to building a full custom tool.

**Why use them:**
- **Lightweight & simple** — just a markdown file, easy to write.
- **Progressive disclosure** — reduces context overhead by only loading detail *as needed* (see below).
- **Easy to make & share** — no code required for the basic version.
- **Can run local scripts** — an alternative "type of tool" the agent can invoke.

**Trade-offs / limitations:**
- Not as flexible/powerful as full custom tools.
- Triggering is somewhat **ad-hoc** — the model decides when a skill seems relevant, which isn't always predictable.
- **Discovery is a "Wild West"** — no strong standard yet for how skills get found/shared across the ecosystem.
- The whole feature is **still evolving**.

**3 Levels of Progressive Disclosure**
The idea: don't dump the *whole* skill into context at once — reveal more detail only as it becomes relevant.
1. **Metadata** — just the name, description, and *when it should trigger*. Cheapest to keep in context at all times.
2. **Instructions** — the actual workflow guidance, steps, and code snippets — loaded once the skill is actually triggered.
3. **Resources + Code** — deeper reference material and scripts that can be *run*, only pulled in when truly needed.

**File System Structure**
Skills live as folders with a defined structure:
```
.claude/
  skills/
    my-great-skill/
      SKILL.md
      scripts/
```
Skills can live in your **project root**, your **home directory** (for global/personal skills), or nested in **subdirectories** — giving flexibility on scope (project-specific vs. always-available).

**Skill Marketplaces**
Places to discover/share skills:
- Anthropic's official GitHub repo (example skills)
- Community sites like **skills.sh**

---

## 9. Plugins — Deeper Dive

**What are Plugins?**
A **bundle** of features — can include MCP servers, Skills, and custom Commands (plus other capabilities) — packaged together as one installable unit.

**Key traits:**
- **Simplest** overall option to extend Claude Code (compared to configuring MCP/Skills separately).
- **Best trade-off** between context usage and capability.
- **Commands are explicitly triggered** (e.g., typing `/my-command`) — unlike Skills, which trigger somewhat automatically/ad-hoc.
- Currently **only available in Claude Code**.
- **Least configuration needed** to get going.
- Downside: may bundle **more functionality than you actually need**, adding bloat.
- Anthropic maintains an official **plugin marketplace** on GitHub for discovering community/official plugins.

**Feature Dev**
Refers to the structured *process* of using Claude Code to develop software — going from an idea, to planning, to implementation, to adding a new feature in a real codebase — often assisted by plugins/skills/commands working together.

---

## 10. Debugging Strategy With AI

A disciplined approach to debugging with an AI coding agent (rather than just repeatedly saying "fix it"):

1. **Snapshot — commit first**
   Run a `git commit` *before* letting the agent touch anything, so you always have a safe point to roll back to.
2. **Paste the trace, let it figure out**
   Give the agent the actual error/stack trace and let it investigate rather than guessing at symptoms yourself.
3. **Guide it with a `debug.md`**
   A structured file/prompt guiding the agent through a proper debugging method:
   - **Reproduce consistently** — confirm you can trigger the bug reliably.
   - **Investigate hypotheses** — form and test theories about the cause.
   - **Demonstrate root cause** — actually prove *why* it's happening, not just patch symptoms.
   - **Fix and prove** — apply the fix and verify it actually resolves the issue (e.g., via a test).
   - **Lesson learned in `CLAUDE.md`** — record the insight so future sessions (and future you) don't repeat the same mistake.

**Systematic Debugging**
The umbrella term for this whole approach — treating debugging as a **repeatable, evidence-based process** (reproduce → hypothesize → prove root cause → fix → verify → document) rather than trial-and-error prompting.

---

### Quick Recap Table

| Term                   | One-liner                                                       |
|------------------------|-----------------------------------------------------------------|
| Vibe Coding            | Describe it, let AI write it, light review                      |
| Vibe Engineering       | Vibe coding + real engineering discipline                       |
| Agentic Engineering    | Designing systems of autonomous AI agents                       |
| IDE / Plugin / CLI     | Three shapes AI coding tools come in                            |
| 8 Stages               | Maturity ladder from autocomplete → agents orchestrating agents |
| AGENT.md               | File defining spec, style, and success criteria for the AI      |
| Checkpoint             | Auto-snapshot before every edit                                 |
| /rewind                | Roll back code/conversation to an earlier checkpoint            |
| /resume                | Reopen an entire past session                                   |
| Ralph Loop             | Autonomous loop: pick task → build → test → commit → repeat     |
| MCP Host/Client/Server | App you use → connector inside it → external tool provider      |
| Local vs Remote MCP    | Runs on your machine vs. hosted elsewhere over network          |
| Skill                  | Markdown-based lightweight instruction set for the agent        |
| Progressive Disclosure | Load only metadata → instructions → resources, as needed        |
| Plugin                 | Bundle of MCP + Skills + Commands, simplest to install          |
| Systematic Debugging   | Reproduce → hypothesize → prove root cause → fix → document     |



Chaos --> YOLO, Ralph Loops, GSD, Swarms
CONTROL  ---> Use of files, Self -correcting, Sandboxes, Orchestration
The goal is controlled chaos


Pro features
/command creation using skills or command
build agent and sub agent