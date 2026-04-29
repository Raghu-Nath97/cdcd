# chatPG Application Environment Diagram (AED)

*   **Diagram Owner:** Lukasz Luszczynski
*   **Last Update:** 12/04/2025

---

## Global PGI (Personnel and Processes)

### P&G Admin, AI Engineer, AI Factory Operations

*   **Authentication Flow:**
    *   P&G Admin, AI Engineer, AI Factory Operations (Web browser) <=> PingFederate (Authentication) <=> Entra ID (Auth)

*   **Interactions:**
    *   P&G Admin, AI Engineer, AI Factory Operations (Web browser) <=> ChatPG (User & Task Administration [HTTPS, UI])

### P&G Model Developer, AI Engineer, Model Ops Engineer

*   **Authentication Flow:**
    *   P&G Model Developer, AI Engineer, Model Ops Engineer (Web browser) <=> PingFederate (Authentication) <=> Entra ID (Auth)
        *   *Note: This is an inferred path based on other diagrams, not explicitly drawn for this role's direct PingFederate connection.*

*   **Interactions:**
    *   P&G Model Developer, AI Engineer, Model Ops Engineer (IDE) <=> GitHub Enterprise Cloud - P&G Organization (Source Code [Git, HTTPS])

### P&G User

*   **Authentication Flow:**
    *   P&G User (Web browser / Microsoft Teams) <=> Entra ID (Auth)
        *   *Note: Authentication via PingFederate is implied through Entra ID based on other diagrams.*

*   **Interactions:**
    *   P&G User (Microsoft Teams) <=> ChatPG (Conversation Streaming [HTTPS, WebRTC], Send Prompt [HTTPS])
    *   P&G User (Web browser) <=> ChatPG (Conversation Streaming [HTTPS, WebRTC], Send Prompt [HTTPS])
    *   P&G User (Web browser) <=> Spyglass (Send Logs, Monitoring Insights traces [HTTPS])

---

## AI Factory Azure Workspaces

### Key Components:

*   **ChatPG** (Central component)
*   **GitHub Enterprise Cloud - P&G Organization**
*   **CICD (Continuous Integration Continuous Delivery) Framework**
*   **AI Factory - Shared Services**
    *   *Note: Provision Infrastructure via IaC (after provisioning, put the service principal credentials to the key vault)*
*   **AI Factory - components** (898489C85FBF12AA, 6B488C380770B57, 1B581B8D65450ECA)
*   **GenAI (Artificial Intelligence) Platform**
*   **Spyglass**

### Connections and Interactions within AI Factory Azure Workspaces:

*   **GitHub Enterprise Cloud - P&G Organization:**
    *   GitHub Enterprise Cloud - P&G Organization <=> CICD (Continuous Integration Continuous Delivery) Framework (Source Code Deployments [HTTPS])
    *   GitHub Enterprise Cloud - P&G Organization <=> AI Factory - Shared Services (Source Code [HTTPS])

*   **CICD (Continuous Integration Continuous Delivery) Framework:**
    *   CICD (Continuous Integration Continuous Delivery) Framework <=> AI Factory - components (Source Code Deployments [HTTPS])

*   **ChatPG:**
    *   ChatPG => GenAI (Artificial Intelligence) Platform (Generate embeddings, Register Prompts, Model Execution [HTTPS])
    *   ChatPG => AI Factory - Shared Services (Application Insights [REST, Parquet])

*   **Spyglass:**
    *   Spyglass <=> ChatPG (Conversation Streaming [HTTPS, WebRTC])
    *   Spyglass <=> GenAI (Artificial Intelligence) Platform (Authentication)
    *   Spyglass <=> PingFederate (Authentication)

*   **GenAI (Artificial Intelligence) Platform:**
    *   GenAI (Artificial Intelligence) Platform => AI Factory - components (Authentication)

*   **AI Factory - components:**
    *   AI Factory - components => AI Factory Instance Information [HTTPS]

---

## Cross-System Interactions

*   **PingFederate:**
    *   PingFederate <=> Entra ID (Authentication)
    *   PingFederate <=> ChatPG (Authentication)
    *   PingFederate <=> GenAI (Artificial Intelligence) Platform (Authentication)

*   **Entra ID:**
    *   Entra ID <=> Microsoft Teams (Auth)

*   **Microsoft Teams:**
    *   Microsoft Teams <=> ChatPG (Conversation Streaming [HTTPS, WebRTC], Send Prompt [HTTPS])

*   **AI Factory - Shared Services:**
    *   AI Factory - Shared Services <=> ChatPG (Provision Infrastructure via IaC)
