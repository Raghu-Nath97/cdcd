---
name: reviewing-python-code
description: 'Reviews Python code for P&G standards compliance, best practices, and quality issues. Use when reviewing pull requests, checking code quality, refactoring Python code, or ensuring compliance with P&G coding standards.'
---

# Python Code Review

Reviews Python code against P&G coding standards and industry best practices.

## Quick Review Checklist

### Code Style
- [ ] Follows PEP 8 style guide
- [ ] Uses 4 spaces for indentation
- [ ] Line length within 80-120 characters
- [ ] Consistent string quoting (single or double)
- [ ] No semicolons at end of statements

### Type Hints & Documentation
- [ ] Functions have type hints for parameters and return values
- [ ] Public modules/functions/classes have docstrings (Google style)
- [ ] Docstrings are descriptive, not imperative

### Naming Conventions
- [ ] `snake_case` for functions, variables, modules
- [ ] `CamelCase` for classes
- [ ] `ALL_CAPS` for constants
- [ ] Descriptive names (avoid single letters like `I`, `O`, `l`)

### Imports
- [ ] Imports at top of file (after docstring)
- [ ] Grouped: stdlib → third-party → local
- [ ] No `from module import *`
- [ ] Absolute imports preferred over relative

### Code Quality
- [ ] Functions have single, clear purpose
- [ ] Functions ~50 lines max
- [ ] Uses f-strings for formatting
- [ ] Uses `pathlib` for file operations
- [ ] Edge cases handled with clear exceptions

## Common Issues to Flag

### ❌ Bad Patterns

```python
# Bad: mutable default argument
def append_item(item, items=[]):
    items.append(item)
    return items

# Bad: bare except
try:
    risky_operation()
except:
    pass

# Bad: using os.path instead of pathlib
import os
path = os.path.join(base, "subdir", "file.txt")

# Bad: string concatenation in loops
result = ""
for item in items:
    result += str(item)

# Bad: no type hints
def process(data, flag):
    return data if flag else None
```

### ✅ Good Patterns

```python
# Good: immutable default
def append_item(item, items: list | None = None) -> list:
    if items is None:
        items = []
    items.append(item)
    return items

# Good: specific exception handling
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise

# Good: pathlib
from pathlib import Path
path = Path(base) / "subdir" / "file.txt"

# Good: list comprehension or join
result = "".join(str(item) for item in items)

# Good: type hints
def process(data: dict, flag: bool) -> dict | None:
    return data if flag else None
```

## Google Style Docstring Format

```python
def calculate_metrics(
    data: pd.DataFrame,
    columns: list[str],
    threshold: float = 0.5
) -> dict[str, float]:
    """Calculate statistical metrics for specified columns.

    Computes mean, median, and standard deviation for each column
    that exceeds the threshold value.

    Args:
        data: Input DataFrame containing the data to analyze.
        columns: List of column names to process.
        threshold: Minimum value threshold for inclusion. Defaults to 0.5.

    Returns:
        Dictionary mapping column names to their computed metrics.

    Raises:
        ValueError: If any column name is not found in the DataFrame.
        TypeError: If data is not a pandas DataFrame.

    Example:
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> calculate_metrics(df, ["a", "b"])
        {"a": {"mean": 2.0, "median": 2.0}, "b": {"mean": 5.0, "median": 5.0}}
    """
```

## Type Hints Quick Reference

```python
# Python 3.9+ (prefer built-in types)
def process(items: list[str], config: dict[str, int]) -> tuple[str, int]:
    ...

# Optional values
def fetch(url: str, timeout: int | None = None) -> str:
    ...

# Callable
from collections.abc import Callable
def apply(func: Callable[[int], str], value: int) -> str:
    ...

# TypedDict for structured dicts
from typing_extensions import TypedDict

class Config(TypedDict):
    name: str
    value: int
```

## Decision Guide

| Issue | Fix | Reference |
|-------|-----|-----------|
| Missing type hints | Add parameter and return types | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |
| No docstring | Add Google-style docstring | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |
| Using os.path | Replace with pathlib | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |
| Bare except | Use specific exception types | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |
| Long function | Split into smaller functions | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |
| Magic numbers | Extract to named constants | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |
| Import * | Use explicit imports | [Standards](.devagent/ai_docs/python/python-code-development-standards.md) |

## Reference Materials

- [Complete P&G Standards](.devagent/ai_docs/python/python-code-development-standards.md)
- [Code Review Cheat Sheet](.devagent/ai_docs/python/python-code-review-cheat-sheet.md)


## Related Skills

- `developing-pyrogai-pipelines` - Python standards for PyrogAI step implementations
- `building-langgraph-agents` - Python standards for LangGraph agent code
