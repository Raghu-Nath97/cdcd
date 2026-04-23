---
name: 'PyrogAI Pipeline YAML'
description: 'PyrogAI pipeline YAML configuration guidelines'
applyTo: '**/config/pipeline_*.yml'
---

# PyrogAI Pipeline Configuration Standards

## Pipeline Structure

All PyrogAI pipelines must be defined in YAML files starting with `pipeline_`:

```yaml
name: my_pipeline
experiment: my_experiment
compute: small
runtime: python39
platforms:
  - AML
  - DBR
  - Vertex
steps:
  - name: data_preparation
    class: my_project.steps.data_prep:DataPrepStep
  - name: model_training
    class: my_project.steps.train:TrainStep
    run_after:
      - data_preparation
```

## Required Fields

Every pipeline must include:
- **`name`**: Unique pipeline identifier
- **`experiment`**: MLflow experiment name
- **`steps`**: List of step definitions

## Step Configuration

Each step requires:
- **`name`**: Unique step name within pipeline
- **`class`**: Python class path in format `module.path:ClassName`

Optional step fields:
- **`run_after`**: List of prerequisite step names
- **`inputs`**: List of input slot names
- **`outputs`**: List of output slot names
- **`compute`**: Override pipeline compute
- **`runtime`**: Override pipeline runtime
- **`environment`**: Restrict to specific environments
- **`platforms`**: Restrict to specific platforms

## Platform Support

Specify target platforms explicitly:
```yaml
platforms:
  - AML      # Azure ML
  - DBR      # Databricks
  - Vertex   # Google Vertex AI
  - Local    # Local development
```

## Runtime Parameters

Define pipeline parameters with environment-specific overrides:

```yaml
params:
  batch_size: 32
  learning_rate: 0.01
  model_type: "random_forest"

env_specific_params:
  dev:
    batch_size: 16
  prod:
    batch_size: 64
    learning_rate: 0.001
```

## Scheduling Configuration

Define pipeline schedules with proper cron expressions:

```yaml
schedules:
  - name: daily_training
    cron: "0 2 * * *"  # Daily at 2 AM UTC
    paused: false
    time_zone: "UTC"
    runtime_params:
      environment: "prod"
```

## Input/Output Slots

Define data flow between steps:

```yaml
input_output_slots:
  - name: raw_data
    type: cloudfile
    path: "data/raw/{environment}/"
  - name: processed_data
    type: cloudfile
    path: "data/processed/{pipeline_name}/"
  - name: model_artifact
    type: mlflow_artifact
    artifact_name: "model"

steps:
  - name: data_prep
    class: steps.prep:PrepStep
    outputs:
      - processed_data
  - name: train_model
    class: steps.train:TrainStep
    inputs:
      - processed_data
    outputs:
      - model_artifact
```

## Compute and Runtime Configuration

Configure compute resources and Python environments:

```yaml
compute: small  # Reference to provider compute config
runtime: python39  # Reference to provider runtime config

steps:
  - name: heavy_computation
    class: steps.compute:HeavyStep
    compute: large  # Override for this step
    runtime: gpu_runtime
```

## Tags and Metadata

Add descriptive tags for organization:

```yaml
tags:
  team: "data-science"
  project: "customer-analytics" 
  criticality: "high"
  owner: "john.doe@company.com"
```

## Best Practices

### Naming Conventions
- Pipeline names: Use lowercase with underscores (`customer_churn_prediction`)
- Step names: Descriptive and sequential (`data_validation`, `feature_engineering`)
- Experiment names: Match pipeline purpose (`customer_churn_exp`)

### Dependencies
- Use `run_after` to define step dependencies
- Avoid circular dependencies
- Group related steps logically

### Environment Management
- Use `env_specific_params` for environment differences
- Test locally before deploying to higher environments
- Use meaningful parameter names

### Platform Compatibility
- Test on all target platforms during development
- Use platform restrictions sparingly
- Leverage PyrogAI's cross-platform abstractions

### Documentation
- Include comments explaining complex configurations
- Document parameter meanings and valid ranges
- Maintain README files for pipeline groups

## Pipeline Execution

For full CLI options for `aif pipeline run` and `aif pipeline notebook`, use `--help` or query `search_aif_documentation` via `@doc-retriever`.

```bash
# Basic pipeline execution
aif pipeline run --pipelines my_pipeline --config-module my_project.config

# With platform, environment, and parameters
aif pipeline run --pipelines my_pipeline --platform AML --environment prod \
  -p batch_size=64 -t team=data-science

# Generate interactive notebook
aif pipeline notebook --pipelines my_pipeline --config-module my_project.config

# Validate pipeline configuration
aif pipeline validate --pipeline-name my_pipeline --config-module my_project.config
```

## Additional Resources

For comprehensive PyrogAI pipeline development:
- Use `../agents/pyrogai.agent.md` for expert pipeline assistance
- Reference `.devagent/ai_docs/pyrogai-framework-reference.md` for configuration structure details
- Check `.devagent/ai_docs/pyrogai-patterns-examples.md` for real-world pipeline examples
- Use `../prompts/pyrogai-config-generator.prompt.md` to generate new configurations