---
name: 'PyrogAI Step Testing'
description: 'PyrogAI step testing standards using aif.pyrogai.testing module (v1.8.0.post14+)'
applyTo: '**/tests/**/*test*.py'
---

# PyrogAI Step Testing Standards

> Requires PyrogAI >= 1.8.0.post14. For older versions, ask the **doc-retriever** agent for legacy testing patterns.

## Core Rule

**ALWAYS use `aif.pyrogai.testing` for PyrogAI step tests.** Never manually patch `PlatformProvider` or internal framework components.

## Required Setup

```python
# conftest.py
pytest_plugins = ['aif.pyrogai.testing.fixtures']
```

## Standard Test Pattern

```python
def test_my_step(step_env):
    # 1. Arrange: configure environment and inputs
    step_env.config = {"threshold": 0.85}
    step_env.write_input_file("data/input.parquet", input_df)

    # 2. Act: create step, setup, run
    step = MyStep()
    step_env.setup_step(step)
    step.run()

    # 3. Assert: verify outputs
    step_env.assert_output_exists("data/output.parquet")
    output_df = step_env.read_output_df("data/output.parquet")
    assert len(output_df) == expected_count
```

## DO / DON'T

### DO

- Use `step_env` fixture for all PyrogAI step tests
- Call `step_env.setup_step(step)` before `step.run()`
- Use `write_input_file()` for test data (supports DataFrame, dict, str)
- Use built-in assertions: `assert_output_exists()`, `assert_logged_metric()`, etc.
- Use mock factories: `mock_bigquery_result()`, `mock_gcp_storage_client()`, `mock_mlflow_run()`
- Test one behavior per test function
- Use `@pytest.mark.parametrize` with `indirect=True` for multiple configs
- Use `step_env.raises(Exception, match="...")` for error cases

### DON'T

- Manually patch `PlatformProvider` or internal framework components
- Use `unittest.mock` for framework-level mocking
- Create custom IoContext mocks (use `TestIoContext`)
- Hardcode file paths (use `step_env.get_output_path()`)
- Write tests without assertions
- Skip cleanup (fixtures handle this automatically)
- Use `min_value` or `max_value` with `assert_logged_metric` (correct signature: `key, value, step=None`)

## Essential Patterns

### With Configuration and Secrets

```python
def test_step_with_config(step_env):
    step_env.config = {"model_type": "xgboost", "n_estimators": 100}
    step_env.runtime_parameters = {"batch_size": 1000}
    step_env.secrets = {"api_key": "test_key_12345"}

    step = ModelTrainingStep()
    step_env.setup_step(step)
    step.run()

    step_env.assert_output_exists("model.pkl")
    step_env.assert_logged_metric("accuracy", 0.95)
    step_env.assert_logged_parameter("model_type", "xgboost")
```

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

### Error Handling

```python
def test_step_raises_on_bad_config(step_env):
    step_env.config = {"invalid_param": True}
    step = ValidatingStep()
    step_env.setup_step(step)
    with step_env.raises(ValueError, match="Invalid configuration"):
        step.run()
```

### Mock Factories

```python
from aif.pyrogai.testing import mock_bigquery_result, mock_gcp_storage_client

def test_step_with_bigquery(step_env):
    mock_bq = mock_bigquery_result(pd.DataFrame({"id": [1, 2]}))
    step_env.set_input_data("bq_client", mock_bq)

    step = DataStep()
    step_env.setup_step(step)
    step.run()
```

## Assertion Reference

| Method | Signature | Description |
|--------|-----------|-------------|
| `assert_output_exists` | `(path)` | File was created |
| `assert_output_not_exists` | `(path)` | File was NOT created |
| `assert_logged_metric` | `(key, value, step=None)` | MLflow metric logged |
| `assert_logged_parameter` | `(key, value)` | MLflow parameter logged |
| `assert_artifact_exists` | `(path)` | MLflow artifact logged |
| `raises` | `(exception, match=...)` | Expected error raised |

## Further Resources

- **Testing Guide**: `.devagent/ai_docs/pyrogai/pyrogai-testing-guide.md`
- **Testing Skill**: `testing-pyrogai-steps` skill for quick-reference checklist
- **Detailed API docs**: Ask the **doc-retriever** agent for mock factory internals, TestIoContext details, or advanced patterns
