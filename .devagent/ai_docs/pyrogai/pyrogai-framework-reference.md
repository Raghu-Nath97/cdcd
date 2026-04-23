# PyrogAI Framework Reference

This document provides comprehensive reference information for PyrogAI framework development, extracted from the actual source code to ensure accuracy and completeness.

## CLI Help Discovery

**When working with PyrogAI CLI commands, ALWAYS use the `--help` flag when uncertain.** This is your first troubleshooting step and primary resource for discovering available options.

### Essential Help Commands

```bash
# Discover all step-related commands
aif step --help

# Get detailed options for specific step commands
aif step new --help      # Creating new steps
aif step run --help      # Running steps locally
aif step test --help     # Testing steps

# Discover all pipeline-related commands
aif pipeline --help

# Get detailed options for specific pipeline commands
aif pipeline run --help       # Executing pipelines
aif pipeline notebook --help  # Generating notebooks
aif pipeline publish --help   # Publishing to platforms

# Main CLI help
aif --help               # See all available command groups
```

### Why Use --help First?

- **Always current**: Reflects your installed PyrogAI version
- **Comprehensive**: Shows all options, including platform-specific ones
- **Quick reference**: Faster than searching documentation
- **Validates syntax**: Confirms exact flag names and formats

**Best Practice**: Before constructing complex CLI commands or asking about options, check `--help` first. If the help output doesn't clarify your question, then consult this reference or ask for assistance.

## Framework Architecture Overview

PyrogAI is P&G's AI Factory solution for building platform-agnostic machine learning pipelines that can run across multiple cloud platforms:

- **Azure ML (AML)**: Microsoft's cloud ML platform
- **Databricks (DBR)**: Apache Spark-based analytics platform  
- **Vertex AI**: Google Cloud's ML platform
- **Local**: Development and testing environment

## Core Components

### Step Base Class

All PyrogAI steps inherit from the abstract `Step` base class located in `aif.pyrogai.steps.step`:

```python
from aif.pyrogai.steps.step import Step

class MyStep(Step):
    def run(self) -> None:
        """Abstract method - must be implemented by all steps."""
        pass
```

### Key Step Attributes

The Step class provides these essential attributes for cross-platform development:

| Attribute | Type | Description |
|-----------|------|-------------|
| `self.logger` | Logger | Platform-aware logging system |
| `self.runtime_parameters` | dict | Runtime parameters passed to pipeline |
| `self.secrets` | SecretManager | Cross-platform secret access |
| `self.ioctx` | IoContext | File system abstraction layer |
| `self.mlflow` | MLflowModule | MLflow tracking integration |
| `self.config` | ConfigModel | Step configuration access |
| `self.pipeline` | PipelineModel | Current pipeline information |
| `self.provider` | ProviderConfig | Current platform provider config |
| `self.platform` | Platform | Current execution platform enum |
| `self.environment` | str | Current environment (dev/stg/prod) |

### Platform Detection

Use the Platform enum from `aif.pyrogai.const` for platform-specific code:

```python
from aif.pyrogai.const import Platform

# Spark session is cross-platform when configured
# Works on: DBR (default), AML, Local (requires spark_session_provider_name in config.json)
df = self.spark_session.read.table("samples.nyctaxi.trips")
result = self.spark_session.sql("SELECT COUNT(*) FROM my_table")
parquet_df = self.spark_session.read.parquet("path/to/data.parquet")

# Platform-specific code still needs checks
if self.platform == Platform.DBR:
    # Databricks-specific APIs (dbutils is DBR-only)
    scopes = self.spark_session.dbutils.secrets.listScopes()
elif self.platform == Platform.AML:
    # Azure ML-specific code
    dataset = self.ml_client.data.get("dataset_name", version="1")
elif self.platform == Platform.VERTEX:
    # Vertex AI-specific code
    pass
elif self.platform == Platform.LOCAL:
    # Local development code
    pass
```

## Testing Module (v1.8.0.post14+)

PyrogAI 1.8.0.post14 introduced `aif.pyrogai.testing` — a standardized testing module with zero manual patching via `step_env` fixture and built-in mock factories.

**See `pyrogai-testing-guide.md` for full API reference, patterns, and migration guide.**

## IoContext File Operations

PyrogAI's IoContext provides platform-agnostic file operations:

### Reading Files
```python
# Get input file path
input_file = self.ioctx.get_fn("input/data.csv")
with open(input_file, 'r') as f:
    data = f.read()

# List files in directory
for file_path in self.ioctx.get_fns("input/*.csv"):
    process_file(file_path)
```

### Writing Files  
```python
# Get output file path
output_file = self.ioctx.get_output_fn("output/results.csv")
with open(output_file, 'w') as f:
    f.write(processed_data)

# Create output directory
output_dir = self.ioctx.get_output_fn("models/")
output_dir.mkdir(parents=True, exist_ok=True)
```

## MLflow Integration

PyrogAI provides built-in MLflow integration for experiment tracking:

### Logging Parameters and Metrics
```python
def run(self) -> None:
    # Log parameters
    self.mlflow.log_param("learning_rate", 0.01)
    self.mlflow.log_param("batch_size", 32)
    
    # Log metrics
    self.mlflow.log_metric("accuracy", 0.95)
    self.mlflow.log_metric("loss", 0.05)
    
    # Log artifacts
    model_path = self.ioctx.get_output_fn("model.pkl")
    self.mlflow.log_artifact(str(model_path))
```

### Experiment Management
```python
# Access experiment information
experiment_id = self.experiment_id
experiment_name = self.experiment_name

# Get MLflow run information  
run_id = self.run_id
run_timestamp = self.run_timestamp
```

## Pipeline Configuration Structure

### Pipeline YAML Structure
```yaml
name: pipeline_name              # Required: Unique pipeline identifier
experiment: experiment_name      # Required: MLflow experiment name
compute: small                   # Optional: Default compute resource
runtime: python39               # Optional: Default runtime environment
platforms:                     # Optional: Target platforms
  - AML
  - DBR  
  - Vertex
  - Local

steps:                          # Required: Step definitions
  - name: step_name             # Required: Unique step name
    class: module.path:ClassName # Required: Step class path
    run_after:                  # Optional: Dependencies
      - previous_step
    inputs:                     # Optional: Input slots
      - input_slot_name
    outputs:                    # Optional: Output slots  
      - output_slot_name
    compute: large              # Optional: Override compute
    runtime: gpu_runtime        # Optional: Override runtime

params:                         # Optional: Pipeline parameters
  param_name: param_value

env_specific_params:            # Optional: Environment overrides
  dev:
    param_name: dev_value
  prod:
    param_name: prod_value

schedules:                      # Optional: Schedule definitions
  - name: schedule_name
    cron: "0 2 * * *"          # Cron expression
    paused: false
    runtime_params:
      param_name: value

tags:                          # Optional: Pipeline tags
  team: team_name
  owner: owner_email
```

### Provider Configuration Structure

#### Azure ML Provider
```yaml
name: AML Provider
platform: AML
environment: [dev, stg, prod]
details:
  subscription_id: subscription_id
  resource_group: resource_group  
  workspace_name: workspace_name
  keyvault_name: keyvault_name
  storage_account: storage_account
  container_name: container_name
computes:
  small:
    size: Standard_D2s_v3
    min_instances: 0
    max_instances: 2
runtimes:
  python39:
    python_version: "3.9"
    requirements_files: requirements.txt
```

#### Databricks Provider
```yaml
name: DBR Provider  
platform: DBR
environment: [dev, stg, prod]
details:
  host: databricks_host
  keyvault: keyvault_name
  secret_scope: secret_scope
computes:
  small:
    new_cluster:
      spark_version: "13.3.x-scala2.12"
      node_type_id: Standard_D3_v2
      num_workers: 2
```

## CLI Quick Reference

For detailed CLI options, use `--help` or query `search_aif_documentation` via `@doc-retriever`.

```bash
# Step commands
aif step new -f my_step                             # Create new step
aif step run --pipeline-name X --step-name Y        # Run step locally
aif step run ... --debug --dry-run                  # Debug/test mode

# Pipeline commands
aif pipeline run --pipelines X --config-module Y    # Run pipeline
aif pipeline notebook --pipelines X --config-module Y  # Generate notebook
aif pipeline validate --pipeline-name X             # Validate config

# Provider commands
aif provider new --platform AML --provider-name X   # Create provider
aif provider validate --config-module Y             # Validate provider
```

## Common Patterns and Best Practices

### Error Handling
```python
def run(self) -> None:
    try:
        # Step logic here
        self.logger.info("Processing started")
        result = self.process_data()
        self.logger.info("Processing completed successfully")
        
    except ValueError as e:
        self.logger.error(f"Invalid input data: {e}")
        raise
    except Exception as e:
        self.logger.error(f"Unexpected error: {e}")
        raise
```

### Parameter Validation
```python
def run(self) -> None:
    # Get required parameters
    batch_size = self.runtime_parameters.get("batch_size")
    if not batch_size:
        raise ValueError("batch_size parameter is required")
    
    # Convert and validate
    try:
        batch_size = int(batch_size)
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
    except ValueError as e:
        self.logger.error(f"Invalid batch_size parameter: {e}")
        raise
```

### Hook Methods
```python
def pre_run(self) -> None:
    """Called before run() method."""
    self.logger.info("Initializing resources")
    # Setup code here

def post_run(self) -> None:
    """Called after run() method.""" 
    self.logger.info("Cleaning up resources")
    # Cleanup code here

def on_error(self, e: BaseException) -> None:
    """Called when an error occurs."""
    self.logger.error(f"Step failed: {e}")
    # Error handling code here
```

### Platform-Specific Features

#### Spark Session (Cross-Platform)

PyrogAI's Spark session works across DBR, AML, and Local platforms:

**On DBR (Databricks):**
- `self.spark_session` is automatically available
- No configuration needed

**On AML or Local:**
- Requires configuration in `config.json`:
  ```json
  {
    "spark_session_provider_name": "Your DBR Provider Name"
  }
  ```
- Connects to a configured Databricks cluster
- Requires `databricks-connect` in requirements.txt
- Needs `dbr_token` secret for authentication

**Usage (all platforms):**
```python
# Works on DBR, AML, and Local (when configured)
df = self.spark_session.read.table("samples.nyctaxi.trips")
df.show()

# Execute Spark SQL
result = self.spark_session.sql("SELECT COUNT(*) FROM my_table")

# DBR-specific APIs (like dbutils) still require platform check
if self.platform == Platform.DBR:
    scopes = self.spark_session.dbutils.secrets.listScopes()
```

**Configuration Requirements (AML/Local):**
1. Active DBR cluster with Unity Catalog
2. Cluster ID configured in provider's `existing_cluster_mapping`
3. Provider name set in `config.json` as `spark_session_provider_name`
4. **Authentication** (when running `aif pipeline run/publish` with DBR cluster):
   - **Recommended**: Service Principal OAuth authentication (use `--dbr-use-service-principal` flag)
     - Requires AZURE_CLIENT_ID/SECRET in environment variables or Key Vault
     - Enforces OAuth-only authentication for enhanced security
   - **Fallback** (when `--dbr-use-service-principal` not used): Automatic credential resolution in priority order:
     1. Service Principal OAuth from environment variables
     2. Service Principal OAuth from secret.json
     3. Personal Access Token (PAT) from secret.json as `dbr_token` (legacy)
     4. Azure CLI credentials (az login)

#### Azure ML Client
```python
# Access AML client (AML platform or configured locally)
if self.platform in [Platform.AML, Platform.LOCAL]:
    dataset = self.ml_client.data.get("dataset_name", version="latest")
    df = pd.read_csv(dataset.path)
```

## Input/Output Slots

Define data flow between pipeline steps using I/O slots:

### Slot Types
- **`cloudfile`**: Cloud storage files (Azure Blob, ADLS, GCS, DBFS)  
- **`mlflow_artifact`**: MLflow artifacts
- **`delta_table`**: Delta Lake tables
- **`aml_asset`**: Azure ML datasets
- **`vertex_artifact`**: Vertex AI artifacts

### Slot Configuration
```yaml
input_output_slots:
  - name: raw_data
    type: cloudfile  
    path: "data/raw/{environment}/"
    
  - name: model_artifact
    type: mlflow_artifact
    artifact_name: "model"
```

### Using Slots in Steps
```python
def run(self) -> None:
    # Read from input slot
    input_data = self.inputs["raw_data"].read()
    
    # Process data
    processed_data = self.process(input_data)
    
    # Write to output slot
    self.outputs["processed_data"].write(processed_data)
```

## Debugging and Troubleshooting

### Enable Debug Logging
```bash
aif pipeline run --pipeline-name my_pipeline --debug --config-module my_project.config
```

### Common Issues
1. **Import Errors**: Check PYTHONPATH includes project src directory
2. **Configuration Errors**: Validate YAML syntax and required fields
3. **Platform Connectivity**: Test provider connections and credentials  
4. **MLflow Issues**: Check experiment name and tracking URI configuration
5. **File Access**: Verify IoContext paths and cloud storage permissions

### System Information
```bash
# Get PyrogAI version and dependencies
aif doctor version --json

# Check system configuration
aif doctor version
```

This reference covers the essential PyrogAI framework concepts and patterns needed for effective development and troubleshooting.

## Related Resources

- **Practical Examples**: See `pyrogai-patterns-examples.md` for real-world implementation patterns
- **Troubleshooting**: Use `pyrogai-troubleshooting-guide.md` for systematic debugging approaches  
- **Expert Assistance**: Use the `@pyrogai` agent for comprehensive development support
- **Code Generation**: Use PyrogAI prompts/commands (e.g., `pyrogai-step-generator`) for specific tasks