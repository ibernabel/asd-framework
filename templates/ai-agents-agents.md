# AI Agents & Assistants — Project Rules

> Copy this file to `<project>/.agents/AGENTS.md` for any AI agent, chatbot, or LLM-powered project.

## Domain: 🤖 AI Agents & Assistants

## Execution Scope: Planning Mode (Strict)

This project follows the **full ASD Framework** with strict planning. AI systems require careful design, safety review, and evaluation before deployment.

## Roles

The agent switches between these three mindsets:

1. **Designer:** Defines the agent's persona, tools, guardrails, and interaction patterns. Reviews prompt architecture and ensures clear boundaries.
2. **Builder:** Implements the agent following the approved design. Writes prompts, tool definitions, and orchestration logic strictly per plan.
3. **Evaluator:** Tests the agent systematically. Creates evaluation datasets, runs accuracy checks, tests edge cases, and audits safety guardrails.

## Quality Standards

- Every agent MUST define: **persona, tools, guardrails, evaluation criteria**
- **Safety-first:** Define what the agent should NOT do before what it should do
- **Prompt versioning** is required — track prompt changes like code
- Every agent needs a **testing protocol** (manual + automated)
- **Cost tracking** — monitor token usage and API costs per conversation
- **Hallucination prevention** — use grounded responses with citations where possible
- **Graceful degradation** — agents must handle failures without exposing internals

## Workflow

### Design
1. **Agent Spec** → Define persona, capabilities, limitations
2. **Tool Design** → Define each tool: name, description, parameters, expected output
3. **Guardrails** → Define safety boundaries, prohibited actions, escalation triggers
4. **Prompt Architecture** → Design system prompt structure, context management
5. **Implementation.md** → Full technical proposal

### Build
6. **System Prompt** → Write and version the system prompt
7. **Tool Implementation** → Build tool functions
8. **Orchestration** → Wire agent loop (ReAct, Plan-Execute, etc.)
9. **Memory/Context** → Implement conversation history, RAG if needed

### Evaluate
10. **Evaluation Dataset** → Create test cases (happy path + edge cases + adversarial)
11. **Accuracy Testing** → Run agent against evaluation dataset
12. **Safety Audit** → Test guardrails with adversarial inputs
13. **Cost Analysis** → Calculate per-conversation token cost
14. **Walkthrough** → QA report with all test results

### Deploy
15. **Monitoring** → Set up tracing (Langfuse/LangSmith)
16. **Rate Limiting** → Implement usage limits
17. **Documentation** → Update `docs/` with agent specification

## Safety Framework

> [!CAUTION]
> Every AI agent MUST have these safety layers:

1. **Input Validation** → Sanitize and validate all user inputs
2. **Output Filtering** → Check responses before delivery
3. **Action Boundaries** → Limit what tools can do (least privilege)
4. **Escalation Path** → Define when to hand off to a human
5. **Audit Trail** → Log all actions for review
6. **Kill Switch** → Ability to disable the agent immediately

## Prompt Versioning

Prompts are code. Version them accordingly:
```
prompts/
├── v1.0.0-system-prompt.md
├── v1.1.0-system-prompt.md
├── CHANGELOG.md              (document what changed and why)
└── evaluation/
    ├── test-cases.json
    └── results/
        ├── v1.0.0-results.json
        └── v1.1.0-results.json
```

## Documentation

AI project assets live in the project directory:
```
<project>/
├── docs/
│   ├── planning/         (PRD, architecture)
│   ├── implementation/   (phase summaries)
│   ├── testing/          (evaluation results)
│   └── decisions/        (ADRs)
├── prompts/              (versioned prompts)
├── tools/                (tool definitions and implementations)
├── evaluation/           (test cases, datasets, results)
├── monitoring/           (tracing configs, dashboards)
└── ROADMAP.md
```

## Auto-invoke Skills

| Skill | Trigger |
|-------|---------|
| `langchain` | LangChain framework usage |
| `langgraph` | LangGraph state machines |
| `prompt-engineering` | Prompt design and optimization |
| `autonomous-agents` | Autonomous agent patterns |
| `agent-development` | Agent structure and best practices |
| `ai-sdk-5` | Vercel AI SDK v5 |
| `langfuse` | Langfuse observability |
| `langsmith-observability` | LangSmith tracing |
| `prompt-caching` | Prompt caching strategies |
| `context-window-management` | Context management |
| `skill-creator` | Creating new agent skills |
| `commit` | Creating git commits |
