# LangGraph Integration Roadmap for ScrubCast

## What is LangGraph?

LangGraph is a library from LangChain for building **stateful, multi-step AI workflows** as graphs. Think of it as upgrading from simple chain calls to complex agent architectures.

### Core Concepts

| Concept | Description |
|---|---|
| **StateGraph** | A directed graph where nodes are functions and edges define flow |
| **State** | Shared data (TypedDict) that flows through the graph |
| **Nodes** | Python functions that do work and return state updates |
| **Edges** | Connect nodes; can be conditional (branching logic) |
| **Checkpointer** | Persists state for conversation memory / human-in-the-loop |
| **Subgraphs** | Reusable graph components nested inside larger graphs |

### Key Benefits over Plain LangChain Chains

- **Complex control flow** — loops, branches, conditional routing
- **Persistent memory** — checkpointers store conversation state
- **Human-in-the-loop** — pause graph for user input
- **Parallel execution** — run independent nodes concurrently
- **Streaming** — stream node outputs in real-time

---

## LangGraph in ScrubCast

The project already uses LangChain for a basic RAG pipeline. Here's what we can build with LangGraph:

### 1. Upgrade RAG Pipeline to a Graph (Recommended First Step)

Current `chat.py` does retrieval + generation in a flat function. A LangGraph graph would let us:

- Add a **query analysis node** (rewrite/expand the user's question)
- Add a **retrieval node** (Qdrant similarity search)
- Add a **quality check node** (is the retrieved context relevant?)
- Conditionally **re-retrieve** or **generate answer**
- Stream token-by-token responses

### 2. Multi-Turn Conversational Agent

Right now each `/chat/ask` call is stateless. LangGraph + a checkpointer gives us:

- Conversation memory across requests
- Context carry-over ("What about the second point mentioned earlier?")
- Session management tied to video_id

### 3. Agentic Workflows

- **Tool-using agent** that can fetch video metadata, search snippets, and answer
- **Multi-video comparison** — agent that searches across multiple video transcripts
- **Summarization pipeline** — graph that chunks, summarizes in parallel, then synthesizes

---

## Proposed Integration Plan

### Phase 1: Basic RAG Graph

```
User Question → [Rewrite Query] → [Retrieve Context] → [Grade Relevance] → [Generate Answer]
                                                          ↓ (not relevant)
                                                     [Rewrite & Re-retrieve]
```

**Changes needed:**

- Add `langgraph` to dependencies
- Create `app/graph/state.py` — define the graph state (TypedDict)
- Create `app/graph/nodes.py` — individual node functions (retrieve, grade, generate)
- Create `app/graph/graph.py` — assemble the StateGraph
- Update `app/services/chat.py` — use the graph instead of raw chain calls
- Update API to support streaming responses

### Phase 2: Persistent Conversations

- Add `langgraph-checkpoint` + SQLite checkpointer
- Store conversation history per video session
- Enable multi-turn context

### Phase 3: Agent Capabilities

- Define tools (search snippets, get video info, summarize section)
- Build a ReAct-style agent graph
- Optional: human-in-the-loop for clarification
