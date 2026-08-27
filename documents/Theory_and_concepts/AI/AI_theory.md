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
- Lang chain open source framework
  - Lang chain core -> Agent framework, create agent model tools etc
  - Lang graph -> Low level orchestration: Graph, state, persistence
  - Lang smith --> Observability evals and monitoring
  - LangSmith Deployment
- The abstraction layers
  - langchain-core (Layer1) building blocks
  - Lang graph (Layer2) Orchestration
  - Langchain (Layer3) Agent
  - Deepagents (Layer4) Agent harness
- LangChain Core
  - Models ChatOpenAi as one interface to every LLM
  - Messages
  - Tools
- LangGraph
  - low-level orchestration framework and runtime for stateful long-running agents. 
  - Dependency graph
  - Durable 
  - State is immutable (Python Object)
  - Nodes -> Do the work. It is a python function. Note take old state and return new state object.
  - Edges -> Chose what to do next (Conditional, non-conditional)
  - 5 Steps
    - Define the State class
    - Start the Graph Builder
    - Create a Node
    - Create the Edges
    - Compile the Graph 
  - Reducer --> take a new state and existing state and combine them
  - The Super-Step -> can be considered a single iteration over the graph nodes
  - checkpointer
  - memory saver, sqlilite saver as memory, checkpoints, time travel
- Lang chain agent
  - create_agent is a function
  - custom middleware
- Microsoft playwright mcp server
- Deep agents
  - create_deep_agent wraps create_agent in an opinionated harness
  - Built in planning todo list
  - Agent Skills: SKILL.md
    - Frontmatter name and description
    - Progressive disclosure
    - Skills vs Tools
      - Skills are the feature for end user who are using agents
      - Tools are for developer making agents
      - Skills are high level construct
      - Tools are better option where you are developing agent

Google ADK
- Code first toolkit
- Type a function it becomes a tool
- adk web
- flexible but heavier to learn

Agent to agent framework
- A Linux Foundation way for agents to find and cll each other

Strands and Pydantic AI
- product from AWS
- open source offering
- super lightweight framework
- any provider lightest loop
MS agent Framework and Agno
Mastra
