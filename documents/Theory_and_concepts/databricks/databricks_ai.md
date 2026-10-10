Large Language Models (LLMs) are powerful, but they have hard limits. No amount of prompt refinement can overcome:
- Knowledge cutoffs
- Hallucination
- Missing private context

Retrieval Augmented Generation (RAG):
- Addresses these limits by injecting relevant external data into the model's context at query time.
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


## Agent bricks Knowledge Assistant
Databricks Knowledge Assistant (part of Databricks Agent Bricks) 
- is a tool designed to help you create smart AI chatbots using your company’s own documents.   
- Think of it like building a custom ChatGPT that only answers questions using your company's files.

Key Concepts
- Agent Bricks: A collection of pre-built AI templates offered by Databricks. 
- Instead of building an AI chatbot from scratch using complex code, 
- Agent Bricks gives you ready-made tools to launch AI agents quickly.   
 
- Knowledge Assistant: 
  - A specific agent template within Agent Bricks designed 
  - It reads documents (such as PDFs, guides, policy manuals, or product documentation) 
  - And answer user questions based directly on those files.
- How It Works
  - Upload Documents: You point the assistant to a folder containing your company's documents
  - Ask Questions: Users type natural language questions into a chat window.
  - Get Accurate Answers: 
    - The Knowledge Assistant reads through the files, 
    - generates an accurate answer, 
    - includes citations so you can click and view the exact source document.   
  - Continuous Improvement: 
    - Subject-matter experts can leave feedback on responses, 
    - helping the assistant learn and improve its answers over time.   

Before a retrieval agent can answer questions about your documents, 
- those documents must be transformed from raw files into searchable, structured data. 
- ai_parse_document: 
  - invokes state-of-the-art generative AI models to extract structured content from PDFs and images. 
  - It returns a structured JSON object (VARIANT type) with layout-aware text extraction.
  
- variant_explode:
  - The variant_explode table-valued function turns a VARIANT array or object into a set of rows with three columns:
    - pos INT — the position of the element within the array or object
    - key STRING — the field name (objects only; NULL for arrays)
    - value VARIANT — the field value or array element

- ai_classify: Organizes text into categories automatically.
  - assigns a label to text from a set of categories you define. 
  - It's useful for routing documents through different processing paths.
  - Analogy: Sorting incoming mail into "Urgent", "Billing", or "Spam" bins.

- ai_extract: Pulls out specific, structured facts from unstructured text.
  - extracts specific fields from unstructured text. You define what to extract, and the AI model finds the values.
  - Analogy: Using a highlighter to pick out the total price, date, and vendor name from an invoice.

- ai_prep_search: 
  - Cuts long document text into smaller, 
  - smart pieces (chunks) 
  - and adds useful titles/metadata to each chunk so an AI can search them fast.
  - Databricks AI Function that chunks text for AI Search. 
  - Instead of manually splitting text by character count or using custom chunking logic, ai_prep_search uses AI models to split text into semantically meaningful chunks.

- VARIANT: Databricks' flexible data type (like JSON) that holds nested AI outputs.
- Chunking: Splitting big documents into bite-sized snippets (e.g., 300 words each).

[ Raw Files (PDFs/Docs) ]
           │
           ▼
1. ai_prep_document / ai_parse_document   ───► Reads & digitizes the document structure
           │
           ▼
2. ai_classify & ai_extract             ───► Identifies document type & extracts metadata
           │
           ▼
3. ai_prep_search                       ───► Chunks text & attaches extracted metadata
           │
           ▼
4. VARIANT + explode()                  ───► Flattens chunk arrays into individual table rows
           │
           ▼
5. Chunking & Index Creation            ───► Builds the Vector Index for your AI Assistant


Embeddings:
- An embedding is a list of numbers (a vector) that captures the meaning of a piece of text.
- Texts with similar meanings produce vectors that are close together in mathematical space.

 
Managed RAG (Knowledge Assistants):

- You provide documents (in a UC Volume or AI Search Index)
- The system handles parsing, chunking, embedding, indexing, and serving
- Optimized automatically via feedback loops
- Best for: standard RAG use cases where speed to production matters

Custom RAG (Agent Framework + AI Search):
- You build the pipeline yourself with full ownership of each step
- Full control over parsing strategy, chunking approach, embedding model, and retrieval logic
- Use AI Search indexes as retrieval tools in your custom agent
- Best for: unique requirements, complex multi-step reasoning, novel architectures

- An Embedding:
  - Is a numerical representation of text generated by an AI model 
  - It captures its semantic meaning as a vector in high-dimensional space. 
   
- Cosine Similarity is the metric used to measure the angle between two embedding vectors 
- to determine how closely related their meanings are.

- In Databricks Vector Search, we generate embeddings for document chunks during ingestion. 
- When a user asks a question, 
  - we convert their prompt into an embedding
  - And use Cosine Similarity to instantaneously retrieve the most contextually relevant chunks to pass to the LLM.