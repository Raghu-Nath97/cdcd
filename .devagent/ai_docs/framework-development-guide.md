# Custom Framework Development Guide

Create personalized GitHub Copilot configurations for your specific frameworks and technology stacks using the **creating-copilot-customizations** skill.

## Quick Start (2 minutes)

### What This Does
The `creating-copilot-customizations` skill guides you through creating **custom GitHub Copilot configurations** specifically for your repository. You get help creating personalized prompts, agents, skills, and instructions tailored to your technology stack.

### How to Get Started
1. **Install DevAgent** in your repository: `devagent init --frameworks general`
2. **Open GitHub Copilot Chat** and describe what you need:

```
I want to create a custom agent for my [framework/library] that helps with [specific tasks].
Help me write the .agent.md file with proper frontmatter and focused content.
```

**Result**: You'll be guided through creating proper `.prompt.md`, `.agent.md`, `.instructions.md`, or `SKILL.md` files for your `.github/` directory, following research-backed best practices.

## Minimal Effort Examples (5 minutes each)

### Example 1: Unknown Library (Let AI Do Everything)
**Time**: 2 minutes

```
I need GitHub Copilot support for a Python package I'm using, but I don't want to spend time researching it.

**Basic Info:**
- Package: streamlit-aggrid 
- I use it to display data tables in Streamlit apps
- Here's how I typically use it:

from st_aggrid import AgGrid
import pandas as pd

df = pd.read_csv("data.csv")
AgGrid(df)

**What I Want:**
Just create good GitHub Copilot configurations. I trust you to make the right decisions about what would be most helpful.
```

**Perfect for**: Busy developers who want immediate productivity gains without research.

### Example 2: Framework I Use Daily
**Time**: 3 minutes

```
I work with FastAPI every day and want better GitHub Copilot support.

**Framework**: FastAPI with Python 3.11+
**My typical code**:

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

**What I struggle with**:
- Setting up new endpoints quickly
- Proper error handling patterns  
- Database integration best practices

Please create configurations that help with these common tasks.
```

**Perfect for**: Developers who know what they need help with.

### Example 3: Testing Framework Setup
**Time**: 5 minutes

```
I want better Copilot support for my Playwright testing setup.

**Setup**:
- Playwright with TypeScript
- Custom utilities in `utils/test-helpers.ts`
- Page object pattern in `tests/pages/`

**Common tasks I do**:
- Creating new page objects
- Writing API tests
- Setting up test fixtures

**What I need**:
- Prompts for generating page objects
- Agent that knows Playwright + my custom patterns
- Instructions for organizing tests properly

Here's a typical page object I create:
// example of my pattern

Can you create configurations that match my existing patterns?
```

**Perfect for**: Developers with established patterns who want AI support for their specific setup.

## Moderate Effort Examples (10 minutes each)

### Example 4: Internal Framework with Documentation
**Time**: 8 minutes

```
I need GitHub Copilot support for our internal company framework.

**Framework Details**:
- Name: DataPipeline (internal framework)
- Documentation: [internal wiki link]
- Language: Python
- Purpose: ETL operations

**Key Concepts**:
- Pipeline classes inherit from `BasePipeline`  
- Step decorators: `@extract`, `@transform`, `@load`
- YAML configuration files
- Built-in logging and error handling

**Common Development Tasks**:
1. Creating new pipeline modules
2. Setting up configuration files
3. Error handling and logging
4. Testing with mock data

**What I Need**:
- Prompt for pipeline boilerplate generation
- Custom agent with our internal patterns
- Instructions for proper error handling
- Reference docs for common patterns

Please help me create comprehensive Copilot support.
```

**Perfect for**: Teams with internal frameworks and some documentation.

### Example 5: Web Framework with Specific Needs
**Time**: 10 minutes

```
I want comprehensive GitHub Copilot support for SvelteKit development.

**Framework Details**:
- SvelteKit 2.x
- Official docs: https://kit.svelte.dev/
- TypeScript setup
- Our specific patterns: file-based routing, SSR with load functions

**Development Workflow**:
1. Create routes with `+page.svelte`, `+layout.svelte`
2. Server-side logic in `+page.server.ts`
3. Form actions with progressive enhancement
4. State management with Svelte stores
5. Performance optimization for SEO

**Specific Help Needed**:
- Prompt for scaffolding new routes with proper file structure  
- Custom agent with SvelteKit best practices
- Instructions for component organization
- Reference docs for load function patterns

**Current Challenge Areas**:
- Form handling with proper validation
- SSR optimization
- Store patterns for complex state

Could you analyze SvelteKit and create configurations that address these specific needs?
```

**Perfect for**: Developers working with well-documented frameworks who have specific workflow needs.

## Advanced Tips

### Getting Better Results

#### Be Specific About Your Patterns
Instead of: "I use React"
Try: "I use React with TypeScript, custom hooks in `src/hooks/`, and Zustand for state management"

#### Share Code Examples
Include actual code snippets showing your current patterns - this helps create configurations that match your existing style.

#### Mention Your Struggles
Explicitly state what you find difficult or time-consuming - these become the focus areas for your custom configurations.

#### Iterate and Refine
After trying the generated configurations, ask for refinements:
```
The prompt you created works well, but could you modify it to also handle error boundaries in React components?
```

### What You Get

#### Custom Prompts (`.github/prompts/`)
- **Boilerplate generation**: Create standard code structures quickly
- **Debugging assistance**: Framework-specific troubleshooting  
- **Optimization help**: Performance and best practices guidance
- **Testing support**: Generate tests following your patterns

#### Custom Agents (`.github/agents/`)
- **Domain expertise**: AI that knows your framework deeply
- **Interactive guidance**: Ask questions and get expert answers
- **Pattern recognition**: Understands your specific setup and preferences
- **Troubleshooting**: Framework-specific problem solving
- **Handoff workflows**: Sequential agent transitions for complex tasks

#### Custom Instructions (`.github/instructions/`)
- **Coding standards**: Your team's specific conventions
- **File organization**: How you structure projects
- **Best practices**: Framework-specific guidelines
- **Quality checks**: Standards for code review

#### Reference Documentation (`.devagent/ai_docs/`)
- **API references**: Key methods and patterns
- **Examples**: Common code patterns and solutions
- **Troubleshooting**: Solutions to frequent problems
- **Context**: Additional information for AI understanding

### File Naming and Organization

Your custom files follow DevAgent conventions:
```
.github/
├── prompts/
│   ├── my-framework-setup.prompt.md
│   └── my-framework-debug.prompt.md
├── agents/
│   └── my-framework-expert.agent.md
├── instructions/
│   └── my-framework-standards.instructions.md
└── ai_docs/
    └── my-framework/
        ├── api-reference.md
        └── common-patterns.md
```

## Sharing Your Success

Created configurations that work exceptionally well? **Share them with the DevAgent team!**

### How to Share
1. **Document your success**: What framework, what problems it solved, how it improved your workflow
2. **Contact the DevAgent maintainers**: Share your story and configuration files
3. **Explain the value**: Who else could benefit from this framework support?

### What Happens Next
- **Review**: The DevAgent team evaluates your configurations
- **Community benefit**: Successful configs may become part of DevAgent's official framework collection
- **Recognition**: Contributors are credited for their community contributions

### Examples of Shareable Success
- "Created amazing SvelteKit support that handles our team's specific SSR patterns"
- "Built comprehensive testing configurations for Playwright + our custom utilities"
- "Generated FastAPI configs that solve our microservices development workflow"

Your custom configurations could help hundreds of other developers facing similar challenges!

## Tips for Success

### Start Small
Begin with one simple customization to understand the process, then expand to more complex needs.

### Provide Context
The more context you provide about your specific setup, the better the generated configurations will match your needs.

### Test and Iterate
Try the configurations, see what works, and ask for refinements. Copilot excels at iterative improvement.

### Think About Your Team
Consider creating configurations that benefit your entire team's workflow, not just your individual preferences.

Ready to create custom GitHub Copilot configurations for your framework? Use the `creating-copilot-customizations` skill and start with one of the examples above!