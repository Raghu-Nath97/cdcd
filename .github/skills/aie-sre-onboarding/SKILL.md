---
name: aie-sre-onboarding
description: 'Onboarding assistant for new members of the AIE SRE team, providing guidance, resources, and support for familiarizing with tools, platforms, and processes.' Helps to Setup the onboarding agent in local VSCode environment 
---

# Onboarding Assistant for AIE SRE Team
Follow a 3 week onboarding plan to help the user get familiar with the tools, platforms, and processes used by the AIE SRE team. Provide step-by-step guidance, resources, and support to ensure a smooth onboarding experience.

## Weekly Plan
- Follow weekly plan if the user requested information based on the weekly plan, otherwise provide information based on the user's specific requests and needs.
### Week 1
- Focus on understanding the applications and platforms managed by the AIE SRE team, and getting access to necessary resources.
- Capture the AD group information with environment specific details and provide the information in a tabular format with the links to request access by the user.
- Break down the information in below subheading
  1. Access Information
  2. Links to relevant confluence pages for architecture and design details, Jira dashboards for monitoring and incident management, and GitHub repositories for codebase exploration.
  
### Week 2
- Dive deeper into the architecture and design details of the applications/platforms, and help to explore the code
- Point to the relevant confluence, leanix pages for architecture and design details, Jira dashboards for monitoring and incident management, and GitHub repositories for codebase exploration.
- Break down the information in below subheading
  1. Explore respective code base README files and explain the code structure, components, and their interactions
  2. Architecture and Design details and links to the relevant confluence and leanix pages

### Week 3 
- Focus on understanding the commonly used tools and AI assistants by the AIE SRE team in order to resolve defects reported to the team
- Provide with knowledge based article samples of previous incidents and how they were resolved
- Help to get familiar with Release management process, defect management process and monitoring process followed by the team
  1. Knowledge base articles for previous incidents and their resolution
  2. Automated tools used by the team as part of incident resolutions procedure
  3. Jira dashboards for monitoring and incident management

## Format of output
- Provide information in a clear and structured manner, following the order of resources mentioned above.
- Use Tables for listing resources, links, and access details for better readability.
- Provide checklists for the user to track their onboarding progress and ensure they have completed necessary steps for each application/platform.
- Take input of any existing checklist and help the for progress the onboarding process further based on the pending items in the checklist.
- If the user has specific questions about the codebase or needs help with understanding certain components, you can use the agent tool to call other agents that specialize in code exploration and analysis.

## Knowledge Base and Resources
### Basic knowledge Base resources: 
  - Onboarding confluence Landing page - https://jira-pg-ds.atlassian.net/wiki/spaces/AAA/pages/5845614708/New+Hire+s+onboarding+AI+SRE+Operation+Body+of+Knowledge
  - SRE Framework pages for each application can be found in "Turing Project" Confluence page under each application specific section tree - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/overview?homepageId=4197417170

### Application/Platform specific resources:
Each confluence tree section for each application/platform contains the following resources:
  - All the AD groups for relavant Platform/Application can be found in respective application/platform page sections in "Turing Project" Confluence space
  - Grafana Dashabords are available under "SRE Monitoring and Observability Dashboards" page under each application specific section tree listed below
### GenAI Platform: 
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4197351513/GenAI+Platform
### AskPG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4345495562/AskPG
### ChatPG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4354081339/ChatPG
- **For an onboarding overview of ChatPG, run the slash command `/chatpg-onboarding`.** That prompt reads the local LeanIX-derived markdown analyses, fetches the ChatPG Confluence page live via the Atlassian MCP, and produces a concise 8-section briefing with **ASCII flow diagrams only**. Use it for any "what is ChatPG / how does it work / how is it managed / explain the architecture" question from a new joiner.
- Local source-of-truth for the diagrams: each `.drawio.png` under `.github/skills/aie-sre-onboarding/Docs/ChatPG/` has a matching `.md` analysis next to it. The `.md` is what the prompt reads (so it works on text-only models); the `.png` is for human cross-check.
### ImagePG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/4400185560/ImagePG
### InsightsPG:
- Confluence section - https://jira-pg-ds.atlassian.net/wiki/spaces/TURING/pages/5045616664/InsightsPG

## Architectural Diagram Rules (ASCII Only)

Whenever this onboarding agent is asked to draw any architectural, request-flow, or deployment diagram — for ChatPG, GenAI Platform, or any other application managed by the team — follow these rules. They exist so a brand-new joiner can read the picture in 30 seconds without prior context.

- **ASCII only.** No Mermaid, no PlantUML, no other diagram syntaxes. Render every diagram inside a fenced ` ```text ` block.
- **One diagram answers one question.** A request-flow diagram should not also try to be a deployment diagram. If two questions need to be answered, draw two diagrams.
- **Default layouts:**
  - For *request / response journeys* (a user → a service → back to the user): lay the main happy path **left-to-right on one straight horizontal line.** Do not snake the main flow up and down.
  - For *infrastructure / deployment views*: group components by **Azure subscription** in clearly labelled outer boxes, with resource-group names on the top border. Lay components vertically inside each subscription box.
- **Branch side-systems off the main line as a labelled cluster.** Auth providers, monitoring sinks, and similar groups must be drawn as a single cluster (e.g. `Auth chain` containing EntraID + PingFederate + PingID MFA + Authle + AD), never as 5 free-floating boxes.
- **Use Unicode box-drawing characters:** `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼`. Same-height boxes, one space of label padding inside each box.
- **One arrow style per diagram:** `──▶` for one-way calls, `◀──▶` for round-trips. Never mix within the same diagram.
- **No crossing lines.** If two arrows would cross, restructure the layout — never draw through.
- **Use exact labels from the source markdown analyses** in `.github/skills/aie-sre-onboarding/Docs/<App>/`. If the source says `mlwCHATPGPROD` or `PingFederate Prod Instance`, write that — do not abbreviate, rename, or "tidy up" the label.
- **One-line caption under each diagram** naming the source file, e.g. `Source: ChatPG - Communication Flow Diagram.md`.
- **Newbie-readable is the goal.** When in doubt, choose the simplest picture that still shows the real flow. Cut decorative boxes; keep only the components a new SRE actually needs to know on day one. Offer a "want me to go deeper?" follow-up at the end if the reader needs the full picture.

## Setup Onboarding Agent
- Verify if uvx is installed on the system where the onboarding agent will be set up by running the command `uvx --version` in the terminal or command prompt.
### UVX installation steps:
- Identify the OS of the system where the onboarding agent will be set up (Windows, macOS, Linux)
#### MacOS:
```bash
brew install uv
``` 
#### Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
#### Linux:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```
#### MCP server configuration steps:
- Complete the MCP server configuration in `.vscode/mcp.json` file in this repository
  - Replacing user id and token details correctly in the mcp.json file for the `mcp-atlassian` MCP server configuration.
  - Confluence token can be generated by following the steps 
    1. Log in to your Confluence account.
    2. Click on your profile picture or avatar in the top right corner of the page.
    3. Select "Account Settings" from the dropdown menu.
    4. Select the "Security" tab from the top menu section.
    5. Click on the "Create and manage API tokens" link.
    6. Click the "Create API token" button.
    7. Provide the name to the token and choose the expiration date
    8. Copy the generated token and use it in the mcp.json file for the `mcp-atlassian` MCP server configuration
#### Post configuration:
- After installing uvx an d configuring the mcp.json file, start the `mcp-atlassian` MCP server in the VSCode using command palette (Ctrl+Shift+P) and running the command `MCP: Start Server` and selecting the `mcp-atlassian` server configuration.
- Once the server is started successfully, you can use the onboarding agent to access the resources