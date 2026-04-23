# AI Agents

## What is an AI Agent?

An AI agent is a modular abstraction that can possess a persona, perform actions in response to user input, and communicate with other agents. Agents use reasoning techniques for planning, leverage tools to interact, and have access to memory.

Agents can:

* **Perceive/Sense:** Use sensors or data inputs (voice, text, visual data) to perceive the environment or user actions
* **Reason/Decide:** Use AI techniques including NLP, ML, and deep learning to interpret inputs and decide on actions
* **Act:** Execute tasks or engage in interactions independently or with human collaboration

## PyGentic Agent Types

To ensure modularity, flexibility, and simplified development, PyGentic divides agents into two main types:

| Agent Type | Description |
|------------|-------------|
| **Templated Agents** | Predefined blueprints provided by the PyGentic library that can be customized and implemented by development teams |
| **Centralized Agents** | AI agents deployed within a centralized infrastructure, accessible through a unified interface provided by the PyGentic library |

## Templated Agents

The PyGentic library provides the following templated agents:

### Supervisor Agent
- **Role:** Intermediary that manages and monitors task execution
- **Goal:** Oversee execution process, track progress, report state of tasks
- **Operation:** Receives commands, initiates execution, monitors progress, handles errors, reports state, collects and returns results

### Reasoning Agent
- **Role:** Performs complex decision-making and problem-solving tasks
- **Goal:** Generate strategies based on inputs and reasoning
- **Operation:** Applies logical rules, AI models, and contextual information to analyze problems and generate solutions

### Planner Agent
- **Role:** Directs requests and data to appropriate agents
- **Goal:** Break down goals into actionable sub-tasks and create action sequences
- **Operation:** Receives tasks and determines the best agent to handle each one; ensures optimal distribution

### Coordinator Agent
- **Role:** Oversees orchestration of various agents
- **Goal:** Manage complex workflows involving multiple agents
- **Operation:** Monitors multi-step processes, ensures correct task order, and handles dependencies

### Role-Playing Agent
- **Role:** Simulates specific personas within a given context
- **Goal:** Simulate different roles in interactive scenarios
- **Operation:** Uses predefined scripts or AI models to assume various roles within a scenario

## Centralized Agents

The PyGentic library provides access to these centralized agents:

### Feedback Agent
- **Role:** Acts as evaluator and informer within the AI system
- **Goal:** Enable system learning from actions and experiences
- **Operation:** Monitors actions, evaluates performance, generates and communicates feedback

### Monitor Agent
- **Role:** Oversees system operations
- **Goal:** Observe, track, report on performance and health of other agents
- **Operation:** Collects and analyzes data from system components; identifies anomalies
- **Responsibility:** Technical observability of the entire solution

### Auditor Agent
- **Role:** Monitors system integrity, compliance, and performance
- **Goal:** Maintain system reliability, security, and adherence to policies
- **Operation:** Monitors operations, validates actions against rules, detects anomalies, generates reports
- **Responsibility:** Business observability of the entire solution