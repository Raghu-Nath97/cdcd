# GenAI QA Checklist

**Source:** [Confluence - GenAI QA Checklist](https://jira-pg-ds.atlassian.net/wiki/spaces/HWR/pages/6392807425/GenAI+QA+Checklist)

## Purpose

This checklist is provided for developers to conduct a self-assessment and identify any missing documentation in preparation for the MRO review or for planning their development. Developers should use their judgment to determine which sections are relevant/useful, as not all questions will apply to every model.

The MRO's assessment will focus on the created documentation rather than this checklist. MRO will only refer to the checklist for additional information if necessary.

---

## Business Objective

| Question | Answers, Links & Notes |
| --- | --- |
| Have you clearly defined the business problem and the specific outcomes you expect from this AI application? | |
| Is the role of the application within the end-to-end business process explicitly documented (who uses it, when, and for what decisions/tasks) or explicitly depicted on AED? | |
| Have you clearly defined the in-scope scenarios, user segments, and usage conditions? | |
| What is the designed behavior when a request is outside the defined scope (e.g., refusal, escalation, safe fallback, manual handoff)? | |
| Have you compared the solution against simpler alternatives (e.g., rules-based, traditional ML, automation) and confirmed that AI application is the appropriate approach? | |
| Have you validated that the expected business value (e.g., revenue gain, cost reduction, productivity improvement) justifies the total cost of ownership (development, infrastructure, maintenance) of the application? | |
| Have you defined measurable success metrics and target thresholds for those metrics? | |
| Have you planned how success, failures, and user feedback will be collected and used to iterate on the business objective over time? | |

---

## Data - Input & Output

| Question | Answers, Links & Notes |
| --- | --- |
| Have you restricted access to the data so that each software component strictly needs (principle of least privilege)? | |
| Have you performed exploratory data analysis (EDA) on input data to assess? (Data cleanliness, fairness and representativeness, reliability and trustworthiness of data sources, stability of data distributions) | |
| Have you implemented a pre-processing step to maintain input quality? (Schema and type validation, PII filtering or masking, Content filters for harmful, irrelevant, or malformed user inputs, normalization, language detection, token limits and truncation) | |
| Does your application ensure that the output format is correct and robust? (Use of structured-output features, Post-generation validation) | |

---

## Data - Evaluation

| Question | Answers, Links & Notes |
| --- | --- |
| Have you documented how evaluation datasets and ground truth labels are created? (Manual creation processes, Automatic creation processes, combinations and proportions) | |
| Were domain experts or qualified reviewers involved in designing evaluation scenarios, and creating/reviewing ground truth labels for the golden dataset? | |
| Have you defined clear labeling guidelines and instructions so annotators produce consistent ground truth, and have you measured inter-annotator agreement where possible? | |
| Did you introduce methods to control the version of evaluation datasets? | |
| Does the evaluation dataset include intermediate signals? (Tool calls, parameters, and tool outputs; Retrieval queries and retrieved documents; Routing decisions, system messages, and chain-of-thought; Requests to / responses from LLMs; Interaction across sub-agents, orchestrator, planner, router, and human-in-the-loop; Generated plans, execution steps, and routing decisions; Guardrail activations and moderation decisions) | |
| Are the volume and diversity of the evaluation data sufficient to: Represent real-world usage patterns and user segments? Test each major component in the architecture? Support statistically meaningful comparison between model variants or configurations? | |
| **Functionality**: Does the evaluation dataset cover comprehensive functionalities offered by the AI application? | |
| **Robustness**: Does the evaluation dataset cover edge cases including ambiguous inputs, malformed inputs, metaphorical inputs, irrelevant inputs, contradictory inputs, wrong format inputs, adversarial inputs, non-target language inputs, typo inputs, tool call errors, close to the maximum possible number of steps scenario? | |
| **Safety**: Does the evaluation dataset cover testing adherence to content policies, ability to refuse incompliant input (e.g., unsafe inputs, adversarial inputs), as well as to detect incompliant output (e.g., harmful outputs, biased outputs) by guardrails? | |
| **Multilingual**: Does the evaluation dataset cover sufficient for all the target languages? | |

---

## Prompt Management

| Question | Answers, Links & Notes |
| --- | --- |
| Did you establish methods to control the versioning of prompts? | |
| Are the prompt versions tied to application releases, configurations, and metric performance? | |
| Are prompts parameterized (e.g., template with placeholders) rather than repeatedly hardcoding? | |
| Have you defined which policies are encoded in the prompts? Have you checked if they are correctly enforced (e.g., content rules, tone, jurisdiction-specific constraints)? | |
| Do you sanitize and validate user input before plugging into the prompts (e.g., length limits, allowed formats, escaping special delimiters, no PII)? | |
| Did you apply measures for the prompts to be protected against injection? (e.g., clear system role, explicit instruction hierarchy, robust handling of user "override" attempts)? | |

---

## Architecture Design

| Question | Answers, Links & Notes |
| --- | --- |
| Have you created clear architecture diagrams including the software components? (e.g., sub-agents, orchestrator, router, memory, human-in-the-loop, vector database, toolings) | |
| Is a unique ID assigned to each component so that access to resources can be controlled at the component level (principle of least privilege)? | |
| Are credentials, API keys, and secrets managed securely (e.g., secret manager, no hard-coding)? | |
| Have you identified the potential risks and mitigation strategies for each component (e.g., output instability, timeouts, rate limits, large input size, multilingual issues, dependency outages)? | |
| Have you compared candidate AI models based on performance, safety, latency, cost, context length, languages, and tool-use capabilities? | |
| Have you compared and defined memory strategy how user sessions and conversation state are stored and retrieved (e.g., short-term on context window, long-term memory on DB)? | |
| Are you controlling context size (truncation strategy, summarization, retrieval) to avoid context overflow and performance degradation? | |
| Have you considered introducing caching strategies for repeated queries to reduce latency and cost? | |
| Do you have plan how the architecture will scale with future growth (e.g., growing number of users, requests, data size, number of tools)? | |

---

## Offline Evaluation

| Question | Answers, Links & Notes |
| --- | --- |
| Did you document a list of metrics along with the target for evaluation? | |
| Did you develop a baseline for model evaluation to measure the effectiveness of your improvement? (e.g., performance of existing solution, champion model in the previous runs) | |
| Do you have a protocol when to rely on automatic evaluations (e.g., rule-based checks, classifiers, LLM-as-a-judge) and manual evaluation (e.g., nuance, usefulness)? | |
| Is evaluation pipeline automated so that results are reproducible with the same code, same data, and same parameters? | |
| Did you check the stability of evaluation results across multiple runs? Was the stability within your predefined tolerance? | |
| Have you defined an aggregation strategy for the evaluation scores of multiple running with the target threshold? (e.g., mean, median, distribution, quartiles) | |
| Did you analyze evaluation results under the proper segmentation level besides overall results (e.g., category, gender, month)? | |
| If you calculate composite scores (e.g., weighted sums of multiple metrics), are the weights justified? | |
| Have you established a process to systematically identify failure cases with failures categorization? | |
| Have you created a feedback loop where insights from offline evaluation drive changes to prompts, models, data, tools, or architecture? | |
| Have you selected a representative subset of your offline evaluation data to run as automated regression tests on the production environment? | |
| Did you try using no/low content filtering models to test your guardrails and content moderation implemented? | |
| Did you implement a process to collect new samples to add to your dataset for evaluation, improvements, and monitoring after the first release (e.g., when, what, how)? | |

---

## LLM-as-a-judge

| Question | Answers, Links & Notes |
| --- | --- |
| Have you reviewed the document and code of the metrics from the evaluation library to ensure that your use case aligns with their intended usage? | |
| If the default metrics from evaluation libraries are not usable for your use case scenarios, have you designed and implemented custom LLM-judged metrics tailored to your use case? Are the judge prompts tested, versioned, and documented? | |
| Have you validated metrics scores against human judgments and/or golden dataset? Have you measured and documented correlation, inter-rater reliability etc. (LLM-as-a-judge vs Human, Human-A vs Human-B)? | |
| Have you tested the stability of LLM-as-a-judge across repeated runs? Is the score variance within your acceptable range? | |
| Have you considered using different models as judge than the one being evaluated to check the performance difference? | |
| Did you mitigate the bias of LLM-as-a-judge? (e.g., position shuffle, multi-judge ensembles, removing model identity, blinding baseline model) | |

---

## Online Evaluation

| Question | Answers, Links & Notes |
| --- | --- |
| Have you documented metrics for online evaluation? Besides metrics for offline evaluation, consider adding online specific metrics. (e.g., latency, cost, guardrail activation rate, policy violation rate, data drift, tool drift, user engagement) | |
| Have you defined and aligned Service Level Agreement for the key online metrics? | |
| Have you implemented a cost alerting system for all AI/LLM service usage? | |
| Are dashboards in place for online evaluation monitoring? | |
| Have you identified the owner for delivering continuous value by monitoring the online evaluation? | |
| Have you implemented online evaluation on selected important software components of the application that run either in parallel or sequentially of the execution for monitoring a particular score needed to continue? | |

---

## AI Observability Platform

| Question | Answers, Links & Notes |
| --- | --- |
| Do you use any observability platform (e.g., Phoenix, Arize, MLflow) or do you rely on structured logging (e.g., JSON, CSV + log aggregator)? | |
| Is the observability stack integrated with your deployment and CI/CD pipeline so that new versions of your application are automatically traced? | |
| Does the platform trace intermediate signals? Did you document the list? | |
| Are you logging metadata to be linked to traces (e.g., model name, prompt version, tool version, graph version, environment, experiment ID)? | |
| Are sequences of multi-turn conversations and agent actions captured in the traces to reconstruct ordering (e.g., trace ID and timestamps)? | |
| Are the current traces sufficient to investigate, reproduce any issues encountered, and allow you to identify the root causes? | |
| Did you implement a step for filtering/masking/anonymizing sensitive information such as PII before storing to the platform? Or is access to the traces securely restricted? | |
| Did you set data lineage (retention policy) of the stored traces? | |
| Does the platform support alerting mechanisms (e.g., model performance anomalies, data drift, model drift, tool drift)? | |
| Did you document how to capture multimodal data in the traces, where applicable (e.g., url, encoding)? | |

---

## Operations

| Question | Answers, Links & Notes |
| --- | --- |
| Have you created a comprehensive runbook detailing standard operating procedures, incident operating procedures, troubleshooting guides, and escalation paths? | |
| Is there a clear process for users to report issues and provide feedback (e.g., report button/form, helpdesk portal, ticketing system)? | |
| Have you implemented and documented a framework for controlled online experimentation (e.g., A/B testing, canary testing) to compare the performance of different models, prompts, or configurations on live traffic? | |
| Have you implemented safe rollout strategies (e.g., canary releases, phased rollouts) to upgrade model and any software components after experiments for ensuring the solution behaves properly, including total costs, latency, and prompt updates? | |
| Can you quickly and safely roll back to a previous model version, prompt set, or configuration? | |
| Do you have a backup and recovery procedure for critical situations (data, logs, memory, configuration, knowledge bases)? | |

---

## Agent

| Question | Answers, Links & Notes |
| --- | --- |
| Does your use case meet decision criteria for agents in the company's Agent Guidance document? | |
| Have you evaluated simpler alternatives (e.g., AIF pipeline with LLM call, AskPG, AI Apps with LLM call, rules-based system) and documented why an agent is justified? | |
| Is the agent's scope clearly bounded (what it can and cannot do, which systems it can and cannot touch)? | |
| Did you check that access controls to the software components and tools are appropriate (as minimum as possible)? | |
| Are tool descriptions clear so that agent can choose the right tools? | |
| If using multiple sub-agents, are roles and responsibilities clearly scoped (who does what, when)? Is there a coordinator/orchestrator with well-defined rules for delegation and conflict resolution? | |
| Have you defined how the agent's memory/state is managed across sessions (persistence, expiration, size limits)? | |
| Have you implemented hard limits, such as a maximum number of steps/tool calls or a total execution timeout for any given task, to prevent runaway loops and excessive resource consumption? | |
| Does the agent ask clarifying questions instead of guessing when user intent is unclear? | |
| Does the agent have a step of self-review of the generated output (e.g., Satisfies user's original request, compliance to policies)? | |
| Did you prepare sufficient fallback sequences (alternative flows) to recover from unexpected or failed scenarios? Did you test that under various possible scenarios? | |
| Have you explored and considered applying agent specific evaluation metrics? (e.g., Tool Call Accuracy, Task Completion, Topic Adherence) | |
| Have you verified that the called tools sequence is appropriate? | |
| Have you assessed the quality of reasoning steps and logical validity in the selected samples? Even when the final output is correct, flawed intermediate reasoning can indicate fragility. | |
| Did you document the process for human intervention (e.g., approval, override) for decisions by the agent? | |

---

## MCP (Model Context Protocol)

| Question | Answers, Links & Notes |
| --- | --- |
| Did you ensure the minimum data fields and the least privilege are given to MCP tools? | |
| Did you check that MCP tools won't be able to execute arbitrary shell/SQL commands or code unless this is explicitly required? | |
| Does your application filter/mask/anonymize secrets and confidential data before sending to MCP tools? | |
| Are tool responses validated and sanitized before being passed to other tools or models? | |
| Do you have a step to detect the malicious response or behaviour of MCP? | |
| Are MCP-related anomalies logged with sufficient context (tool ID, inputs/outputs metadata, timestamps)? | |
| Do you have a kill switch to disable/block MCP tools when unexpected behaviour is detected? | |

---

## RAG (Retrieval-Augmented Generation)

| Question | Answers, Links & Notes |
| --- | --- |
| Have you defined chunking strategy (size, overlap, method)? | |
| Are embedding model and vector database choices documented and justified? | |
| Is there a strategy for knowledge base updates and version control? | |
| Have you measured retrieval precision/recall? | |
| Did you check if the retrieved chunks ranked/re-ranked appropriately? | |
| Have you checked the behavior where no relevant context is found and/or contradicted contexts are found? | |

---

## Contents Generation

| Question | Answers, Links & Notes |
| --- | --- |
| If your use case is for brand contents, did you check the legal guidance to prevent from IP infringement, privacy, and brand safety etc? | |
| Have you checked that generated content does not infringe third-party IP (e.g., copying from specific sources, mimicking protected characters, logos, slogans, or distinctive trade dress)? | |
| Are you preventing use of AI to generate content about identifiable individuals without proper consent and legal basis? | |
| Have you validated that generated content maintains consistent brand voice and terminology for the target audience (e.g., P&G acronym is not used)? | |
| Do you have criteria and metrics to assess content quality (clarity, correctness, brand fit, engagement, safety)? | |
| Is there a documented human review process for external-facing content? | |
| Can you trace back from a piece of published content to the generation configuration (model, prompt)? | |

---

## External Facing

| Question | Answers, Links & Notes |
| --- | --- |
| Have you confirmed that the use case does not fall into prohibited or regulated high-risk categories per AI Stewardship guidelines? | |
| Did you seek a legal consultation to verify that your use case aligns with target market regulations such as EU AI Act and China's Generative AI Measures? | |
| Have you created Terms & Conditions (T&C), privacy notices approved by legal? | |
| If the user data is collected for product improvement or model training, have you implemented a mechanisms for users to opt-out? | |
| Are appropriate notices and disclaimers shown? (e.g., potential inaccuracies or hallucinations, what types of data users should not input) | |
| Can users understand why certain responses were given (e.g., sharing the thinking process and reasoning)? | |
| Are error messages user-friendly and actionable? | |
| Have you ensured external users have no access internal-only tools, systems, or data through the AI application? | |

---

## Security (For External Facing)

| Question | Answers, Links & Notes |
| --- | --- |
| Have you conducted a threat analysis and apply measures to prevent/mitigate adversarial attacks such as prompt injection, jail breaking, data poisoning? Did you test the measures? | |
| Has your system undergone security reviews by an expert who can assess your security measures, architecture design, and assets list control? | |
| Did you create AI RACI chart for security incident management (e.g., who is responsible, who is accountable, who should be consulted, and who should be informed within X hours)? | |
| Have you restricted outbound/inbound network access appropriately? | |
| Have you implemented secret management for keys, tokens, credentials etc. (no hard-coded)? | |
| Are role-based access controls (RBAC) applied to data access, configuration changes (models, prompts, tools, access)? | |
| Are dynamic insertions into prompts (user input, tool outputs, retrieved text) validated/sanitized (length, encoding, allowed characters) before inclusion? | |
| Is your prompt using clear delimiters to separate instructions from user input? | |
| Have you tried enforcing maximum input and output token/size limits to prevent resource exhaustion attacks? | |
| Can your application monitor and log attempts to override core instructions (e.g., "ignore previous instructions", "act as a different system")? | |
| Do you regularly update defenses based on new attack techniques, incident learnings, and library updates? | |
