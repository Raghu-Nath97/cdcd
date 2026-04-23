---
name: testing-pyrogai-steps
description: 'Tests PyrogAI pipeline steps using aif.pyrogai.testing module. Use when writing step tests, creating test fixtures, debugging test failures, setting up conftest.py, or using mock factories for BigQuery, GCS, and MLflow.'
---

# PyrogAI Step Testing

Test PyrogAI steps using the `aif.pyrogai.testing` module (v1.8.0.post14+). This module provides zero-manual-patching testing with automatic mocking of `PlatformProvider` and all internal components.

> **Version requirement**: Requires PyrogAI >= 1.8.0.post14. For older versions, see the migration section below or ask the `doc-retriever` agent for legacy testing patterns.

## Quick Start

### 1. Configure conftest.py

```python
# conftest.py
pytest_plugins = ['aif.pyrogai.testing.fixtures']
```

### 2. Write Your First Test

```python
def test_my_step(step_env):
    step = MyStep()
    step_env.setup_step(step)
    step.run()
    step_env.assert_output_exists("output.parquet")
```

## Core Pattern: Arrange → Act → Assert

```python
import pandas as pd

def test_data_processor(step_env):
    # Arrange: set config and write input data
    step_env.config = {"threshold": 0.85}
    input_df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    step_env.write_input_file("data/input.parquet", input_df)

    # Act: create step, setup environment, run
    step = DataProcessorStep()
    step_env.setup_step(step)
    step.run()

    # Assert: verify outputs
    step_env.assert_output_exists("data/output.parquet")
    output_df = step_env.read_output_df("data/output.parquet")
    assert len(output_df) == 3
```

## StepTestEnvironment Reference

### Initialization Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config` | `dict` | `{}` | Step configuration |
| `runtime_parameters` | `dict` | `{}` | Runtime parameters |
| `secrets` | `dict` | `{}` | Secrets dictionary |
| `platform` | `str` | `"Local"` | Platform name |
| `temp_dir` | `Path` | auto | Custom temp directory |

### Key Methods

| Method | Description |
|--------|-------------|
| `setup_step(step)` | Inject all test dependencies into step |
| `write_input_file(path, data)` | Write test input (DataFrame, dict, str) |
| `set_input_data(slot, data)` | Set non-file slot data (e.g., mock clients) |
| `read_output(path)` | Read output file (auto-detects format) |
| `read_output_df(path)` | Read output as DataFrame |
| `read_output_json(path)` | Read output as dict |
| `get_output_path(path)` | Get full path to output file |
| `cleanup()` | Remove temp files (automatic with fixture) |

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

```python
from aif.pyrogai.testing import assert_parquet_equal, assert_json_matches, assert_model_loadable

assert_parquet_equal("expected.parquet", "actual.parquet")
assert_json_matches("output.json", {"key": "value"})
assert_model_loadable("model.pkl")
```

## Essential Patterns

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
```

### Context Manager (Alternative to Fixture)

```python
from aif.pyrogai.testing import step_environment

def test_with_context_manager():
    with step_environment(config={"key": "val"}) as env:
        step = MyStep()
        env.setup_step(step)
        step.run()
```

### Mock Factories

```python
from aif.pyrogai.testing import mock_bigquery_result, mock_gcp_storage_client, mock_mlflow_run

# BigQuery mock
mock_bq = mock_bigquery_result(pd.DataFrame({"id": [1, 2]}))
step_env.set_input_data("bq_client", mock_bq)
result = mock_bq.to_pandas()  # Returns the DataFrame

# GCS mock
mock_gcs = mock_gcp_storage_client(files={"data/input.csv": b"id,value\n1,10"})
bucket = mock_gcs.get_bucket("test-bucket")

# MLflow mock (usually not needed - step_env.mlflow is pre-mocked)
mock_mlflow = mock_mlflow_run(run_id="test_123")
```

### Error Handling

```python
def test_step_raises_on_bad_config(step_env):
    step_env.config = {"invalid_param": True}
    step = ValidatingStep()
    step_env.setup_step(step)
    with step_env.raises(ValueError, match="Invalid configuration"):
        step.run()
```

### Secrets and Runtime Parameters

```python
def test_step_with_secrets(step_env):
    step_env.secrets = {"api_key": "test_key_12345"}
    step_env.runtime_parameters = {"batch_size": 1000}
    step = ApiStep()
    step_env.setup_step(step)
    step.run()
```

## DO / DON'T

| DO ✅ | DON'T ❌ |
|-------|---------|
| Use `step_env` fixture for most tests | Manually patch `PlatformProvider` |
| Use `write_input_file()` for test data | Create files manually with `open()` |
| Use `assert_logged_metric(key, value)` | Inspect mock call args manually |
| Use `mock_bigquery_result()` etc. | Build custom BigQuery/GCS mocks |
| Test one behavior per test function | Test multiple concerns in one test |
| Use `step_env.raises()` for errors | Use bare `pytest.raises()` for step errors |
| Register fixtures in `conftest.py` | Import fixtures in each test file |

## Common Pitfalls

- **Missing conftest.py setup**: Add `pytest_plugins = ['aif.pyrogai.testing.fixtures']`
- **Wrong `assert_logged_metric` signature**: It's `(key, value, step=None)` — there is NO `min_value` parameter
- **Forgetting `setup_step()`**: Always call `step_env.setup_step(step)` before `step.run()`
- **Using old manual patches**: If you see `@patch('aif.pyrogai.pipelines...')`, migrate to `step_env`
- **PyrogAI version too old**: Module requires `>=1.8.0.post14`; check with `pip show aif-pyrogai`

## Reference Materials

**Testing Guide**: [../../../.devagent/ai_docs/pyrogai/pyrogai-testing-guide.md](../../../.devagent/ai_docs/pyrogai/pyrogai-testing-guide.md)
**Framework Reference**: [../../../.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md](../../../.devagent/ai_docs/pyrogai/pyrogai-framework-reference.md)
**Patterns & Examples**: [../../../.devagent/ai_docs/pyrogai/pyrogai-patterns-examples.md](../../../.devagent/ai_docs/pyrogai/pyrogai-patterns-examples.md)

For detailed API docs, mock factory internals, or advanced patterns — ask the **doc-retriever** agent to look up the PyrogAI testing docs.

## Related Skills

- `developing-pyrogai-pipelines` - When building the steps you're testing
- `reviewing-python-code` - For Python standards in your test code