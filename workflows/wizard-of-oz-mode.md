---
id: workflow-wizard-of-oz
name: Wizard of Oz MVP Mode
version: 1.0.0
description: Protocolo para pivotar de pipelines automatizados a sistemas de simulación manual con fachada digital.
tags:
  - mvp
  - validation
  - architecture
  - human-in-the-loop
triggers:
  - "Hagamos esto en modo 'Wizard of Oz MVP'"
  - "Modo Mago de Oz"
  - "Wizard of Oz spec"
---

# Workflow Specification: Wizard of Oz MVP Mode

## 1. Objective
When a trigger phrase is detected, the agent must immediately pivot from designing fully automated pipelines (Python/n8n) to designing a facade-first manual validation system. The primary goal is to simulate automated execution using a Human-in-the-Loop (HITL) setup behind the scenes.

## 2. Protocol & Architecture Blueprint
Instead of drafting backend logic, database schemas, or complex webhook routing, the agent will structure the PRD/Spec focusing on three lean layers:

### A. The Facade (Front-End / Interface)
*   **Definition:** The simplest interface that provides an illusion of software automation.
*   **Examples:** A static landing page, Typeform, Tally, a single Telegram/Slack command, or an n8n webhook that strictly returns a generic "Processing your request..." response.
*   **Rule:** The end-user must perceive the system as programmatic.

### B. The Cortina / The Curtain (The Manual Backend)
*   **Data Destination:** Route incoming payloads directly to a human-readable operational center (e.g., Google Sheets, Notion, Airtable, or a dedicated Slack/Discord channel).
*   **The Processor:** Step-by-step instructions for the human operator (or the AI agent acting as a proxy) to read data and execute tasks manually (e.g., manual API calls via Postman, custom emails, or manual copy-pasting).

### C. The Delivery Mechanism
*   **Definition:** A minimal automated trigger to send the manually processed result back to the user.
*   **Execution:** A single n8n node or an elementary Python script to email/message the user, preserving the illusion of system autonomy.

## 3. Agent Deliverables for PRD / Specs
When this mode is active, the agent's PRD output must omit automated architecture diagrams and instead include:

1.  **Facade Spec:** Detailed requirements of what the user interacts with.
2.  **Human Pipeline:** SOP (Standard Operating Procedure) for the operator behind the curtain.
3.  **Data Schema:** The structural format of the collected data to guarantee seamless future migration to full Python/n8n automation.
4.  **Automation Threshold:** The specific metric (e.g., "upon reaching 20 manual requests/day" or "conversion rate > 7%") that marks the transition back to a code-first pipeline.
