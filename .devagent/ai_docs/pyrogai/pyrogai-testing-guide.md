# PyrogAI Step Testing Guide

Reference guide for `aif.pyrogai.testing` (v1.8.0.post14+) — PyrogAI's standardized testing module that eliminates manual patching.

> **Version requirement**: Requires PyrogAI >= 1.8.0.post14. Check with `pip show aif-pyrogai`. For detailed API docs or migration guidance, ask the **doc-retriever** agent.

## Overview

The testing module provides:

- **Zero manual patching** — no need to patch `PlatformProvider` or internal framework components
- **Fixture-based setup** — standard pytest patterns with automatic cleanup
- **File I/O via TestIoContext** — temporary directories managed automatically
- **Configuration injection** — config, runtime parameters, secrets
- **Assertion helpers** — built-in assertions for files, MLflow metrics, and artifacts
- **Mock factories** — ready-to-use mocks for BigQuery, GCS, MLflow

## Quick Start

### 1. Configure conftest.py

```python
pytest_plugins = ['aif.pyrogai.testing.fixtures']
```

### 2. Write a Test

```python
import pandas as pd

def test_my_step(step_env):
    # Arrange
    step_env.config = {"threshold": 0.85}
    step_env.write_input_file("data/input.parquet", pd.DataFrame({"col": [1, 2, 3]}))

    # Act
    step = MyStep()
    step_env.setup_step(step)
    step.run()

    # Assert
    step_env.assert_output_exists("data/output.parquet")
    output_df = step_env.read_output_df("data/output.parquet")
    assert len(output_df) == 3
```

### Alternative: Context Manager

```python
from aif.pyrogai.testing import step_environment

def test_my_step():
    with step_environment(config={"key": "val"}) as env:
        step = MyStep()
        env.setup_step(step)
        step.run()
        env.assert_output_exists("output.parquet")
```

## Public API

### Core Components

| Component | Description |
|-----------|-------------|
| `StepTestEnvironment` | Main testing interface with mocked dependencies and utilities |
| `TestIoContext` | IoContext subclass optimized for testing with temp directories |
| `step_env` | Pytest fixture with automatic cleanup (function-scoped) |
| `step_environment` | Context manager for explicit environment control |

### StepTestEnvironment Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `config` | `dict` | Step configuration dictionary |
| `runtime_parameters` | `dict` | Runtime parameters for the step |
| `secrets` | `dict` | Secrets dictionary |
| `ioctx` | `TestIoContext` | Test-optimized IoContext |
| `logger` | `MagicMock` | Mocked logger for verification |
| `mlflow` | `MagicMock` | Mocked MLflow for verification |

### Setup & Input Methods

| Method | Description |
|--------|-------------|
| `setup_step(step)` | Inject all test dependencies into step instance |
| `set_input_data(slot_name, data)` | Set non-file input slot data (e.g., mock clients) |
| `write_input_file(path, data)` | Write test input files (DataFrame \u2192 parquet, dict \u2192 JSON, str \u2192 text) |

### Output Reading Methods

| Method | Description |
|--------|-------------|
| `get_output_path(path)` | Get full path to output file |
| `read_output(path)` | Read output file (auto-detects format) |
| `read_output_df(path, **kwargs)` | Read output as DataFrame |
| `read_output_json(path)` | Read output as dict |

### Assertion Methods

| Method | Description |
|--------|-------------|
| `assert_output_exists(path)` | Verify file was created |
| `assert_output_not_exists(path)` | Verify file was NOT created |
| `assert_logged_metric(key, value, step=None)` | Verify MLflow metric was logged |
| `assert_logged_parameter(key, value)` | Verify MLflow parameter was logged |
| `assert_artifact_exists(path)` | Verify MLflow artifact was logged |
| `raises(exception, match=...)` | Context manager for expected errors |

### Standalone Assertion Helpers

| Helper | Description |
|--------|-------------|
| `assert_parquet_equal(expected, actual)` | Compare parquet file outputs |
| `assert_json_matches(path, expected)` | Validate JSON structure and content |
| `assert_model_loadable(path)` | Verify saved models can be loaded |

### Mock Factories

| Factory | Description |
|---------|-------------|
| `mock_bigquery_result(df, query_string=None)` | Mock BigQuery results; `.to_pandas()` / `.to_dataframe()` return the DataFrame |
| `mock_gcp_storage_client(files={})` | Mock GCS client with predefined files; supports `get_bucket()`, `blob()`, upload/download |
| `mock_mlflow_run(run_id=None, experiment_id=None, artifact_uri=None)` | Mock MLflow run context (usually not needed \u2014 `step_env.mlflow` is pre-mocked) |

## Common Patterns

### Parametrized Testing

```python
@pytest.mark.parametrize("step_env", [
    {"config": {"model": "xgboost"}, "runtime_parameters": {"country": "us"}},
    {"config": {"model": "lightgbm"}, "runtime_parameters": {"country": "de"}},
], indirect=True)
def test_multi_config(step_env):
    step = ModelTrainingStep()
    step_env.setup_step(step)
    step.run()
    step_env.assert_output_exists("model.pkl")
    step_env.assert_logged_parameter("model", step_env.config["model"])
```

### Testing with Mock Factories

```python
from aif.pyrogai.testing import mock_bigquery_result

def test_step_with_bigquery(step_env):
    mock_bq = mock_bigquery_result(pd.DataFrame({"id": [1, 2], "value": [100, 200]}))
    step_env.set_input_data("bigquery_client", mock_bq)

    step = DataGetterStep()
    step_env.setup_step(step)
    step.run()

    output_df = step_env.read_output_df("data/results.parquet")
    assert len(output_df) == 2
```

### Error Handling

```python
def test_step_error_handling(step_env):
    step = ValidatingStep()
    step_env.setup_step(step)
    with step_env.raises(ValueError, match="Invalid config"):
        step.run()
```

### Multi-Step Workflow

```python
def test_pipeline_sequence(step_env):
    # Step 1
    step1 = PreprocessStep()
    step_env.setup_step(step1)
    step1.run()

    # Pass output as input to step 2
    data = step_env.read_output_df("preprocessed.parquet")
    step_env.write_input_file("input/data.parquet", data)

    # Step 2
    step2 = ModelStep()
    step_env.setup_step(step2)
    step2.run()

    step_env.assert_output_exists("model.pkl")
```

## Migration from Manual Mocking

If your tests use manual `@patch('aif.pyrogai.pipelines...')` decorators, migrate to `step_env`:

```python
# BEFORE: fragile manual patching
@patch('aif.pyrogai.pipelines.components.environment.PlatformProvider._handle_metainfo')
@patch('aif.pyrogai.pipelines.components.environment.PlatformProvider._set_log_files')
def test_my_step(mock1, mock2):
    step = MyStep()
    step.logger = Mock()
    step.ioctx = Mock()
    step.run()

# AFTER: clean testing module
def test_my_step(step_env):
    step = MyStep()
    step_env.setup_step(step)
    step.run()
    step_env.assert_output_exists("output.parquet")
```

## Further Resources

- **Testing Skill**: See the `testing-pyrogai-steps` skill for quick-reference DO/DON'T checklist
- **Framework Reference**: `pyrogai-framework-reference.md` for core PyrogAI API
- **Patterns & Examples**: `pyrogai-patterns-examples.md` for step implementation patterns
- **Detailed API docs**: Ask the **doc-retriever** agent \u2014 it has access to `procter-gamble/de-cf-pyrogai` docs including mock factory internals, TestIoContext details, advanced configuration, and assertion implementations
