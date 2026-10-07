Large Language Models (LLMs) are powerful, but they have hard limits. No amount of prompt refinement can overcome:
- Knowledge cutoffs
- Hallucination
- Missing private context

Retrieval Augmented Generation (RAG) 
- addresses these limits by injecting relevant external data into the model's context at query time.
- Instead of relying on frozen training data, a RAG system 
  - retrieves relevant documents
  - augments the prompt with them
  - lets the model generate a grounded response


Prompt engineering focuses on crafting the instruction text sent to a model. 
- It involves choosing the right words, 
- formatting, 
- examples.
- It's tactical and operates at the level of a single query.

Context engineering is a broader discipline. 
- It's the art and science of designing the entire information environment that a model receives
- Not just the question, but all the 
  - supporting data, 
  - instructions, 
  - history,
  - constraints that shape the model's decision at inference time.

- prompt engineering is writing a good question on an exam. 
- Context engineering is designing the entire 
  - exam room, 
  - including the reference materials on the desk, 
  - the instructions on the board, 
  - and the rules about what resources are allowed.


##  Why Context Engineering Matters for Agents
When building AI agents (systems that reason, plan, and take actions), context engineering becomes essential
Effective context engineering for agents involves:
- Providing the right information at the right time 
  - supplying relevant retrieved data, tool outputs, and prior decisions without overwhelming the model with noise
- Writing clear instructions that persist
  - system prompts that define behavior, constraints, and output format across multiple turns
- Managing state across turns
  - summarizing conversation history, pruning irrelevant context, and keeping token budgets under control
- Keeping the context trustworthy
  - grounding the model strictly in retrieved facts and preventing hallucination through explicit instructions
