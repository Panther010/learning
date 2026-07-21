- AI agent: AI system that can do work for you independently where LLM control the workflow. LLM with tool in a loop to achieve a goal.
- Agentic System: System where LLMs direcy their own process and tool usage maintaning cntrol teir accomplish task
- Prompt chaining: Seriedd of LLM call
- Routing: Direct an input into a specialized sub-task ensuring sparation of concern
- Parallelization Breaking down tasks and running multiple task concurrently
- Orchestrator-worker: Complex tasks are broken down dynamically and combined
- Evaluator optimiser. LLM output iw validated by another LLM
- Risk of frameworks - unpredictable paths/output/costs
  - Monitor 
  - Guardrails
- Agentic trap - dont use AI just for the sake of using it should solve business problem and add value
- Anthropomorphizing ??
- Agentic engineer
  - AI builder : n8n
  - AI products : Claude code
  - AI runtimes : AWS Lambda, Bed rock
  - AI frameworks : OpenAi Agents SDK
- tool give llm abilities (Tool calling)
- The Agent loop
- What is system prompt
- Conversation history: Complete conversation so far
- The illusion of the memory:
- every prompt need to give system prompt and history with latest message for remember and use history
- gradio what is this in simple language 
- Make tool 
- LLM with tool
- LLM with tool in loop
- Context engineering
  - System prompt
  - Long term memory
  - USer prompt
  - available tool
  - structured output
  - retrieved information (RAG)
  - State history (Short term memory)
- What is gradio

Open AI agent SDK
- open source framework any one can use it. few abstraction as possible
- Asyncio python 
  - all the method and function async should start with async
  - result await and then processing
  - this help to do thing parallel
  - Asyncio lightwait alternative to threading or multiprocessing 
  - coroutines
  - await schedule it for execution within event loop? 
  - asyncio.gather
- Open AI agent SDK
  - lightweight flexible
- agent represent a particular LLM with system prompt and tools
- agents as tools and handoffs
- Guardrails
- Three steps
  - create an agent
  - use with trace() to track the agent
  - Runner.run()

- Orchestration
  - with code
  - LLMs - Tols
  - Handoffs

- Pydantic
- Guardrails
  - input
  - output
  - Tool guardrail
- Trip wire
- sandbox agent 
  - manifest
  - capabilities
  - sandbox: Sandbox agent


CrewAI
- CrewAI AMP
- CrewAI UI Studio
- CrewAI open-source framework
- CrewAI Crews: The intelligence
- CrewAi Flows : The backbone
- Core concepts
  - Agent: an autonomous unit, with an LLM a role a goal a backstory memory tools
  - Task: a specific assignment to be carried out with a description expected output agent
  - Crew: A team of Agents and Tasks. To way of running
    - Sequential
    - Hierarchical
- Five steps
  - Create the project
  - Fill the config yaml files
  - Complete crew.py module to create the Agents. Tasks and Crew
  - Update main.py
  - Crewai run
- Tools 
- Context
- Structured output
- custom tool
- Hierarchical process
- memory
- Traces 3 steps 



LangChain/ Lang Graph