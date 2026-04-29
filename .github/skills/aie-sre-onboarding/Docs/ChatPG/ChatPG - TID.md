# ChatPG Technical Infrastructure Diagram

*   **Diagram Owner:** Lukasz Luszczynski
*   **Update:** 12/04/2025

---

## Subscription: PG-NA-External-<Prod/NonProd>-08

**Resource Groups:** AZ-RG-AIP-MLWCHATPGPROD, AZ-RG-AIP-MLWCHATPGPROD-DR

### Services Container (Note: Service outside AIF Azure Workspace Blueprint)

*   **Components:**
    *   [Container Registry]
    *   [Key Vault]
    *   [BLOB Storage]
    *   [PostgreSQL flex server]
    *   [Cache for Redis]
    *   [Application Insights]

### PGI Network (10.99.0.0/16)

*   **Components:**
    *   [Machine Learning Workspace] mlwCHATPGPROD
    *   [Private Endpoint]
    *   [Private Endpoint]
    *   **privatelink subnet** (Note: Solution is based on AIF Azure ML Blueprint)
        *   [Private Endpoint]
        *   Service endpoints

*   **Connections within Subscription PG-NA-External-<Prod/NonProd>-08:**
    *   [PostgreSQL flex server] & [Cache for Redis] <=> [Machine Learning Workspace] mlwCHATPGPROD (HTTPS, L7)
    *   [Container Registry] <=> [Machine Learning Workspace] mlwCHATPGPROD (HTTPS, L7)
    *   [Key Vault] <=> [Machine Learning Workspace] mlwCHATPGPROD (HTTPS, L7)
    *   [BLOB Storage] <=> [Machine Learning Workspace] mlwCHATPGPROD (HTTPS, L7)
    *   [Application Insights] <=> [Machine Learning Workspace] mlwCHATPGPROD (HTTPS, L7)
    *   [Machine Learning Workspace] mlwCHATPGPROD <=> [Private Endpoint] (HTTPS, L7)
    *   [Private Endpoint] <=> [Private Endpoint] (HTTPS, L7)
    *   `privatelink subnet` <=> Service endpoints (HTTPS, L7)

---

## Subscription: PG-NA-External-Prod-04

**Resource Group:** AZ-RG-CICDFramework-DA-AKS-Agent-Prod-01

### AKS aks-cicd-da-eastus2-prod

*   **Components:**
    *   [Pod] GHA Runner
    *   Shared AKS Cluster for GHA Runner

### aks-cicd-da-eastus2-prod-vnet (10.99.0.0/16)

*   **Components:**
    *   Service endpoints
    *   [Private Endpoint]
    *   [Private Endpoint]
    *   **privateendpoints** (10.99.144.0/20)

*   **Connections within Subscription PG-NA-External-Prod-04:**
    *   Service endpoints <=> [Private Endpoint] (HTTPS, L7)
    *   [Private Endpoint] <=> [Private Endpoint] (HTTPS, L7)
    *   GHA Runner <=> Shared AKS Cluster for GHA Runner

---

## Subscription: AZ-RG-AIF-AKS-MT-EastUS2-[Prod/NonProd/Dev/QA], AZ-RG-AIF-AKS-MT-12-EastUS2-[Prod/NonProd], AZ-RG-AIF-AKS-DR-08-CentralUS-Prod

### Components within this Subscription:

*   Service endpoints
*   [Private Endpoint]
*   [Private Endpoint]
*   [Private Endpoint]
*   [Private Endpoint]
*   [Private Endpoint]
*   Private Link Service
*   [Load Balancer]
*   [Pod] ML & Application Containers (aks-aif-dr-prod-08-8b5b-vnet 10.99.0.0/16)
*   [AKS] (12/dev/)
*   Shared AKS Cluster for AI Factory - Shared Services based applications
*   AI Factory - components (898489C85FBF12AA, 30F53140632C417A, 1B581B8D65450ECA)
*   GitHub Enterprise Cloud - P&G Organization
*   CICD (Continuous Integration Continuous Delivery) Framework

### privateendpoints (10.99.144.0/20)

*   **Connections within this Subscription:**
    *   Service endpoints <=> [Private Endpoint] (HTTPS, L7)
    *   [Private Endpoint] <=> [Private Endpoint] (HTTPS, L7)
    *   Private Link Service <=> [Load Balancer] (HTTPS, L7)
    *   [Load Balancer] <=> [Pod] ML & Application Containers (HTTPS, L7)
    *   [Pod] ML & Application Containers <=> [AKS] (HTTPS, L7)
    *   [Pod] ML & Application Containers <=> Shared AKS Cluster for AI Factory - Shared Services based applications (HTTPS, L7)
    *   AI Factory - components <=> AI Factory Instance Information [HTTPS]
    *   GitHub Enterprise Cloud - P&G Organization <=> CICD (Continuous Integration Continuous Delivery) Framework (Source Code Deployments [HTTPS])
    *   CICD (Continuous Integration Continuous Delivery) Framework <=> GitHub Enterprise Cloud - P&G Organization (Source Code [Git, HTTPS])

---

## Global PGI (Personnel and Processes)

### P&G Admin, AI Engineer, AI Factory Operations

*   **Authentication Flow:**
    *   P&G Admin, AI Engineer, AI Factory Operations (Web browser) <=> PingFederate Prod Instance (Authentication) <=> Entra ID (Auth) <=> Microsoft Teams (Auth) <=> Web browser

*   **Interactions:**
    *   P&G Admin, AI Engineer, AI Factory Operations (Web browser) <=> PGI Network (User & Task Administration [HTTPS, UI])

### P&G User (MDM devices)

*   **Authentication Flow:**
    *   P&G User (Web browser / Microsoft Teams) <=> PingFederate Prod Instance (Authentication) <=> Entra ID (Auth)

*   **Interactions:**
    *   P&G User (Microsoft Teams) <=> Private Link Service (Forwarding user requests [JSON])
    *   P&G User (Microsoft Teams) <=> Spyglass (Conversation Streaming [HTTPS, WebRTC], TCP, UDP, L7)
    *   P&G User (Web browser) <=> Spyglass (Conversation Streaming [HTTPS, WebRTC], TCP, UDP, L7)
    *   P&G User (Web browser) <=> GenAI (Artificial Intelligence) Platform

### P&G Model Developer, AI Engineer, Model Ops Engineer

*   **Authentication Flow:**
    *   P&G Model Developer, AI Engineer, Model Ops Engineer (Web browser) <=> PingFederate Prod Instance (Authentication)

*   **Interactions:**
    *   P&G Model Developer, AI Engineer, Model Ops Engineer (IDE) <=> CICD (Continuous Integration Continuous Delivery) Framework (Source Code Deployments [HTTPS])

---

## Cross-Subscription and External Connections

*   **PG-NA-External-<Prod/NonProd>-08 <=> PG-NA-External-Prod-04:**
    *   [Machine Learning Workspace] mlwCHATPGPROD (Pipeline execution [HTTP, REST]) => GHA Runner (HTTPS, L7)
    *   GHA Runner <=> `Check the newest DEVX set-up`

*   **PG-NA-External-<Prod/NonProd>-08 <=> AZ-RG-AIF-AKS-MT-EastUS2-[Prod/NonProd/Dev/QA], etc.:**
    *   [Machine Learning Workspace] mlwCHATPGPROD (HTTPS, L7) <=> Private Link Service

*   **AZ-RG-AIF-AKS-MT-EastUS2-[Prod/NonProd/Dev/QA], etc. => External Components:**
    *   Private Link Service => Spyglass (Send Prompt [HTTPS], ports: 443, 3478, 19302, 5004, 16384-32768)
    *   [Pod] ML & Application Containers => Application Insights [REST, Parquet]
    *   Spyglass => GenAI (Artificial Intelligence) Platform (Send Logs, Monitoring Insights Traces [HTTPS])
    *   GenAI (Artificial Intelligence) Platform => AI Factory - components (Generate embeddings, Register Prompts, Model Execution [HTTPS])
    *   GenAI (Artificial Intelligence) Platform <=> AI Factory Instance Information [HTTPS]
    *   AI Factory - components <=> Shared AKS Cluster for AI Factory - Shared Services based applications (HTTPS, L7)
