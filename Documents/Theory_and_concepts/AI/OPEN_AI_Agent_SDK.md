# OpenAI Agents SDK — Revision Notes

## 1. What Is It?

The **OpenAI Agents SDK** is an **open-source Python framework** for building agentic applications. Its design philosophy: **as few abstractions as possible** — you can see and control the actual agent loop, instead of it being hidden behind magic.

- Lightweight & flexible.
- Built primarily around OpenAI's models, but is provider-flexible (works with other model providers too).
- Core idea: give it a *few clear building blocks* (Agent, Runner, Tools, Handoffs, Guardrails, Sessions) rather than a huge complex framework.

---

## 2. Quick Refresher: Asyncio in Python

The SDK is **async-first**, so you need to know this to use it comfortably.

- **`async def`** — any function that needs to *wait* for something (like an API call) should be declared with `async def`.
- **`await`** — used when *calling* an async function; it pauses that function until the result comes back, **without blocking the whole program**.
  ```python
  async def get_answer():
      result = await call_llm()   # pauses here, but other code can run meanwhile
      return result
  ```
- **Coroutines** — the special "pausable" functions created by `async def`. They don't run immediately when called; they need to be `await`ed (or scheduled) to actually execute.
- **Event Loop** — the manager that decides which paused coroutine to resume next. `await` basically means *"schedule me for execution and let other tasks run while I wait."*
- **`asyncio.gather(...)`** — run multiple coroutines **at the same time (concurrently)** and wait for all of them to finish.
  ```python
  results = await asyncio.gather(task1(), task2(), task3())
  ```
- **Why Asyncio (not threads/multiprocessing)?**
  Asyncio is a **lightweight** way to do concurrent work — great for tasks that spend most of their time *waiting* (like network/API calls), without the overhead of real threads or separate processes.

---

## 3. Core Concept: What Is an "Agent" Here?

In this SDK, an **Agent** = **an LLM + a system prompt (instructions) + a set of tools** it's allowed to use. That's it — a clearly defined package of "who it is, what it can do."

```python
from agents import Agent

billing_agent = Agent(
    name="Billing",
    instructions="Handle refunds and invoice questions only.",
)
```

**Agents as Tools & Handoffs** (two different ways multiple agents can work together):
- **Agent-as-a-tool** — one agent calls another agent *like a tool*, gets an answer back, and **stays in control** of the conversation itself (the orchestrator never lets go of the wheel).
- **Handoff** — one agent **fully transfers** the conversation to a more specialized agent, who now takes over completely. Implemented internally as a special `transfer_to_X` tool call, so it shows up in tracing.
  > Example: A "Triage" agent decides a question is about billing → **hands off** to the "Billing" agent, who now handles everything from here.

---

## 4. The Three Basic Steps to Run an Agent

1. **Create an agent** — define its name, instructions, and tools.
2. **Wrap with `trace()`** — to track/record everything that happens during the run (for debugging & observability).
3. **Call `Runner.run()`** — this actually executes the agent loop (calls the LLM, runs tools, handles handoffs) until it produces a final answer.

```python
from agents import Agent, Runner, trace

agent = Agent(name="Assistant", instructions="You are helpful.")

with trace("My workflow"):
    result = await Runner.run(agent, "What's the capital of France?")
    print(result.final_output)
```

The **Runner** is what actually drives the loop: it sends messages to the model, executes any tool calls, follows handoffs, and stops once the run is complete (or paused for approval).

---

## 5. Orchestration — How Agents Get Coordinated

There are two broad ways to control multi-step/multi-agent flows:

- **Orchestration with code** — you (the developer) write explicit logic to decide what happens next (if/else, calling different agents manually).
- **LLM-driven orchestration (LLMs + Tools + Handoffs)** — the **LLM itself decides** the next step: which tool to call, or whether to hand off to a different specialist agent. This is the more "agentic" style, since control lives inside the model's reasoning rather than your code.

---

## 6. Pydantic

**Pydantic** is a Python library used to define **structured data models** with type validation. The Agents SDK uses it heavily to define **structured outputs** — i.e., forcing the LLM's response into a specific, predictable shape (instead of free-form text).
```python
from pydantic import BaseModel

class WeatherReport(BaseModel):
    city: str
    temperature: float
```
This way, when the agent responds, you get a validated `WeatherReport` object instead of having to parse raw text yourself.

---

## 7. Guardrails

**Guardrails** = safety/validation checks that run *alongside* your agent to catch problems early — cheap, fast checks rather than relying only on the main LLM call.

- **Input Guardrails** — check the **user's input** *before* it reaches the main agent (e.g., blocking off-topic or unsafe requests). These run only on the *first* agent in a run.
- **Output Guardrails** — check the **agent's final output** *before* it's returned to the user (e.g., blocking leaked private data).
- **Tool Guardrails** — checks that run around **individual tool calls**, useful in multi-agent setups with managers/handoffs/delegated specialists, where you want to validate a specific tool call rather than just the whole agent's input/output.

**Tripwire** — the "alarm" mechanism inside a guardrail. If a guardrail's check fails, it **triggers the tripwire** (`tripwire_triggered = True`), which raises an exception and **halts the run** immediately — so you can catch it and respond appropriately (instead of letting a bad input/output continue through).
```python
from agents import GuardrailFunctionOutput

async def no_pii_guardrail(ctx, agent, output):
    contains_pii = check_for_pii(output)   # your own check
    return GuardrailFunctionOutput(
        output_info={"pii_found": contains_pii},
        tripwire_triggered=contains_pii,   # stops the run if True
    )
```

---

## 8. Sandbox Agents

A **Sandbox Agent** is a special type of Agent designed to work inside an **isolated execution environment** ("sandbox") — so it can safely read/write files, run shell commands, or execute code without touching your real system directly.

- **Manifest** — defines the **workspace** the sandbox agent gets when a fresh session starts: which files/folders are mounted in, what environment variables exist, what storage (like S3, Azure Blob, Google Cloud Storage) is connected. Think of it as *"here's the folder/desk this agent is allowed to work on."*
- **Capabilities** — plug-in *abilities* attached to a sandbox agent — they can shape the workspace before a run starts, add extra instructions, or expose additional tools (like shell access, file editing, or "skills") tied to that live sandbox session.
- **Sandbox (the environment itself)** — the actual isolated runtime where the agent's commands/code execute — can be a local sandbox, Docker, or hosted providers (e.g., E2B, Modal, Daytona, Cloudflare, Vercel).

> Example: A "Sandbox engineer" agent is given a manifest pointing to a mounted repo folder, plus a "Skills" capability — it can then read files in that repo, make edits via patches, and run verification commands, all safely contained inside the sandbox instead of your actual machine.

A key security principle: **credentials/secrets are injected by the sandbox provider at runtime — never written into the agent's prompt/instructions.**

---

### Quick Recap Table

| Term | One-liner |
|---|---|
| Agent | LLM + instructions + tools, bundled together |
| Runner.run() | Executes the agent loop until a final answer |
| trace() | Records/tracks what happens during a run |
| Handoff | One agent fully transfers control to a specialist |
| Agent-as-tool | One agent calls another but stays in control |
| Guardrail | Safety check on input, output, or a tool call |
| Tripwire | The trigger that halts a run when a guardrail fails |
| Pydantic | Defines structured, validated output shapes |
| Sandbox Agent | Agent that runs inside an isolated execution environment |
| Manifest | Defines the sandbox's workspace (files, env vars, storage) |
| Capabilities | Plug-ins that add abilities/tools to a sandbox agent |

