# LangChain Structured Output Guide

Guide to extracting structured, type-safe data from LLM responses using LangChain.

## Table of Contents
1. [Overview](#overview)
2. [Using ToolStrategy](#using-toolstrategy)
3. [Using ProviderStrategy](#using-providerstrategy)
4. [Schema Design](#schema-design)
5. [Validation and Error Handling](#validation-and-error-handling)
6. [Common Patterns](#common-patterns)

---

## Overview

Structured output ensures LLM responses conform to a specific schema, making them predictable and type-safe.

### Why Structured Output?

- **Type safety**: Responses conform to Pydantic models
- **Validation**: Automatic field validation
- **Predictability**: No parsing of free-text responses
- **Integration**: Easy integration with databases and APIs

---

## Using ToolStrategy

`ToolStrategy` uses function calling to enforce structured output:

### Basic Example

```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class PersonInfo(BaseModel):
    """Extracted person information."""
    name: str = Field(description="Full name")
    email: str = Field(description="Email address")
    phone: str | None = Field(default=None, description="Phone number")

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    response_format=ToolStrategy(PersonInfo),
    system_prompt="Extract person information from the input."
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "John Doe, john@example.com, 555-1234"}]
})

person: PersonInfo = result["structured_response"]
print(f"Name: {person.name}, Email: {person.email}")
```

### Classification Example

```python
from typing import Literal

class SentimentAnalysis(BaseModel):
    """Sentiment analysis result."""
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        description="Overall sentiment"
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Confidence score (0.0-1.0)"
    )
    key_phrases: list[str] = Field(
        description="Key phrases that influenced sentiment"
    )

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[],
    response_format=ToolStrategy(SentimentAnalysis)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "This product is amazing! Best purchase ever!"}]
})

analysis: SentimentAnalysis = result["structured_response"]
```

---

## Using ProviderStrategy

`ProviderStrategy` uses provider-native structured output (when available):

```python
from langchain.agents.structured_output import ProviderStrategy

# Some providers have native structured output support
agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    response_format=ProviderStrategy(PersonInfo),
    system_prompt="Extract person information."
)
```

**Note**: `ProviderStrategy` is more efficient but not all providers support it. `ToolStrategy` works universally.

---

## Schema Design

### Complex Nested Schemas

```python
class Address(BaseModel):
    """Address information."""
    street: str
    city: str
    state: str = Field(min_length=2, max_length=2)
    zip_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")

class Contact(BaseModel):
    """Contact method."""
    type: Literal["email", "phone", "mail"]
    value: str
    preferred: bool = False

class Customer(BaseModel):
    """Complete customer information."""
    name: str
    age: int = Field(ge=18, le=120)
    address: Address
    contacts: list[Contact] = Field(min_items=1)
    notes: str | None = None

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    response_format=ToolStrategy(Customer)
)
```

### Enum-Based Fields

```python
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TicketClassification(BaseModel):
    """Support ticket classification."""
    category: Literal["bug", "feature", "question", "complaint"]
    priority: Priority
    estimated_hours: float = Field(ge=0.5, le=40)
    tags: list[str] = Field(max_items=5)
```

### Optional vs Required Fields

```python
class ProductReview(BaseModel):
    """Product review analysis."""
    # Required fields
    product_name: str
    rating: int = Field(ge=1, le=5)
    sentiment: Literal["positive", "neutral", "negative"]
    
    # Optional fields
    pros: list[str] | None = None
    cons: list[str] | None = None
    recommendation: str | None = None
```

---

## Validation and Error Handling

### Field Validators

```python
from pydantic import field_validator

class EmailContact(BaseModel):
    """Contact with email validation."""
    name: str
    email: str
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Invalid email format")
        return v.lower()

class AgeValidator(BaseModel):
    """Age with business logic validation."""
    name: str
    age: int
    
    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError("Must be 18 or older")
        if v > 100:
            raise ValueError("Age seems unrealistic")
        return v
```

### Model Validators

```python
from pydantic import model_validator

class DateRange(BaseModel):
    """Date range with cross-field validation."""
    start_date: str
    end_date: str
    
    @model_validator(mode="after")
    def validate_date_range(self):
        from datetime import datetime
        
        start = datetime.fromisoformat(self.start_date)
        end = datetime.fromisoformat(self.end_date)
        
        if end < start:
            raise ValueError("end_date must be after start_date")
        
        return self
```

### Handling Validation Errors

```python
from pydantic import ValidationError

try:
    result = agent.invoke({
        "messages": [{"role": "user", "content": "Extract data from this..."}]
    })
    data = result["structured_response"]
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Handle validation errors
```

---

## Common Patterns

### Data Extraction

```python
class InvoiceData(BaseModel):
    """Invoice information extraction."""
    invoice_number: str
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    vendor: str
    total_amount: float = Field(ge=0)
    line_items: list[dict] = Field(default_factory=list)

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    response_format=ToolStrategy(InvoiceData),
    system_prompt="Extract invoice information from the document."
)
```

### Classification

```python
class ContentModeration(BaseModel):
    """Content moderation result."""
    is_safe: bool
    categories: list[Literal["spam", "hate", "violence", "adult", "clean"]]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    tools=[],
    response_format=ToolStrategy(ContentModeration)
)
```

### Multi-Step Analysis

```python
class CompetitorAnalysis(BaseModel):
    """Competitor analysis result."""
    competitors: list[str]
    market_share: dict[str, float]
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]
    recommendation: str

agent = create_agent(
    model="openai:gpt-5",
    tools=[search_tool, database_tool],  # Can use tools too!
    response_format=ToolStrategy(CompetitorAnalysis),
    system_prompt="Research competitors and provide SWOT analysis."
)
```

### Combining with Tools

```python
@tool
def search_database(query: str) -> str:
    """Search internal database."""
    return f"Database results for: {query}"

class ResearchReport(BaseModel):
    """Research report with citations."""
    summary: str
    key_findings: list[str]
    data_sources: list[str]
    confidence: Literal["high", "medium", "low"]

agent = create_agent(
    model="openai:gpt-4o",
    tools=[search_database],  # Agent can use tools during research
    response_format=ToolStrategy(ResearchReport),
    system_prompt="Research the topic and provide a structured report."
)
```

---

## Best Practices

1. **Clear descriptions**: Use `Field(description=...)` for better model understanding
2. **Validation**: Add validators for business logic
3. **Optional fields**: Use `| None` with defaults for optional data
4. **Enums**: Use `Literal` or `Enum` for fixed choices
5. **ToolStrategy first**: Use `ToolStrategy` unless provider-specific features are needed
6. **Test schemas**: Validate schemas with real data before deployment
7. **Handle errors**: Wrap invocations in try/except for `ValidationError`
8. **Keep it simple**: Don't over-complicate schemas; start simple and iterate
9. **Document schemas**: Add docstrings to classes and fields
10. **Version schemas**: Consider versioning for production schemas

---

## Production Example

Sentiment analysis with structured output:

```python
class SentimentResult(BaseModel):
    """Sentiment analysis structured output."""
    sentiment: Literal["positive", "neutral", "negative"]
    confidence: float = Field(ge=0.0, le=1.0)
    aspects: list[str] = Field(default_factory=list)

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    response_format=ToolStrategy(SentimentResult),
    system_prompt="Analyze the sentiment of customer reviews."
)

# Use in batch processing
results = []
for review in reviews:
    result = agent.invoke({
        "messages": [{"role": "user", "content": review}]
    })
    results.append(result["structured_response"])
```

---

## Integration with NileGPT

Example usage in NileGPT for sentiment analysis:

```python
class SentimentResult(BaseModel):
    """Sentiment analysis structured output."""
    sentiment: Literal["positive", "neutral", "negative"]
    confidence: float = Field(ge=0.0, le=1.0)
    aspects: list[str] = Field(default_factory=list)

agent = create_agent(
    model="openai:gpt-4o",
    tools=[],
    response_format=ToolStrategy(SentimentResult),
    system_prompt="Analyze the sentiment of customer reviews."
)

# Use in batch processing
results = []
for review in reviews:
    result = agent.invoke({
        "messages": [{"role": "user", "content": review}]
    })
    results.append(result["structured_response"])
```
