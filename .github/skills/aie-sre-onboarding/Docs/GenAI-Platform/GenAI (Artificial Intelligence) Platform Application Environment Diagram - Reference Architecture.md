# (Generative AI UC Name) Application Environment Diagram (AED) — Reference Architecture

*   **Diagram Owner:** [[Owner Name]]
*   **Last Update:** [[Date]]

> Reference architecture template that any new GenAI use case (UC) clones and customises. Shows every persona, client surface, AI Factory workspace and external AI provider that a UC may connect to.

---

## P&G Operations & Maintenance Teams

*   **User/Device:** Web browser/Device
*   **Interactions:**
    *   Web browser/Device <=> Spyglass (Logging, Monitoring, Tracing)

---

## P&G Software Engineer

*   **User/Device:** Web browser/Device
*   **Components:**
    *   DAP Launchpad (CD0034B2530)
*   **Interactions:**
    *   Web browser/Device <=> DAP Launchpad (Exploratory Data Analysis)

---

## External API User, End-User

*   **User/Device:** Web browser/Device
*   **Authentication:**
    *   Web browser/Device <=> Ping Federate (Auth) <=> EntraID (Auth)
*   **Components:**
    *   P&G External Application ()
    *   EAI Azure API Management (001F0FE72CC30765)
*   **Interactions:**
    *   Web browser/Device <=> P&G External Application () (Auth)
    *   P&G External Application () <=> EAI Azure API Management (Send Response [HTTPS])
    *   EAI Azure API Management <=> AskPG (C100417B284) (API Management)

---

## P&G API User, End-User

*   **User/Device:** Web browser/Device
*   **Authentication:**
    *   Web browser/Device <=> Ping Federate (Auth) <=> EntraID (Auth)
*   **Components:**
    *   P&G Internal Application ()
*   **Interactions:**
    *   Web browser/Device <=> P&G Internal Application () (Auth)
    *   P&G Internal Application () <=> AskPG (C100417B284) (text)

---

## P&G Data Managers

*   **Components:**
    *   Data Platforms (CDL - Consumer Data Lake, CDG - Consumer Data Garage)
*   **Interactions:**
    *   P&G Data Managers <=> Data Platforms (Ingest Data [HTTPS])
    *   P&G Data Managers <=> AskPG (User Prompts [HTTPS])
    *   P&G Data Managers <=> Data Platforms (Data Management [HTTPS])

---

## AI Factory Azure Workspaces [D6B5D8900C57BC9]

*   **Core Components:**
    *   **AskPG (C100417B284)**
    *   **AI Factory - Shared Services**
    *   **Generative AI (Artificial Intelligence) Platform (C004260728)**
    *   **AI Factory - External Platform**
*   **External AI:**
    *   Generative AI
    *   Foundational Models
    *   Vertex AI
    *   Open AI

### Interactions within AI Factory Azure Workspaces

*   **AskPG (C100417B284):**
    *   AskPG <=> AI Factory - Shared Services (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])
    *   AskPG <=> Generative AI (Artificial Intelligence) Platform (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])
    *   AskPG <=> AI Factory - External Platform (Send Logs, Monts. [REST, HTTPS])
    *   AskPG <=> Data Platforms (Ingest Data, Data Management [REST, HTTPS])

*   **Generative AI (Artificial Intelligence) Platform (C004260728):**
    *   Generative AI Platform <=> AI Factory - components (Send Response [REST, HTTPS])
    *   Generative AI Platform <=> Generative AI (External AI)
    *   Generative AI Platform <=> Foundational Models
    *   Generative AI Platform <=> Vertex AI
    *   Generative AI Platform <=> Open AI

---

## Cross-System Interactions

*   **P&G External Application ():**
    *   P&G External Application () <=> AskPG (C100417B284) (Send Response [HTTPS])
    *   P&G External Application () <=> AI Factory - Shared Services (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])
    *   P&G External Application () <=> Generative AI (Artificial Intelligence) Platform (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])

*   **P&G Internal Application ():**
    *   P&G Internal Application () <=> AskPG (C100417B284) (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])
    *   P&G Internal Application () <=> AI Factory - Shared Services (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])
    *   P&G Internal Application () <=> Generative AI (Artificial Intelligence) Platform (Model Request, Generate embeddings, Query Embeddings [REST, HTTPS])

*   **Spyglass:**
    *   Spyglass <=> AI Factory - External Platform (Send Logs, Monts. [REST, HTTPS])

---

## Note (Warning)

*   This diagram provides a reference architecture for connecting a new use case to the GenAI platform.
*   To customise the diagram to meet the requirements of the new use case, you should:
    *   Remove all unnecessary blocks
    *   Add missing components of the new solution
    *   Add information about the processes and actual data flow for the blocks
    *   Fill in the cover table
    *   Register the application
