---
name: developing-pyrogai-pipelines
description: 'Develops PyrogAI ML pipelines, steps, and configurations. Use when creating Steps, writing pipeline YAML, debugging PyrogAI code, working with aif CLI commands, or integrating with Azure ML, Databricks, or Vertex AI platforms.'
---

# PyrogAI Pipeline Development

PyrogAI is P&G's AI Factory solution for building platform-agnostic machine learning pipelines that run on Azure ML, Databricks, Vertex AI, and locally.

## Quick Start

```python
from aif.pyrogai.steps.step import Step

class MyStep(Step):
    def run(self) -> None:
        self.logger.info("Starting step execution")
        # Access runtime params: self.runtime_parameters
        # Access secrets: self.secrets.get("my_secret")
        # Access file I/O: self.ioctx.get_input_fn("slot_name")
```

## Core Step Attributes

| Attribute | Purpose |
|-----------|---------|
| `self.logger` | Platform-aware logging |
| `self.runtime_parameters` | Runtime config dict |
| `self.secrets` | Cross-platform secret access |
| `self.ioctx` | File system abstraction (IoContext) |
| `self.mlflow` | MLflow tracking integration |
| `self.platform` | Current platform enum (AML/DBR/VERTEX/LOCAL) |
| `self.config` | Step configuration access |
| `self.pipeline` | Current pipeline information |

## CLI Essentials

**Always check `--help` first** - it's the most up-to-date reference:

```bash
# Discover commands
aif step --help
aif pipeline --help

# Create new step
aif step new -f my_step --class-name MyStep

# Run step locally
aif step run --pipeline-name my_pipeline --step-name my_step

# Run pipeline
aif pipeline run --name my_pipeline --platform local

# Generate notebook from pipeline
aif pipeline notebook --name my_pipeline
```

## Platform Detection Pattern

```python
from aif.pyrogai.const import Platform

if self.platform == Platform.DBR:
    df = self.spark_session.table("my_table")
elif self.platform == Platform.AML:
    dataset = self.ml_client.data.get("dataset_name", version="1")
elif self.platform == Platform.VERTEX:
    # Vertex AI-specific code
    pass
elif self.platform == Platform.LOCAL:
    # Local development code
    pass
```

## Input/Output Slots

```python
def run(self) -> None:
    # Read from input slot
    input_path = self.ioctx.get_input_fn("input_data")
    df = pd.read_parquet(input_path)
    
    # Write to output slot
    output_path = self.ioctx.get_output_fn("output_data")
    df.to_parquet(output_path)
```

## Secret Management

```python
def run(self) -> None:
    # Access secrets (works across all platforms)
    api_key = self.secrets.get("my_api_key")
    db_password = self.secrets.get("database_password")
```

## MLflow Integration

```python
def run(self) -> None:
    # Log parameters
    self.mlflow.log_param("learning_rate", 0.01)
    
    # Log metrics
    self.mlflow.log_metric("accuracy", 0.95)
    
    # Log artifacts
    self.mlflow.log_artifact("model.pkl")
    
    # Log model
    self.mlflow.sklearn.log_model(model, "model")
```

## Decision Guide

| Need | Solution | Reference |
|------|----------|-----------|
| Create new step | `aif step new -f name` | [Framework Reference](.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md) |
| Platform-specific code | Use `self.platform` enum | [Patterns & Examples](.devagent/ai_docs/pyrogai/pyrogai-patterns-examples.md) |
| Access secrets | `self.secrets.get()` | [Framework Reference](.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md) |
| File I/O across platforms | Use `self.ioctx` | [Framework Reference](.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md) |
| Track experiments | Use `self.mlflow` | [Framework Reference](.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md) |
| Debug step failures | `aif step run --step-name` | [Troubleshooting Guide](.devagent/ai_docs/pyrogai/pyrogai-troubleshooting-guide.md) |
| Pipeline configuration | Edit `pipeline.yaml` | [Framework Reference](.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md) |

## Common Pitfalls

- **Don't hardcode paths** - use `self.ioctx` for all file operations
- **Don't access secrets directly** - use `self.secrets.get()`
- **Don't assume platform** - use `self.platform` for platform-specific code
- **Always use `self.logger`** - not `print()` or standard logging

## Reference Materials

- [Complete Framework Reference](.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md)
- [Patterns & Examples](.devagent/ai_docs/pyrogai/pyrogai-patterns-examples.md)
- [Troubleshooting Guide](.devagent/ai_docs/pyrogai/pyrogai-troubleshooting-guide.md)

## Related Skills

- `building-langgraph-agents` - When building agentic workflows on PyrogAI
- `reviewing-python-code` - For Python coding standards in step implementations
