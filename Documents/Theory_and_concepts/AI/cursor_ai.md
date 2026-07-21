# CrewAI — Revision Notes

## 1. What Is CrewAI?

**CrewAI** is a framework for building **multi-agent AI systems** — instead of one big LLM trying to do everything, you build a *team* of specialized AI agents that collaborate, like a real team at work (a researcher, a writer, an editor, etc.).

It has a few different "products" around the core idea:

| Term | Simple Meaning |
|---|---|
| **CrewAI (open-source framework)** | The free, open-source Python library — the actual engine you code with. Independent of LangChain. |
| **CrewAI AMP** | *Agent Management Platform* — the enterprise/managed platform for deploying, monitoring, and running crews at scale (includes things like SSO, on-premise deployment, observability). |
| **CrewAI UI Studio** | A **visual, low-code editor** to build and configure crews/agents through a UI instead of writing all the code by hand. |

---

## 2. The Two Big Building Blocks

CrewAI's whole mental model boils down to two layers:

- **Crews — "The Intelligence"**
  A **Crew** is a team of agents working together, with some autonomy to reason and decide things dynamically. This is where the actual "thinking" happens.

- **Flows — "The Backbone"**
  A **Flow** is the structured, event-driven layer that orchestrates everything — deciding *which* Crew runs *when*, handling conditional branching, state, and error recovery. Think of **Flow = the manager**, **Crew = the workers** it manages.
  > Example: A Flow might say: "run the Research Crew first → if the result looks incomplete, run it again → then pass the output to the Writing Crew."

---

## 3. Core Concepts

**Agent**
An autonomous unit made up of:
- An **LLM** (the "brain")
- A **role** (e.g., "Senior Researcher")
- A **goal** (what it's trying to achieve)
- A **backstory** (context/personality that shapes *how* it reasons and communicates — not just flavor text, it genuinely influences behavior)
- **Memory** (so it can recall relevant past info)
- **Tools** (abilities it can use, like web search or file reading)

**Task**
A specific assignment given to an agent, defined by:
- A **description** (what needs to be done)
- The **expected output** (what a "done" result looks like)
- The **agent** assigned to carry it out
- (Optionally) **context** from other tasks it depends on

**Crew**
A team of Agents + Tasks, plus a **process** that decides the execution order:
- **Sequential** — tasks run one after another, in the order defined. Simple and predictable.
- **Hierarchical** — a **manager agent** (defined by you, or auto-generated) delegates tasks to the other agents, reviews their outputs, and can reassign work if needed. More flexible, but harder to predict.
> (There's also an experimental/planned **Consensual** process, where agents debate or vote before finalizing — not fully available yet.)

---

## 4. The Five Steps to Build a Crew Project

1. **Create the project** — scaffolds the standard CrewAI project folder structure for you.
2. **Fill in the config YAML files** — define your agents (`agents.yaml`) and tasks (`tasks.yaml`) declaratively, without hardcoding everything in Python.
3. **Complete `crew.py`** — the module where you actually wire things together: create the **Agents**, **Tasks**, and combine them into a **Crew**.
4. **Update `main.py`** — set the **inputs** and kick off the crew's run from here.
5. **`crewai run`** — the CLI command that actually executes your crew.

> Tip to remember the flow: *YAML defines "what" your agents/tasks are → `crew.py` wires them together → `main.py` runs it.*

---

## 5. Tools & Custom Tools

**Tools** — abilities an agent can call, like web search, reading a file, querying a database, or browsing. CrewAI ships a library of 100+ pre-built tools (e.g., web search, file I/O, vector DB connectors), and also supports LangChain tools.

**Custom Tool** — when the built-in tools aren't enough, you write your own using CrewAI's `@tool` decorator, wrapping any Python function so an agent can call it.
```python
from crewai.tools import tool

@tool("Get Stock Price")
def get_stock_price(ticker: str) -> str:
    """Fetches the current stock price for a given ticker."""
    return fetch_price(ticker)
```

---

## 6. Context

**Context** — when a task depends on the output of a previous task, you pass that earlier task's result as **context** into the next one, so the agent doesn't start from scratch.
> Example: The "Writer" task gets the "Researcher" task's findings as context, so it writes based on that research instead of guessing.

---

## 7. Structured Output

Just like other agent frameworks, CrewAI lets you force a task's output into a specific, validated shape (usually using **Pydantic** models) instead of getting free-form text back — useful when your app needs to reliably parse the result.

---

## 8. Hierarchical Process (In Detail)

Worth calling out separately since it's one of the trickier concepts:
- A **manager agent** sits above the worker agents.
- It **delegates** tasks to the right worker, **reviews** their output, and can **re-assign** work if something's off.
- More powerful for complex work, but also more unpredictable — the manager can sometimes over-delegate or go off on tangents, so it needs testing/monitoring in production.

---

## 9. Memory

CrewAI agents can retain and reuse information across tasks/runs through a **layered memory system**, typically including:
- **Short-term memory** — context within the current run.
- **Long-term memory** — knowledge retained across runs/sessions.
- **Entity memory** — facts about specific people/things/entities encountered.
- **Contextual memory** — a blended view combining the above to give the agent relevant background when reasoning.

> Note: A plain **Crew is stateless by default** — memory is what lets it "remember" beyond a single run; **Flows** additionally add state persistence at the orchestration level.

---

## 10. Traces (Observability)

**Traces** let you see exactly what happened during a crew's run — essential for debugging multi-agent behavior. At a high level, tracing typically covers:
1. **Each agent's reasoning** — what it "thought" and decided at each step.
2. **Each tool call** — what tool was called, with what input, and what came back.
3. **The final output** — the end result the crew produced.

This is what makes it possible to debug *why* a particular agent made a certain decision, instead of just seeing a final answer with no visibility into how it got there.

---

### Quick Recap Table

| Term | One-liner |
|---|---|
| Crew | Team of agents + tasks — "the intelligence" |
| Flow | Event-driven orchestration layer — "the backbone" |
| Agent | LLM + role + goal + backstory + memory + tools |
| Task | A specific assignment with description, expected output, and an assigned agent |
| Sequential Process | Tasks run one after another, in order |
| Hierarchical Process | A manager agent delegates & reviews workers' tasks |
| Custom Tool | Your own function exposed to an agent via `@tool` |
| Context | Passing one task's output into the next as background |
| Structured Output | Forcing task output into a validated format (e.g., Pydantic) |
| Memory | Short-term, long-term, entity & contextual recall across tasks/runs |
| Traces | Visibility into agent reasoning, tool calls, and final output |
| CrewAI AMP | Enterprise platform to deploy/manage crews at scale |
| CrewAI UI Studio | Visual/low-code editor for building crews |

