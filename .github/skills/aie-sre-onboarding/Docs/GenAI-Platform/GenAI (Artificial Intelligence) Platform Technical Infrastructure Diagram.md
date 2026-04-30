# AI Factory - Generative AI Platform Technical Infrastructure Diagram (TID)

*   **Diagram Owner:** Artur Koladza, Lukasz Luszczynski
*   **Last Update:** [[Date]]

> The actual GenAI Platform TID — Global Internet, PGI, GCP and the full Azure subscription / resource-group layout for both the **External Platform** and **Internal Platform** instances, plus ChatPG, CICD, Spyglass.

---

## Global Internet

*   **User:** P&G User
*   **Devices:** WebBrowser/MSTF Teams App
*   **Interactions:**
    *   WebBrowser/MSTF Teams App => API Gateway (Request [HTTPS])

---

## P&G User (Global PGI)

*   **Devices:** WebBrowser/MSTF Teams App
*   **Authentication:**
    *   WebBrowser/MSTF Teams App <=> Ping Federate (port 443, https)
    *   WebBrowser/MSTF Teams App <=> EntraID (port 443, https)

---

## PGI (P&G Admin, AI Engineer, AI Factory Operations)

*   **User:** P&G Admin, AI Engineer, AI Factory Operations
*   **Devices:** Web Browser
*   **Authentication:**
    *   Web Browser <=> Ping Federate (port 443, https)
    *   Web Browser <=> EntraID (port 443, https)
*   **Interactions:**
    *   Web Browser <=> AI Factory - Generative AI (AI) Platform - Internal Platform (User & Task Admin [HTTPS, UI])

---

## PGI (P&G User)

*   **User:** P&G User
*   **Authentication:**
    *   Ping Federate (Auth) <=> EntraID (Auth)
        *   Ping Federate sends SAML assertion to EntraID and receives `access_token`, `refresh_token` from EntraID
*   **Interactions:**
    *   Ping Federate <=> API Management (Request [HTTPS])

---

## GCP (Google Cloud Platform)

### `<<ABSTRACT PROJECT>>`

*   **Components (illustrative only — block is purely abstract to demonstrate the possibility of deploying into GCP):**
    *   Cloud Build
    *   Cloud Storage
    *   Cloud KMS
    *   Cloud Scheduler
    *   Secret Manager
    *   Cloud Function
    *   Cloud Run
    *   Cloud SQL
*   **Interactions:**
    *   GCP hosted Client application (P&G User) <=> API Management (Request [HTTPS])
    *   GCP hosted Client application <=> API Gateway (Request [HTTPS])

---

## Azure Environment (Shared Services & Subscriptions)

### API Gateway

*   **Connections:**
    *   API Gateway => API Management (Request [HTTPS])

### API Management

*   **Authentication:**
    *   API Management <=> Ping Federate (Auth) (port 443, https)
*   **Connections:**
    *   API Management => AI Factory - Generative AI (AI) Platform - External Platform (Request [HTTPS])
    *   API Management => AI Factory - Generative AI (AI) Platform - Internal Platform (Request [HTTPS])

### AI Factory - Generative AI (AI) Platform - External Platform

*   **Components:**
    *   AI Factory - General Service (genai platform service)
        *   Audit Endpoints
    *   Service endpoints
    *   Private Endpoint
    *   Load Balancer
    *   AKS (Azure Kubernetes Service)
    *   Container Registry
    *   Azure OpenAI
    *   Azure ML (Azure OpenAI)
    *   Azure ML (Cortex for Redis)
*   **Subscriptions/Resource Groups:**
    *   `dev (IUC. GCP. DEV. VPC. Name)`
    *   `uat (IUC. GCP. UAT. VPC. Name)`
    *   `prod (IUC. GCP. PROD. VPC. Name)`
    *   `prod (AZ-RG-AIF-AKS-MT-EastUS2-Prod)`
    *   `prod (AZ-RG-AIF-AKS-DR-08-CentralUS-Prod)`
    *   `prod (AZ-RG-AIF-MLWCHATPGPROD)`
*   **Interactions:**
    *   AI Factory - General Service <=> Load Balancer (HTTPS, L7)
    *   Load Balancer <=> AKS (HTTPS, L7)
    *   AKS <=> Azure OpenAI (HTTPS, L7)
    *   AKS <=> Azure ML (Azure OpenAI) (HTTPS, L7)
    *   AKS <=> Azure ML (Cortex for Redis) (HTTPS, L7)
    *   AKS <=> Container Registry (HTTPS, L7)

### AI Factory - Generative AI (AI) Platform - Internal Platform

*   **Components:**
    *   AI Factory - General Service (genai platform service)
        *   Audit Endpoints
    *   Service endpoints
    *   Private Endpoint
    *   Load Balancer
    *   AKS (Azure Kubernetes Service)
    *   Container Registry
    *   Azure OpenAI
    *   Azure ML (Azure OpenAI)
    *   Azure ML (Cortex for Redis)
    *   Microsoft Teams
*   **Subscriptions/Resource Groups:**
    *   `prod (AZ-RG-AIF-AKS-MT-EastUS2-Prod)`
    *   `prod (AZ-RG-AIF-AKS-DR-08-CentralUS-Prod)`
    *   `prod (AZ-RG-AIF-MLWCHATPGPROD)`
*   **Interactions:**
    *   AI Factory - General Service <=> Load Balancer (HTTPS, L7)
    *   Load Balancer <=> AKS (HTTPS, L7)
    *   AKS <=> Azure OpenAI (HTTPS, L7)
    *   AKS <=> Azure ML (Azure OpenAI) (HTTPS, L7)
    *   AKS <=> Azure ML (Cortex for Redis) (HTTPS, L7)
    *   AKS <=> Container Registry (HTTPS, L7)
    *   AKS <=> Microsoft Teams (HTTPS, L7)

### Subscription: PG-NA-External-Prod-05, PG-NA-External-Prod-10, PG-NA-External-Prod-12

*   **Components:**
    *   ML Workspace
    *   Azure ML
    *   `Azure CoreML (MLFlow & Torch)`
    *   Azure SQL DB
    *   Private Endpoint
    *   Private Endpoint
    *   Load Balancer
*   **Interactions:**
    *   ML Workspace <=> Azure ML (HTTPS, L7)
    *   ML Workspace <=> `Azure CoreML (MLFlow & Torch)` (HTTPS, L7)
    *   ML Workspace <=> Azure SQL DB (HTTPS, L7)

### Subscription: AZ-RG-AIF-MLWCHATPGPROD, AZ-RG-AIF-MLWCHATPGPROD-DR

*   **Components:**
    *   ML Workspace
    *   Azure ML
    *   Azure SQL DB
    *   `Azure CoreML (MLFlow & Torch)`
    *   Private Endpoint
    *   Load Balancer
*   **Interactions:**
    *   ML Workspace <=> Azure ML (HTTPS, L7)
    *   ML Workspace <=> Azure SQL DB (HTTPS, L7)
    *   ML Workspace <=> `Azure CoreML (MLFlow & Torch)` (HTTPS, L7)

### ChatPG Backend

*   **Components:**
    *   ChatPG Backend
*   **Interactions:**
    *   ChatPG Backend <=> AI Factory - Generative AI (AI) Platform - Internal Platform (Prompt, Results [JSON], HTTPS, L7)

### ChatPG Frontend

*   **Components:**
    *   ChatPG Frontend
*   **Interactions:**
    *   ChatPG Frontend <=> ChatPG Backend (Request, Results [JSON], HTTPS, L7)

### AKS (AZ-RG-AIF-AKS-MT-EastUS2-[Prod/NonProd/Dev/QA], etc.)

*   **Components:**
    *   AKS (Azure Kubernetes Service)
*   **Interactions:**
    *   AKS <=> ChatPG Frontend (HTTPS, L7)

### Azure (Hub/Spoke)

*   **Connections:**
    *   Azure (Hub/Spoke) <=> Subscription: PG-NA-External-Prod-05, etc.

### CICD (Continuous Integration Continuous Delivery) Framework

*   **Connections:**
    *   CICD <=> AI Factory - Generative AI (AI) Platform - External Platform (Source Code Deployments [HTTPS])
    *   CICD <=> AI Factory - Generative AI (AI) Platform - Internal Platform (Source Code Deployments [HTTPS])
    *   CICD <=> Azure (Source Code)

### Spyglass

*   **Connections:**
    *   Spyglass <=> AI Factory - Generative AI (AI) Platform - Internal Platform (Logs [HTTPS])

---

## Cross-Architecture Flows

*   **P&G User (Global Internet)** <=> API Gateway <=> API Management <=> AI Factory - Generative AI Platform - External Platform (Request [HTTPS])
*   **P&G User (Global PGI)** <=> API Management <=> AI Factory - Generative AI Platform - Internal Platform (Request [HTTPS])
*   **P&G Admin, AI Engineer, AI Factory Operations** <=> AI Factory - Generative AI Platform - Internal Platform (User & Task Admin [HTTPS, UI])
*   **P&G Model Developer, AI Engineer, Data Science, Model Ops Engineer** (via IDE) <=> GitHub Enterprise Cloud <=> CICD <=> AI Factory - Generative AI Platform (Source Code, Source Code Deployments)

---

## Note

*   Those requests go through Traffic Manager and APIM which is part of AIF External Shared Services.
