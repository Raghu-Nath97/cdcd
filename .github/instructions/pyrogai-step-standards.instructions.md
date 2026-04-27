---
name: 'PyrogAI Step Development'
description: 'PyrogAI step development standards and best practices'
applyTo: 'src/**/steps/**/*.py'
---

# PyrogAI Step Development Guidelines

## CLI Help Discovery

**When uncertain about PyrogAI CLI commands, ALWAYS use the `--help` flag first.** This is your primary resource for discovering available options and understanding command usage.

```bash
# Discover step subcommands
aif step --help

# Learn about creating new steps
aif step new --help

# Understand step execution options
aif step run --help

# Explore pipeline commands
aif pipeline --help

# Pipeline execution options
aif pipeline run --help

# Notebook generation options
aif pipeline notebook --help
```

**Best Practice**: Before asking about command options or generating complex CLI commands, check the built-in help. It's always up-to-date with the installed version.

## Creating New Steps with CLI

**Use `aif step new` to generate step boilerplate.** This is the recommended way to create new PyrogAI steps, ensuring consistent structure and best practices.

### Basic Step Creation

```bash
# Create step with prompts for class name
aif step new -f my_step

# Create step with explicit class name
aif step new -f data_processor --class-name DataProcessorStep

# Use default class name (derived from file name)
aif step new -f my_step --use-default-class-name
```

### Step Creation Options

- **`--file-name` / `-f`** (required): File name for the step module (without .py extension)
- **`--class-name`**: Name of the step class (optional, prompted if not provided)
- **`--config-module`**: Python module containing project config
- **`--use-default-class-name`**: Skip prompt and use auto-generated class name from file name
- **`--force`**: Override existing step file without prompting

### Advanced Examples

```bash
# Create step with config module specified
aif step new -f feature_engineering \
  --class-name FeatureEngineeringStep \
  --config-module my_project.config

# Force overwrite existing step
aif step new -f existing_step --force

# Create multiple steps quickly with default names
aif step new -f data_validation --use-default-class-name
aif step new -f model_training --use-default-class-name
aif step new -f model_evaluation --use-default-class-name
```

### Recommended Workflow

1. **Generate step boilerplate**: Use `aif step new` to create the file structure
2. **Review generated code**: Check the created file and understand the template
3. **Customize implementation**: Add your business logic to the `run()` method
4. **Test locally**: Use `aif step run` to validate (see Step Execution section)
5. **Iterate**: Refine logic and test until step works correctly

**Important**: The CLI generates production-ready step templates with proper imports, logging, error handling, and PyrogAI patterns already in place. Start with CLI generation rather than manual code creation.

## Step Execution

Test steps locally with `aif step run`. For full CLI options and examples, run `aif step run --help` or use `@doc-retriever` to query `search_aif_documentation`.

```bash
# Basic step run
aif step run --pipeline-name my_pipeline --step-name my_step --config-module my_project.config

# With debug and runtime parameters
aif step run --pipeline-name my_pipeline --step-name my_step \
  --config-module my_project.config --debug -p batch_size=64
```

## Step Class Structure

All PyrogAI steps must inherit from the base `Step` class and implement the abstract `run()` method:

```python
from aif.pyrogai.steps.step import Step

class MyStep(Step):
    def run(self) -> None:
        """Implement your step logic here."""
        pass
```

## Essential Step Attributes

Use these built-in step attributes for platform-agnostic development:

- **`self.logger`**: Platform-aware logging (use instead of print)
- **`self.runtime_parameters`**: Dict of runtime parameters
- **`self.secrets`**: Platform-agnostic secret access
- **`self.ioctx`**: IoContext for file operations
- **`self.mlflow`**: MLflow tracking integration
- **`self.config`**: Step configuration access
- **`self.pipeline`**: Current pipeline information

## Logging Best Practices

Always use the step logger for consistent platform behavior:

```python
def run(self) -> None:
    self.logger.info("Step started")
    self.logger.debug("Debug information")
    self.logger.warning("Warning message")
    self.logger.error("Error occurred")
```

## File Operations

Use IoContext for platform-agnostic file operations:

```python
def run(self) -> None:
    # Read files
    input_file = self.ioctx.get_fn("input/data.csv")
    with open(input_file, 'r') as f:
        data = f.read()
    
    # Write files  
    output_file = self.ioctx.get_output_fn("output/results.csv")
    with open(output_file, 'w') as f:
        f.write(data)
```

## MLflow Integration

Leverage built-in MLflow for experiment tracking:

```python
def run(self) -> None:
    # Log parameters
    self.mlflow.log_param("learning_rate", 0.01)
    
    # Log metrics
    self.mlflow.log_metric("accuracy", 0.95)
    
    # Log artifacts
    self.mlflow.log_artifact("model.pkl")
```

## Error Handling

Implement proper error handling with informative messages:

```python
def run(self) -> None:
    try:
        # Your step logic
        pass
    except Exception as e:
        self.logger.error(f"Step failed: {str(e)}")
        raise
```

## Runtime Parameters

Access and validate runtime parameters:

```python
def run(self) -> None:
    # Get required parameters
    batch_size = int(self.runtime_parameters.get("batch_size", 32))
    
    # Validate parameters
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
```

## Platform-Specific Code

Spark session is cross-platform when configured:
- **DBR**: Works by default
- **AML/Local**: Requires `spark_session_provider_name` in config.json

```python
# Cross-platform Spark operations - no platform check needed
df = self.spark_session.read.table("samples.nyctaxi.trips")
result = self.spark_session.sql("SELECT * FROM my_table WHERE date > '2025-01-01'")
csv_df = self.spark_session.read.csv("path/to/file.csv", header=True)
```

When platform-specific code is necessary, check the platform:

```python
from aif.pyrogai.const import Platform

def run(self) -> None:
    # Cross-platform Spark operations work everywhere
    df = self.spark_session.read.table("my_table")
    filtered = self.spark_session.sql("SELECT * FROM my_table LIMIT 100")
    
    # DBR-specific APIs still need platform check
    if self.platform == Platform.DBR:
        # dbutils is Databricks-only
        scopes = self.spark_session.dbutils.secrets.listScopes()
    elif self.platform == Platform.AML:
        # Azure ML specific code
        dataset = self.ml_client.data.get("my_dataset", version="1")
```

## Hook Methods

Utilize pre/post execution hooks when needed:

```python
def pre_run(self) -> None:
    """Called before run() method."""
    self.logger.info("Initializing step")

def post_run(self) -> None:
    """Called after run() method."""
    self.logger.info("Step completed")

def on_error(self, e: BaseException) -> None:
    """Called when an error occurs."""
    self.logger.error(f"Step failed with error: {e}")
```

## Input/Output Slots

Use I/O slots for data flow between steps:

```python
def run(self) -> None:
    # Read from input slot
    input_data = self.inputs["my_input"].read()
    
    # Process data
    result = process_data(input_data)
    
    # Write to output slot
    self.outputs["my_output"].write(result)
```

## Avoid Common Anti-Patterns

- ❌ Don't use `print()` - use `self.logger`
- ❌ Don't hardcode file paths - use `self.ioctx`
- ❌ Don't access secrets directly - use `self.secrets`
- ❌ Don't ignore runtime parameters - use `self.runtime_parameters`
- ❌ Don't skip error handling - implement proper exception management

## Additional Resources

For comprehensive PyrogAI development support:
- Use `../agents/pyrogai.agent.md` for expert assistance
- Reference `.devagent/ai_docs/pyrogai-framework-reference.md` for complete API documentation
- Check `.devagent/ai_docs/pyrogai-patterns-examples.md` for implementation examples
- **For testing steps**: See `pyrogai-testing.instructions.md` for the testing module (`aif.pyrogai.testing`) v1.8.0.post14+
- Use `../prompts/pyrogai-step-generator.prompt.md` to generate new steps