---
description: 'Create comprehensive documentation using specified template'
mode: 'agent'
tools: ['editFiles', 'codebase', 'search']
---

# Create Documentation Task

This task guides you through creating comprehensive documentation using a specified template.

## Process Overview

1. **Load the specified template** from the provided template file
2. **Analyze template structure** and identify required sections
3. **Elicit information** from user for each template section
4. **Populate template** with gathered information
5. **Review and refine** the completed documentation
6. **Save the final document** in the appropriate location

## Required User Interaction Format

For each template section, use this exact format:

```
## Section: [Section Name]

**Purpose:** [Brief description of what this section covers]

**Required Information:**
- [List of specific information needed]
- [Include any formatting requirements]
- [Note any dependencies on other sections]

**Please provide the following details:**
[Specific questions or prompts for this section]
```

## Template Population Process

1. **Start with document metadata** (title, author, date, version)
2. **Work through sections systematically** in template order
3. **Cross-reference related sections** to ensure consistency
4. **Apply appropriate formatting** based on document type
5. **Include all required elements** from the template

## Quality Assurance

Before finalizing:
- Verify all template sections are completed
- Check for consistency across sections
- Ensure proper formatting and structure
- Validate any technical content or specifications
- Review for completeness and clarity

## File Naming and Location

- Use descriptive, standardized file names
- Include version numbers or dates as appropriate
- Save in the designated documentation directory
- Follow organizational naming conventions

## Completion Steps

1. Present the completed document for user review
2. Make any requested revisions
3. Save the final version in the appropriate location
4. Provide summary of created documentation
5. Suggest any follow-up actions or related documentation needs
