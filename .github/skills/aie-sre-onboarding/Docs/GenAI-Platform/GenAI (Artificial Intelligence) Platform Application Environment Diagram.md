# AI Factory - Generative AI Platform Application Environment Diagram (AED)

*   **Diagram Owner:** Artur Koladza, Lukasz Luszczynski
*   **Last Update:** 13/05/2025

> The actual GenAI Platform AED — concrete personas, the real AI Factory workspaces, and the live integration surfaces (API Management, AI Observability, AI Provisioner, AI Apps, Spyglass).

---

## External & User Groups

### External API User, End-User

*   **Client Application**
*   **Web browser**
*   *Note: Those requests go through Traffic Manager and APIM which is part of AIF External Shared Services*

### P&G Admin, AI Engineer, AI Factory Operations

*   **Web browser**
*   **Ping Federate** (Authentication)

### P&G API User, End-User

*   **GCP hosted Client application**
*   **Client application**
*   **Web browser**
*   **Ping Federate** (Authentication)

### P&G Model Developer, AI Engineer, Data Science, Model Ops Engineer

*   **IDE**

---

## AI Factory Azure Workspaces

### Key Components

*   **GitHub Enterprise Cloud**
*   **CICD (Continuous Integration Continuous Delivery) Framework**
*   **API Management**
*   **GenAI (Artificial Intelligence) Platform** (two instances shown — one in External, one in Shared Services)
*   **AI Factory - AI Observability (Azure)**
*   **AI Factory - AI Provisioner**
*   **AI Factory - AI Apps**
*   **Spyglass**

### Hierarchical Grouping

*   **AI Factory - Shared Services - External Platform**
    *   GenAI (Artificial Intelligence) Platform
*   **AI Factory - Shared Services**
    *   GenAI (Artificial Intelligence) Platform
    *   AI Factory - AI Observability (Azure)
    *   AI Factory - AI Provisioner
    *   AI Factory - AI Apps

### Interactions and Flows

*   **External API User, End-User:**
    *   Client application => API Management (Request [HTTPS])
    *   Web browser => API Management (Request [HTTPS])
*   **P&G Admin, AI Engineer, AI Factory Operations:**
    *   Web browser <=> Ping Federate (Authentication)
    *   Web browser => GenAI (Artificial Intelligence) Platform (User & Task Administration [HTTPS, UI])
*   **P&G API User, End-User:**
    *   GCP hosted Client application => API Management (Request [HTTPS])
    *   Client application => API Management (Request [HTTPS])
    *   Web browser <=> Ping Federate (Authentication)
    *   Web browser => API Management (Request [HTTPS])
*   **P&G Model Developer, AI Engineer, Data Science, Model Ops Engineer:**
    *   IDE => GitHub Enterprise Cloud (Source Code [Git, HTTPS])
*   **API Management:**
    *   API Management => GenAI (Artificial Intelligence) Platform (within External Platform)
    *   API Management => GenAI (Artificial Intelligence) Platform (within Shared Services)
*   **GitHub Enterprise Cloud:**
    *   GitHub Enterprise Cloud <=> CICD Framework (Source Code Deployments [HTTPS])
*   **CICD Framework:**
    *   CICD Framework => AI Factory - AI Provisioner (Provision generative applications via IaC)
*   **AI Factory - AI Provisioner:**
    *   AI Factory - AI Provisioner => AI Factory - AI Apps
*   **GenAI Platform (within Shared Services):**
    *   GenAI Platform => AI Factory - AI Observability (Application Insights [REST, Parquet])
*   **AI Factory - AI Observability:**
    *   AI Factory - AI Observability => AI Factory - AI Apps (Application Insights [REST, Parquet])
*   **AI Factory - AI Apps:**
    *   AI Factory - AI Apps => Spyglass (Send Logs, Monitoring Insights Traces [HTTPS])
