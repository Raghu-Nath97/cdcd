---
description: 'Execute systematic checklist assessment with user interaction'
mode: 'agent'
tools: ['codebase', 'editFiles', 'search']
---

# Execute Checklist Assessment

This task guides you through a systematic checklist assessment process with required user interaction.

## Process Overview

1. **Load the specified checklist** from the provided checklist file
2. **Present checklist items systematically** - one section at a time
3. **Elicit user responses** for each checklist item using the exact format below
4. **Document findings** as you progress through each item
5. **Mark items as completed** and track overall progress
6. **Generate final assessment report** with all findings and recommendations

## Required User Interaction Format

For each checklist item, use this exact format:

```
## Checklist Item: [Item Title]

**Question:** [Specific question about this checklist item]

**Options:**
1. Fully Compliant - No issues identified
2. Partially Compliant - Minor issues need attention  
3. Non-Compliant - Significant issues require immediate action
4. Not Applicable - This item doesn't apply to current context
5. Need More Information - Additional details required

**Please respond with the number (1-5) and any additional details or context.**
```

## Documentation Requirements

- Create a running log of all responses and findings
- Note any areas requiring follow-up or remediation
- Include timestamps and user responses
- Generate summary recommendations at completion

## Critical Rules

- NEVER skip the elicitation format - user interaction is mandatory
- Present items in logical order from the checklist
- Wait for user response before proceeding to next item
- Document everything for audit trail purposes
- Provide clear next steps and recommendations

## Completion

Upon finishing all checklist items:
1. Provide a comprehensive summary
2. List all non-compliant or partially compliant items
3. Prioritize recommendations by risk level
4. Suggest timeline for remediation actions
