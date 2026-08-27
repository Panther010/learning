# AI Agents & Agentic Systems — Revision Notes

## 1. The Basics

**AI Agent**
An AI system that does work *independently* — the LLM itself decides what steps to take, not a fixed script.
> Example: You say "book me the cheapest flight to Delhi next week." An agent searches flights, compares prices, and books one — deciding the steps itself instead of you telling it each step.

**Agentic System**
A broader term — any system where the LLM *directs* its own process and tool usage while staying in control of how the task gets done (as opposed to just following a rigid pipeline).
> Think of it as the "family" that AI Agents belong to. Not every agentic system is a full autonomous agent — some just let the LLM make some decisions along the way.

**LLM + Tools + Loop = Agent**
The simplest mental model:
`LLM + Tools, running in a loop, until the goal is achieved = Agent`
The LLM keeps thinking → acting → observing results → thinking again, until it's done.

---

## 2. Common Workflow Patterns

These are different ways of *structuring* how LLM calls work together. Not all of them are "agents" — some are fixed pipelines.

| Pattern                 | Simple Meaning                                                                                                        | Example                                                                                                                  |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Prompt Chaining**     | A series of LLM calls, one after another, where output of one feeds the next.                                         | Step 1: LLM writes an outline → Step 2: LLM expands outline into an essay.                                               |
| **Routing**             | Send an input to a specialized sub-task/model, so each part handles only what it's good at (separation of concerns).  | A customer query gets routed to "billing bot" vs "tech support bot" depending on topic.                                  |
| **Parallelization**     | Break a task into pieces and run them **at the same time** instead of one after another.                              | Summarizing 5 different documents simultaneously instead of one by one.                                                  |
| **Orchestrator–Worker** | A "manager" LLM breaks a complex task into dynamic sub-tasks, sends them to "worker" LLMs, then combines the results. | Orchestrator says "research topic X" → splits into 3 worker tasks (history, stats, examples) → combines into one report. |
| **Evaluator–Optimizer** | One LLM produces output, a *second* LLM checks/critiques it, and the first improves it based on feedback.             | LLM writes code → second LLM reviews it for bugs → first LLM fixes and resubmits.                                        |

---

## 3. Risks & Anti-Patterns

**Risks of Agentic Frameworks**
Because the LLM decides its own path, things can become:
- **Unpredictable paths** — you can't fully predict what steps it'll take.
- **Unpredictable output** — results may vary run to run.
- **Unpredictable cost** — more steps/tool calls = more tokens = more money.

To manage this:
- **Monitoring** — track what the agent is doing, logs, traces.
- **Guardrails** — rules/limits that stop the agent from doing something unsafe, wrong, or too costly (e.g., max steps, approval before certain actions).

**The Agentic Trap**
Don't build an agent just because "AI agents" are trendy. Ask: *does this actually solve a real business problem or add value?* If a simple script or single LLM call does the job, don't over-engineer it into an "agent."

**Anthropomorphizing**
Treating the AI like it has human feelings, intentions, or consciousness (e.g., saying "the AI is happy to help" or "it wants to..."). It's a mental shortcut but can be misleading — the model doesn't actually *want* anything; it's predicting text. Good to notice when you're doing this, especially when reasoning about *why* an AI behaved a certain way.

---

## 4. Agentic Engineering — The Tool Landscape

A simple way to categorize the tools used to build agentic systems:

| Category          | What it means                                             | Example                 |
|-------------------|-----------------------------------------------------------|-------------------------|
| **AI Builders**   | No/low-code tools to visually build agent workflows       | n8n                     |
| **AI Products**   | Ready-made AI products/apps you use directly              | Claude Code             |
| **AI Runtimes**   | Infrastructure to *run* AI workloads/agents in production | AWS Lambda, AWS Bedrock |
| **AI Frameworks** | Code libraries/SDKs to build agents programmatically      | OpenAI Agents SDK       |

---

## 5. Tools & The Agent Loop

**Tools give the LLM abilities (Tool Calling)**
An LLM by itself can only generate text — it can't check the weather, search the web, or run code. **Tools** are functions you give the LLM access to, so it can *call* them when needed.
> Example: Give the LLM a `get_weather(city)` tool → now it can answer "what's the weather in Mumbai?" by actually calling that function instead of guessing.

**LLM + Tool**
The basic setup — the LLM has one (or more) tools it *can* call if needed, for a single task.

**LLM + Tool in a Loop**
The LLM keeps calling tools, checking results, and deciding the next step *repeatedly* until the goal is reached — this loop is what makes it "agentic" rather than a one-shot answer.

**The Agent Loop**
The repeating cycle an agent goes through:
1. **Think** — LLM decides what to do next based on the goal and context.
2. **Act** — it calls a tool (search, code, API, etc.).
3. **Observe** — it looks at the tool's result.
4. Repeat until the task is complete or it decides to give a final answer.

---

## 6. System Prompt, Memory & Context

**System Prompt**
The initial instructions given to the LLM *before* the conversation starts — defines its role, behavior, tone, and rules. It's like the "job description" the model reads before starting work.
> Example: *"You are a helpful customer support agent for a shoe company. Always be polite and never discuss competitors."*

**Conversation History**
The complete record of the conversation so far (all previous user messages + AI replies). This gets sent along with every new message.

**The Illusion of Memory**
LLMs don't actually "remember" you between messages — they have no built-in memory. What *looks* like memory is really the **entire conversation history being re-sent** to the model every single time. The model is reading the whole transcript fresh each turn, not recalling it.

**Key rule:** Every prompt sent to the LLM needs to include the **system prompt + conversation history + latest message** — this is *how* the illusion of "remembering" and continuity is created.

---

## 7. Context Engineering

**Context Engineering** = the practice of carefully deciding *what information* to feed the LLM at each step, since it only knows what's inside its context window. It's the evolution of "prompt engineering" — now it's about managing everything around the prompt too.

The main pieces that make up context:

- **System Prompt** — the model's role/instructions (see above).
- **Long-term Memory** — facts/preferences saved and reused across sessions (e.g., "user prefers concise answers").
- **User Prompt** — the actual current question/request from the user.
- **Available Tools** — what functions/tools the model is allowed to call right now.
- **Structured Output** — asking the model to reply in a specific format (e.g., JSON) so it's easy for other systems to use.
- **Retrieved Information (RAG)** — *Retrieval-Augmented Generation*: pulling relevant documents/data from an external source (like a database) and inserting them into the prompt so the LLM has accurate, up-to-date facts.
  > Example: Before answering "what's our refund policy?", the system retrieves the actual policy document and feeds it to the LLM so it doesn't guess.
- **State/History (Short-term memory)** — the ongoing conversation history within the current session (as discussed above).

---

## 8. Gradio

**Gradio** — in simple terms, it's a Python library that lets you quickly build a **simple web UI** (like a chat box, form, or demo page) around your AI model or function — without needing to know web development (HTML/CSS/JS).
> Example: You write a Python function that summarizes text. With a few lines of Gradio code, you get a shareable web page with a text box where anyone can paste text and see the summary — no frontend coding needed.

It's commonly used to quickly demo or test AI agents/models.

---

### Quick Recap Table

| Term                | One-liner                                                 |
|---------------------|-----------------------------------------------------------|
| AI Agent            | LLM independently completing a goal using tools in a loop |
| Agentic System      | LLM directs its own process while staying in control      |
| Prompt Chaining     | Sequential LLM calls, output → next input                 |
| Routing             | Send input to the right specialized handler               |
| Parallelization     | Run multiple sub-tasks at once                            |
| Orchestrator-Worker | Manager LLM splits & combines worker tasks                |
| Evaluator-Optimizer | One LLM checks another's output                           |
| Agentic Trap        | Don't use AI just to use AI — solve real problems         |
| Context Engineering | Curating everything fed into the LLM's context window     |
| Gradio              | Quick way to build a web UI for your AI function          |

