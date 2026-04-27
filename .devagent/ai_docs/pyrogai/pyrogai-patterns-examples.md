# PyrogAI Common Patterns and Examples

This document provides real-world examples and common patterns extracted from the PyrogAI codebase to guide developers in implementing effective ML pipeline solutions.

## Step Implementation Patterns

### Data Processing Step Pattern
```python
from aif.pyrogai.steps.step import Step
import pandas as pd
from pathlib import Path


class DataProcessingStep(Step):
    """Template for data processing steps."""

    def run(self) -> None:
        """Process input data and save results."""
        self.logger.info("Starting data processing")
        
        # Get parameters with defaults
        chunk_size = int(self.runtime_parameters.get("chunk_size", 10000))
        output_format = self.runtime_parameters.get("output_format", "csv")
        
        # Validate parameters
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        
        # Process data
        input_files = list(self.ioctx.get_fns("input/*.csv"))
        self.logger.info(f"Found {len(input_files)} input files")
        
        processed_data = []
        for file_path in input_files:
            self.logger.debug(f"Processing {file_path}")
            df = pd.read_csv(file_path, chunksize=chunk_size)
            
            for chunk in df:
                processed_chunk = self._process_chunk(chunk)
                processed_data.append(processed_chunk)
        
        # Combine and save results
        final_df = pd.concat(processed_data, ignore_index=True)
        output_path = self.ioctx.get_output_fn(f"processed_data.{output_format}")
        
        if output_format == "csv":
            final_df.to_csv(output_path, index=False)
        elif output_format == "parquet":
            final_df.to_parquet(output_path)
        
        # Log metrics
        self.mlflow.log_param("chunk_size", chunk_size)
        self.mlflow.log_param("output_format", output_format)
        self.mlflow.log_metric("rows_processed", len(final_df))
        self.mlflow.log_metric("files_processed", len(input_files))
        
        self.logger.info(f"Processed {len(final_df)} rows from {len(input_files)} files")

    def _process_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """Process individual data chunk."""
        # Add your processing logic here
        # Example: remove duplicates, handle missing values, etc.
        chunk = chunk.drop_duplicates()
        chunk = chunk.dropna()
        return chunk
```

### Model Training Step Pattern
```python
from aif.pyrogai.steps.step import Step
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


class ModelTrainingStep(Step):
    """Template for model training steps."""

    def run(self) -> None:
        """Train and save machine learning model."""
        self.logger.info("Starting model training")
        
        # Get hyperparameters
        n_estimators = int(self.runtime_parameters.get("n_estimators", 100))
        max_depth = int(self.runtime_parameters.get("max_depth", 10))
        test_size = float(self.runtime_parameters.get("test_size", 0.2))
        random_state = int(self.runtime_parameters.get("random_state", 42))
        
        # Load training data
        data_path = self.ioctx.get_fn("input/training_data.csv")
        df = pd.read_csv(data_path)
        
        # Prepare features and target
        target_column = self.runtime_parameters.get("target_column", "target")
        feature_columns = [col for col in df.columns if col != target_column]
        
        X = df[feature_columns]
        y = df[target_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        
        self.logger.info(f"Training model with {len(X_train)} samples")
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.logger.info(f"Model accuracy: {accuracy:.4f}")
        
        # Save model
        model_path = self.ioctx.get_output_fn("model.pkl")
        joblib.dump(model, model_path)
        
        # Save evaluation report
        report = classification_report(y_test, y_pred, output_dict=True)
        report_path = self.ioctx.get_output_fn("evaluation_report.json")
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Log to MLflow
        self.mlflow.log_param("n_estimators", n_estimators)
        self.mlflow.log_param("max_depth", max_depth)
        self.mlflow.log_param("test_size", test_size)
        self.mlflow.log_param("n_features", len(feature_columns))
        self.mlflow.log_param("n_train_samples", len(X_train))
        
        self.mlflow.log_metric("accuracy", accuracy)
        self.mlflow.log_metric("precision", report["macro avg"]["precision"])
        self.mlflow.log_metric("recall", report["macro avg"]["recall"])
        self.mlflow.log_metric("f1_score", report["macro avg"]["f1-score"])
        
        self.mlflow.log_artifact(str(model_path))
        self.mlflow.log_artifact(str(report_path))
        
        self.logger.info("Model training completed successfully")
```

### Platform-Specific Data Access Pattern
```python
from aif.pyrogai.steps.step import Step
from aif.pyrogai.const import Platform
import pandas as pd


class DataAccessStep(Step):
    """Template for platform-specific data access."""

    def run(self) -> None:
        """Access data using platform-specific methods."""
        self.logger.info(f"Accessing data on platform: {self.platform}")
        
        if self.platform == Platform.DBR:
            df = self._read_from_databricks()
        elif self.platform == Platform.AML:
            df = self._read_from_azure_ml()
        elif self.platform == Platform.VERTEX:
            df = self._read_from_vertex()
        else:
            df = self._read_from_files()
        
        self.logger.info(f"Loaded {len(df)} rows")
        
        # Save processed data
        output_path = self.ioctx.get_output_fn("processed_data.csv")
        df.to_csv(output_path, index=False)
        
        # Log metrics
        self.mlflow.log_metric("rows_loaded", len(df))
        self.mlflow.log_metric("columns_count", len(df.columns))

    def _read_from_databricks(self) -> pd.DataFrame:
        """Read data from Databricks using Spark.
        
        Can be configured to work on Platform Providers DBR, AML and Local
        """
        table_name = self.runtime_parameters.get("table_name", "default.sample_table")
        
        spark_df = self.spark_session.table(table_name)
        
        # Convert to Pandas (be careful with large datasets)
        df = spark_df.toPandas()
        
        self.logger.info(f"Read {len(df)} rows from Databricks table: {table_name}")
        return df

    def _read_from_azure_ml(self) -> pd.DataFrame:
        """Read data from Azure ML dataset."""
        dataset_name = self.runtime_parameters.get("dataset_name", "sample_dataset")
        dataset_version = self.runtime_parameters.get("dataset_version", "latest")
        
        dataset = self.ml_client.data.get(dataset_name, version=dataset_version)
        df = pd.read_csv(dataset.path)
        
        self.logger.info(f"Read {len(df)} rows from AML dataset: {dataset_name}:{dataset_version}")
        return df

    def _read_from_vertex(self) -> pd.DataFrame:
        """Read data from Vertex AI / BigQuery."""
        # For Vertex AI, typically read from BigQuery or GCS
        table_name = self.runtime_parameters.get("bq_table", "project.dataset.table")
        
        # Using BigQuery client (requires google-cloud-bigquery)
        from google.cloud import bigquery
        
        client = bigquery.Client()
        query = f"SELECT * FROM `{table_name}`"
        df = client.query(query).to_dataframe()
        
        self.logger.info(f"Read {len(df)} rows from BigQuery table: {table_name}")
        return df

    def _read_from_files(self) -> pd.DataFrame:
        """Read data from file system (Local/development)."""
        file_pattern = self.runtime_parameters.get("file_pattern", "input/*.csv")
        
        files = list(self.ioctx.get_fns(file_pattern))
        if not files:
            raise FileNotFoundError(f"No files found matching pattern: {file_pattern}")
        
        dataframes = []
        for file_path in files:
            df = pd.read_csv(file_path)
            dataframes.append(df)
        
        combined_df = pd.concat(dataframes, ignore_index=True)
        self.logger.info(f"Read {len(combined_df)} rows from {len(files)} files")
        return combined_df
```

## Pipeline Configuration Patterns

### Multi-Stage ML Pipeline
```yaml
name: customer_churn_prediction
experiment: customer_churn_exp
compute: small
runtime: python39

platforms:
  - AML
  - DBR
  - Local

input_output_slots:
  - name: raw_customer_data
    type: cloudfile
    path: "data/raw/customers/{environment}/"
  
  - name: processed_features
    type: cloudfile
    path: "data/processed/{pipeline_name}/features/"
    
  - name: trained_model
    type: mlflow_artifact
    artifact_name: "churn_model"
    
  - name: predictions
    type: cloudfile
    path: "data/output/{pipeline_name}/{run_id}/"

steps:
  - name: data_validation
    class: customer_churn.steps.validation:DataValidationStep
    inputs:
      - raw_customer_data
    environment:
      - dev
      - stg
      - prod
      
  - name: feature_engineering
    class: customer_churn.steps.features:FeatureEngineeringStep
    run_after:
      - data_validation
    inputs:
      - raw_customer_data
    outputs:
      - processed_features
      
  - name: model_training
    class: customer_churn.steps.training:ModelTrainingStep
    run_after:
      - feature_engineering
    inputs:
      - processed_features
    outputs:
      - trained_model
    compute: large
    
  - name: model_evaluation
    class: customer_churn.steps.evaluation:ModelEvaluationStep
    run_after:
      - model_training
    inputs:
      - processed_features
      - trained_model
      
  - name: batch_prediction
    class: customer_churn.steps.prediction:BatchPredictionStep
    run_after:
      - model_evaluation
    inputs:
      - processed_features
      - trained_model
    outputs:
      - predictions

params:
  # Data parameters
  min_transaction_count: 10
  lookback_days: 90
  
  # Model parameters
  n_estimators: 100
  max_depth: 10
  test_size: 0.2
  
  # Processing parameters
  batch_size: 10000

env_specific_params:
  dev:
    min_transaction_count: 5
    n_estimators: 50
    batch_size: 1000
  stg:
    min_transaction_count: 8
    n_estimators: 75
    batch_size: 5000
  prod:
    min_transaction_count: 10
    n_estimators: 100
    batch_size: 10000

schedules:
  - name: weekly_retrain
    cron: "0 2 * * 1"  # Monday at 2 AM
    paused: false
    time_zone: "UTC"
    runtime_params:
      full_retrain: "true"
      
  - name: daily_prediction
    cron: "0 6 * * *"  # Daily at 6 AM
    paused: false
    time_zone: "UTC"
    runtime_params:
      prediction_only: "true"

tags:
  team: "customer-analytics"
  use_case: "churn-prediction"
  criticality: "high"
  data_classification: "confidential"
```

### Hyperparameter Optimization Pipeline
```yaml
name: hyperopt_model_tuning
experiment: model_optimization_exp
compute: small
runtime: python39

steps:
  - name: prepare_hyperopt_data
    class: ml_pipeline.steps.hyperopt_prep:HyperoptDataPrepStep
    
  - name: hyperopt_search
    class: ml_pipeline.steps.hyperopt_search:HyperoptSearchStep
    run_after:
      - prepare_hyperopt_data
    compute: xlarge
    
  - name: best_model_training
    class: ml_pipeline.steps.best_model:BestModelTrainingStep
    run_after:
      - hyperopt_search

params:
  # Hyperopt parameters
  max_evals: 100
  search_space:
    n_estimators: [50, 100, 200, 500]
    max_depth: [5, 10, 15, 20]
    learning_rate: [0.01, 0.1, 0.2, 0.3]
  
  # Cross-validation
  cv_folds: 5
  scoring_metric: "f1_macro"

env_specific_params:
  dev:
    max_evals: 10
    cv_folds: 3
  stg:
    max_evals: 50
    cv_folds: 4
  prod:
    max_evals: 100
    cv_folds: 5
```

## Error Handling Patterns

### Robust Error Handling with Recovery
```python
from aif.pyrogai.steps.step import Step
import time
from typing import Optional


class RobustProcessingStep(Step):
    """Step with comprehensive error handling and retry logic."""

    def run(self) -> None:
        """Execute with error handling and recovery."""
        max_retries = int(self.runtime_parameters.get("max_retries", 3))
        retry_delay = int(self.runtime_parameters.get("retry_delay", 30))
        
        for attempt in range(max_retries):
            try:
                self._execute_main_logic()
                self.logger.info("Processing completed successfully")
                return
                
            except ConnectionError as e:
                self.logger.warning(f"Connection error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("Max retries exceeded for connection error")
                    raise
                    
            except ValueError as e:
                self.logger.error(f"Data validation error (not retryable): {e}")
                raise
                
            except Exception as e:
                self.logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("Max retries exceeded for unexpected error")
                    raise

    def _execute_main_logic(self) -> None:
        """Main processing logic that might fail."""
        # Your main processing code here
        pass

    def on_error(self, e: BaseException) -> None:
        """Handle errors with notification and cleanup."""
        self.logger.error(f"Step failed with error: {e}")
        
        # Clean up temporary resources
        self._cleanup_temp_files()
        
        # Log error metrics
        self.mlflow.log_param("error_type", type(e).__name__)
        self.mlflow.log_param("error_message", str(e))
        
        # Trigger custom notifications if needed
        if hasattr(self, 'custom_notifications_to_trigger'):
            self.custom_notifications_to_trigger["error_notification"] = True

    def _cleanup_temp_files(self) -> None:
        """Clean up temporary files on error."""
        temp_dir = self.ioctx.get_output_fn("temp/")
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)
            self.logger.info("Cleaned up temporary files")
```

## Testing Patterns

PyrogAI 1.8.0.post14+ includes a stable testing module (`aif.pyrogai.testing`) that eliminates manual patching. See `pyrogai-testing-guide.md` for comprehensive documentation.

### Step Unit Testing with step_env Fixture (Recommended)

Add to your `conftest.py`:
```python
pytest_plugins = ['aif.pyrogai.testing.fixtures']
```

```python
# tests/test_my_step.py
import pytest
import pandas as pd
from my_project.steps.my_step import MyStep


def test_step_success(step_env):
    """Test successful step execution using step_env fixture."""
    # Write test input data
    test_data = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    step_env.write_input_file("input/data.parquet", test_data)
    
    # Create and setup step
    step = MyStep()
    step_env.setup_step(step)
    
    # Execute
    step.run()
    
    # Verify outputs
    step_env.assert_output_exists("output/results.parquet")
    output_df = step_env.read_output_df("output/results.parquet")
    assert len(output_df) == 3
    
    # Verify MLflow logging
    step_env.mlflow.log_metric.assert_called()


def test_step_with_config(step_env):
    """Test step with custom configuration."""
    step_env.config["threshold"] = 0.5
    step_env.runtime_parameters["batch_size"] = 100
    
    step = MyStep()
    step_env.setup_step(step)
    step.run()


def test_step_error_handling(step_env):
    """Test expected error behavior."""
    step_env.config["invalid_param"] = True
    step = MyStep()
    step_env.setup_step(step)
    
    with step_env.raises(ValueError, match="Invalid configuration"):
        step.run()


@pytest.mark.parametrize("step_env", [
    {"config": {"model": "xgboost"}, "runtime_parameters": {"n_estimators": 100}},
    {"config": {"model": "lightgbm"}, "runtime_parameters": {"n_estimators": 200}},
], indirect=True)
def test_step_multi_config(step_env):
    """Test step with multiple configurations via parametrization."""
    step = ModelStep()
    step_env.setup_step(step)
    step.run()
    step_env.assert_output_exists("model.pkl")
```

### Testing with Context Manager

```python
from aif.pyrogai.testing import step_environment

def test_step_with_context_manager():
    """Test using context manager for explicit control."""
    with step_environment(
        config={'key': 'value'},
        runtime_parameters={'param': 'val'},
        secrets={'api_key': 'test_key'}
    ) as env:
        step = MyStep()
        env.setup_step(step)
        step.run()
        env.assert_output_exists("output.parquet")
```

### Testing with External Service Mocks

```python
from aif.pyrogai.testing import mock_bigquery_result, mock_gcp_storage_client
import pandas as pd


def test_step_with_bigquery(step_env):
    """Test step that queries BigQuery."""
    # Create mock BigQuery result
    test_data = pd.DataFrame({"customer_id": [1, 2], "value": [100, 200]})
    mock_bq = mock_bigquery_result(test_data)
    
    # Inject mock into step via input slot
    step_env.set_input_data("bigquery_client", mock_bq)
    
    step = DataGetterStep()
    step_env.setup_step(step)
    step.run()


def test_step_with_gcs(step_env):
    """Test step that reads from GCS."""
    files = {
        "data/input.csv": b"id,value\n1,10\n2,20",
        "config/settings.json": b'{"key": "value"}'
    }
    mock_gcs = mock_gcp_storage_client(files=files)
    step_env.set_input_data("storage_client", mock_gcs)
    
    step = StorageStep()
    step_env.setup_step(step)
    step.run()
```

### Multi-Step Workflow Testing

```python
def test_pipeline_sequence(step_env):
    """Test multiple steps in sequence."""
    import pandas as pd
    
    # Write initial input
    raw_data = pd.DataFrame({"raw_col": [1, 2, 3]})
    step_env.write_input_file("raw/data.parquet", raw_data)
    
    # Step 1: Preprocess
    step1 = PreprocessStep()
    step_env.setup_step(step1)
    step1.run()
    
    # Verify intermediate output and chain to next step
    processed_data = step_env.read_output_df("processed/data.parquet")
    step_env.write_input_file("input/preprocessed.parquet", processed_data)
    
    # Step 2: Model training
    step2 = ModelStep()
    step_env.setup_step(step2)
    step2.run()
    
    # Verify final output
    step_env.assert_output_exists("model/model.pkl")
    step_env.assert_logged_metric("accuracy", min_value=0.7)
```

### Integration Testing

```python
# tests/integration/test_pipeline_integration.py
import pytest
import subprocess
from pathlib import Path


class TestPipelineIntegration:
    """Integration tests for pipeline execution via CLI."""
    
    def test_local_pipeline_execution(self, tmp_path):
        """Test complete pipeline execution locally."""
        # Prepare test data
        test_data_dir = tmp_path / "input"
        test_data_dir.mkdir()
        
        test_file = test_data_dir / "test_data.csv"
        test_data = "col1,col2\n1,2\n3,4\n"
        test_file.write_text(test_data)
        
        # Run pipeline
        cmd = [
            "aif", "pipeline", "run",
            "--pipeline-name", "test_pipeline",
            "--config-module", "test_project.config",
            "--platform", "Local",
            "-p", f"input_dir={test_data_dir}",
            "-p", f"output_dir={tmp_path / 'output'}"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Verify execution
        assert result.returncode == 0, f"Pipeline failed: {result.stderr}"
        
        # Check outputs
        output_dir = tmp_path / "output"
        assert output_dir.exists()
        assert any(output_dir.iterdir())
```

These patterns provide a solid foundation for developing robust, maintainable PyrogAI pipelines while following framework best practices and conventions.

## Related Resources

- **Framework Reference**: See `pyrogai-framework-reference.md` for complete API documentation
- **Troubleshooting**: Use `pyrogai-troubleshooting-guide.md` when patterns don't work as expected
- **Expert Assistance**: Use the `@pyrogai` agent for pattern-specific guidance
- **Code Generation**: Use the `pyrogai-step-generator` prompt/command to generate steps based on these patterns