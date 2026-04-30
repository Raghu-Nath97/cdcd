# (Generative AI UC Name) Technical Infrastructure Diagram (TID) — Reference Architecture

*   **Diagram Owner:** [[Owner Name]]
*   **Last Update:** [[Date]]

> Reference architecture template for the **network/infrastructure** view of any new GenAI use case. Shows the Cincinnati GO PGI zone, the Global Internet zone and the Azure Environment zone, with port/protocol annotations on every link.

---

## Cincinnati GO PGI

### P&G API User, End-User

*   **Device:** Web browser/Device
*   **Authentication/Access:**
    *   Web browser/Device <=> EntraID (port 443, https)
    *   Web browser/Device <=> Ping Federate (port 443, https)

### P&G Software Engineer

*   **Device:** Web browser/Device
*   **Authentication/Access:**
    *   Web browser/Device <=> EntraID (port 443, https)
    *   Web browser/Device <=> Ping Federate (port 443, https)
*   **Components:**
    *   Spyglass (FFT000045B38407)
*   **Interactions:**
    *   Web browser/Device <=> Spyglass (Logging, Monitoring, Tracing)

### P&G Operations & Maintenance Teams

*   **Device:** Web browser/Device
*   **Authentication/Access:**
    *   Web browser/Device <=> EntraID (port 443, https)
    *   Web browser/Device <=> Ping Federate (port 443, https)

---

## Global Internet

### External API User, End-User

*   **Device:** Web browser/Device
*   **Components:**
    *   P&G External Application ()
*   **Interactions:**
    *   Web browser/Device <=> P&G External Application () (port 443, https)

---

## Azure Environment (General)

### EAI Azure API Management (001F0FE72CC30765)

*   **Interactions:**
    *   EAI Azure API Management <=> AI Factory - Generative AI (Artificial Intelligence) Platform (port 443, https)
    *   EAI Azure API Management <=> P&G Internal Application () (API Management)

### P&G Internal Application ()

*   **Networking:** `project-network` (999.0.0.0/16)
    *   Private Endpoints
*   **Interactions:**
    *   P&G Internal Application () <=> AI Factory - Generative AI (Artificial Intelligence) Platform (port 443, https)

### AI Factory - Generative AI (Artificial Intelligence) Platform (C004260728)

*   **Hierarchical Grouping:**
    *   AI Factory - Shared Services - External Platform
    *   Foundational Models
    *   Vertex AI
    *   Open AI
*   **Interactions:**
    *   AI Factory - Generative AI Platform <=> Foundational Models (port 443, https)
    *   AI Factory - Generative AI Platform <=> Vertex AI (port 443, https)
    *   AI Factory - Generative AI Platform <=> Open AI (port 443, https)

---

## Cross-System Interactions

*   **Between PGI and Azure:**
    *   Web browser/Device (P&G API User, End-User) <=> P&G Internal Application () (port 443, https)
    *   Web browser/Device (P&G Software Engineer) <=> P&G Internal Application () (port 443, https)
    *   Web browser/Device (P&G Operations & Maintenance Teams) <=> P&G Internal Application () (port 443, https)
    *   Spyglass <=> P&G Internal Application () (port 443, https)
    *   P&G External Application () <=> EAI Azure API Management (port 443, https)

---

## Note (Warning)

*   This diagram provides a reference architecture for connecting a new use case to the GenAI platform.
*   To customise the diagram to meet the requirements of the new use case, you should:
    *   Remove all unnecessary blocks
    *   Add missing components of the new solution
    *   Add information about the processes and actual data flow for the blocks
    *   Fill in the cover table
    *   Register the application
