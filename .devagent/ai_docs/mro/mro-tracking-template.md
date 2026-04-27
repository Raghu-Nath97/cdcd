# MRO Assessment Tracking Template

This template is used by the MRO Agent to create and maintain the `mro.md` file in the project root. The agent should copy this structure when initializing a new assessment.

---

## Template Content

```markdown
# MRO Assessment Progress

## Assessment Metadata

| Field | Value |
|-------|-------|
| **Checklist Type** | [Data QA / Model QA / GenAI QA] |
| **Project Name** | [Project name] |
| **Started Date** | [YYYY-MM-DD] |
| **Last Updated** | [YYYY-MM-DD] |
| **Assessor** | [Name or "MRO Agent"] |
| **Overall Progress** | [X]% ([completed]/[total] items) |

---

## Section Progress

| Section | Status | Items Complete | Notes |
|---------|--------|----------------|-------|
| [Section 1 Name] | Not Started / In Progress / Complete | 0/X | |
| [Section 2 Name] | Not Started / In Progress / Complete | 0/X | |
| ... | ... | ... | |

---

## Detailed Item Tracking

### [Section 1 Name]

#### Item 1.1: [Question/Item Title]
- **Status:** [ ] Not Checked / [~] In Progress / [x] Complete / [!] Needs Attention
- **Detection Method:** Auto-detected / User-provided / N/A
- **Answer:** 
  > [Answer content here]
- **Evidence:**
  - `path/to/relevant/file.py` - [Brief description]
  - `path/to/config.yaml` - [Brief description]
- **Notes:** [Any additional notes or concerns]
- **Checked Date:** [YYYY-MM-DD]

#### Item 1.2: [Question/Item Title]
- **Status:** [ ] Not Checked
- **Detection Method:** 
- **Answer:** 
- **Evidence:**
- **Notes:**
- **Checked Date:**

[Continue for each item...]

---

## Findings Summary

### Issues Identified
1. [Issue description] - **Severity:** High/Medium/Low
2. [Issue description] - **Severity:** High/Medium/Low

### Recommendations
1. [Recommendation]
2. [Recommendation]

### Positive Findings
1. [What's working well]
2. [What's working well]

---

## Session Log

| Date | Session Summary | Items Completed |
|------|-----------------|-----------------|
| [YYYY-MM-DD] | [Brief summary of what was covered] | [List of item IDs] |
| [YYYY-MM-DD] | [Brief summary of what was covered] | [List of item IDs] |

---

## Next Steps

- [ ] [Next item to review]
- [ ] [Next item to review]
- [ ] [Pending action item]

---

*This file is automatically maintained by the MRO Agent. Manual edits are allowed but may be overwritten during assessment sessions.*
```

---

## Usage Instructions for the Agent

1. **Creating a new mro.md:**
   - Copy the template structure above
   - Fill in the Assessment Metadata
   - Populate Section Progress based on the selected checklist
   - Create item entries for each checklist question

2. **Updating mro.md during assessment:**
   - Update item status as you progress
   - Add evidence links when auto-detecting information
   - Record answers (both auto-detected and user-provided)
   - Update section progress counts
   - Recalculate overall progress percentage
   - Add to Session Log at end of each session

3. **Resuming from existing mro.md:**
   - Read the file to understand current state
   - Check "Next Steps" for where to continue
   - Skip items already marked as complete
   - Continue from first incomplete item

4. **Status Legend:**
   - `[ ]` - Not Checked: Item has not been reviewed yet
   - `[~]` - In Progress: Item is being reviewed or needs more info
   - `[x]` - Complete: Item has been fully reviewed and documented
   - `[!]` - Needs Attention: Item has issues or concerns requiring follow-up
