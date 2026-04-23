---
description: 'Create and set up a new feature branch following team conventions'
mode: 'agent'
tools: ['terminal', 'codebase']
---

# Feature Branch Setup

Create a new feature branch following team conventions with intelligent project analysis.

## Information Gathering

Ask for the following if not provided:

### Required Information
- **Ticket Number**: Ask for ticket/issue number (any format). If user says "no ticket" or similar, skip this in branch naming.
- **Feature Description**: 2-3 words describing the change
- **Change Type**: 
  - `feature` - New functionality
  - `bugfix` - Bug fixes  
  - `refactor` - Code improvements
  - `docs` - Documentation changes
  - `hotfix` - Urgent production fixes

## Branch Creation Process

### 1. Preparation
```bash
# Check current status and ensure clean working directory
git status

# Switch to main and get latest changes
git checkout main
git pull origin main
```

### 2. Branch Naming Convention

Based on ticket availability and change type:

#### With Ticket Number
- **Format**: `[type]/[ticket-number]-[short-description]`
- **Examples**: 
  - `feature/ML-123-customer-segmentation`
  - `bugfix/456-validation-error`
  - `refactor/PROJ-789-cleanup-config`

#### Without Ticket Number  
- **Format**: `[type]/[brief-description]`
- **Examples**: 
  - `feature/improve-error-handling`
  - `bugfix/memory-leak-fix`
  - `docs/update-api-documentation`

### 3. Create and Push Branch
```bash
# Create and switch to new branch
git checkout -b [branch-name]

# Push branch to remote and set up tracking
git push -u origin [branch-name]
```

## Project Context Analysis

**Quick project assessment** (for guidance only):

### Project Type Detection
- **PyrogAI Project**: Look for `aif.pyrogai` imports, pipeline configs
- **API Project**: Check for FastAPI, Flask, Django patterns
- **Data Project**: Look for pandas, numpy, data processing patterns
- **General Python**: Standard Python project structure

### Existing Patterns
- Note current directory structure and naming conventions
- Check for existing testing patterns
- Identify configuration management approach

## Next Steps Guidance

### Based on Change Type

#### New Features
- **Small Features**: Start implementing directly
- **Complex Features**: Consider using `/plan-product` for comprehensive planning
- **PyrogAI Features**: Reference PyrogAI chat mode (`@workspace #pyrogai`) for framework guidance

#### Bug Fixes
- Focus on isolated changes to minimize risk
- Add regression tests to prevent future occurrences
- Consider if root cause analysis is needed

#### Refactoring
- Plan backwards compatibility strategy
- Ensure comprehensive test coverage before changes
- Consider feature flags for large refactors

#### Documentation
- Update related documentation files
- Consider if API documentation needs updates
- Check if examples need to be updated

### Framework-Specific Guidance

#### For PyrogAI Projects
- **New Steps**: Follow PyrogAI step development patterns
- **IPA Endpoints**: Reference IPA development best practices
- **Configuration**: Use environment-specific config patterns
- **Testing**: Include both unit and integration tests

#### For API Projects
- **Endpoints**: Follow RESTful conventions
- **Validation**: Use proper request/response models
- **Testing**: Include API integration tests
- **Documentation**: Update OpenAPI/Swagger specs

## DevAgent Integration Check

If `.github` configurations detected:
```bash
# Check current DevAgent setup
devagent status

# Update configurations if they're outdated (optional)
devagent update --instructions-only  # for PyrogAI projects
devagent update --prompts            # for prompt updates
```

## Examples

### Complete Workflow Examples

#### With Ticket Number
```bash
# User input: "ML-456", "real-time-scoring", "feature"
git checkout main
git pull origin main
git checkout -b feature/ML-456-real-time-scoring
git push -u origin feature/ML-456-real-time-scoring
```

#### Without Ticket Number
```bash
# User input: "no ticket", "memory-leak-fix", "bugfix"
git checkout main
git pull origin main
git checkout -b bugfix/memory-leak-fix
git push -u origin bugfix/memory-leak-fix
```

## Scope Boundaries

### ✅ This Prompt DOES:
- Create properly named branches following team conventions
- Provide basic project context awareness
- Suggest appropriate next steps and resources
- Execute git commands for branch creation

### ❌ This Prompt does NOT:
- Create extensive file structures or scaffolding
- Write code templates or boilerplate
- Make architecture decisions
- Set up complex project configurations
- Replace comprehensive feature planning

### 🔗 Use Other Tools For:
- **Complex Planning**: `/plan-product` prompt
- **PyrogAI Guidance**: PyrogAI chat mode (`@workspace #pyrogai`)
- **Code Scaffolding**: Framework-specific generators or templates
- **Architecture Decisions**: Domain-specific chat modes

---

**Focus**: Quick, clean branch creation with awareness of project context and team conventions.
