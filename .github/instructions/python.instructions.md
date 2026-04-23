---
name: 'Python Standards'
description: 'Python coding conventions and guidelines'
applyTo: '**/*.py'
---

# Python Coding Conventions

## Quick Reference

This document provides a quick reference for Python coding standards. For comprehensive details, refer to:

- **Detailed Standards**: `ai_docs/python/python-code-development-standards.md` - Complete P&G Python development standards
- **Code Review Guide**: `ai_docs/python/python-code-review-cheat-sheet.md` - Code review checklist and common issues

## Python Instructions

-   Write clear and concise comments for each function explaining the "why", not just the "how"
-   Ensure functions have descriptive names and include type hints
-   Provide docstrings following Google Style conventions (descriptive-style, not imperative)
-   For Python 3.9+, prefer built-in collections for type hints (e.g., `list[str]`, `dict[str, int]`)
-   For Python 3.8 and below, use the `typing` module when needed
-   Break down complex functions into smaller, manageable functions (ideally ~50 lines each)
-   Use f-strings for string formatting over other methods
-   Use pathlib for file operations instead of os.path

## General Instructions

-   Always prioritize readability and clarity (KISS principle)
-   For algorithm-related code, include explanations of the approach used
-   Write code with good maintainability practices, including comments on why certain design decisions were made
-   Handle edge cases and write clear exception handling
-   For libraries or external dependencies, mention their usage and purpose in comments
-   Use consistent naming conventions and follow language-specific best practices
-   Write concise, efficient, and idiomatic code that is also easily understandable
-   When you are done with your work, run black on the files you have been working on
-   Use absolute imports instead of relative imports
-   Use descriptive variable names (avoid single letters like `I`, `O`, `l`)
-   Never use triple-quoted strings as multi-line comments

## Code Style and Formatting

-   Follow the **PEP 8** style guide for Python (see detailed standards in `ai_docs/python/`)
-   Use **flake8** for automated style checking as specified in development standards
-   Maintain proper indentation (use 4 spaces for each level of indentation)
-   Line length: maintain consistency within project (80-120 characters, align with team)
-   Place function and class docstrings immediately after the `def` or `class` keyword
-   Use blank lines appropriately:
    -   2 blank lines between top-level functions and classes
    -   1 blank line between methods in a class
    -   1 blank line between logical sections within functions
-   Use Google style docstrings with descriptive language
-   Don't use semicolons
-   Use consistent string quoting (pick single or double quotes and stick to it)
-   Use `"""triple-double quotes"""` for docstrings
-   **Don't inherit from `object`** - it's default in Python 3

## Naming Conventions

-   **Modules/Packages**: all_lowercase_with_underscores
-   **Classes**: CamelCase
-   **Variables/Functions**: all_lowercase_with_underscores
-   **Constants**: ALL_UPPERCASE_WITH_UNDERSCORES
-   **Private attributes**: Use `__all__` to define public interface rather than `_leading_underscore`
-   Avoid conflicts with Python keywords using suffix (e.g., `class_name` not `_class`)
-   Use standard abbreviations only when widely understood (e.g., `pd` for pandas, `np` for numpy)

## Imports

-   Always import at the top of the file (after module docstring and `__all__`)
-   Group imports in three sections with blank lines between:
    1. Standard library imports
    2. Third-party imports
    3. Local application imports
-   Within each group: non-from imports before from imports
-   Names imported from one source should appear in one `from ... import ...` statement
-   Never use `from module import *` in production code
-   Use `import module as alias` only for standard abbreviations

## Code Modularity and Structure

-   Use `__all__ = []` to explicitly define module's public interface
-   Typical module length should be ~150 lines
-   One class per module (with exceptions for tightly-coupled helper classes)
-   Use `if __name__ == '__main__':` for executable modules
-   Parametrize static/reusable elements using configuration files
-   Use environment variables for environment-specific settings (not configuration)

## Default Arguments and Functions

-   Use default argument values when the same value is used 90% of the time
-   Functions should have a single, clear purpose
-   Use conditional expressions (ternary operator) for simple conditions
-   Prefer list comprehensions over explicit loops when appropriate
-   Use `return None` when explicitly returning None, bare `return` to exit early

## Exception Handling and Edge Cases

-   Always include test cases for critical paths of the application
-   Account for common edge cases like empty inputs, invalid data types, and large datasets
-   Include comments for edge cases and expected behavior
-   Write unit tests for functions with descriptive docstrings
-   Use `raise NotImplementedError('description')` for methods meant to be overridden
-   Provide explanations for unusual, unobvious, or unexpected implementations

## Data Naming Conventions

When creating new data objects, follow P&G Data Naming Convention:

-   Use lowercase with underscores
-   Use singular nouns (e.g., `event` not `events`)
-   Use US English spelling
-   Names should be: unambiguous, meaningful, self-documenting, and concise
-   For attributes: optional qualifiers + mandatory class + function words
-   Common functions: `id`, `name`, `code`, `amt`, `qty`, `cnt`, `pct`, `date`, `desc`

## Documentation

-   Every public module/function/class/method needs a docstring
-   Use Google style docstrings consistently
-   Module docstrings should include usage examples
-   Class docstrings should summarize behavior and list public methods
-   Function docstrings should document args, returns, and raised exceptions
-   Use TODO comments for planned improvements: `# TODO(name): description`

## Example of Proper Documentation

```python
def calculate_circle_area(radius: float, pi: float = 3.14159) -> float:
    """Calculate the area of a circle given the radius.

    Args:
        radius: The radius of the circle in units.
        pi: Value of pi to use in calculation. Defaults to 3.14159.

    Returns:
        The area of the circle, calculated as π * radius².

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative")

    return pi * radius ** 2
```

## Performance and Best Practices

-   Use appropriate log severity levels
-   For set operations, use method versions (`union()`, `intersection()`) over operators
-   Use f-strings for string formatting
-   Leverage pathlib for file operations
-   Use namedtuple for simple data structures instead of classes when appropriate
-   Consider using conditional expressions for simple if-else assignments
