# PyrogAI Troubleshooting Guide

This guide covers common issues and solutions when working with PyrogAI, based on real framework behavior and common developer scenarios.

## Step Execution Issues

### Import and Module Errors

**Problem: `ModuleNotFoundError` when running steps**
```
ModuleNotFoundError: No module named 'my_project.steps.my_step'
```

**Solutions:**
1. Ensure PYTHONPATH includes project src directory:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
   ```

2. Verify step class path format in pipeline YAML:
   ```yaml
   steps:
     - name: my_step
       class: my_project.steps.my_step:MyStepClass  # module.path:ClassName
   ```

3. Check file and directory structure:
   ```
   src/
   ├── my_project/
   │   ├── __init__.py
   │   └── steps/
   │       ├── __init__.py
   │       └── my_step.py
   ```

**Problem: `AttributeError: 'MyStep' object has no attribute 'logger'`**

**Solution:** Ensure step properly inherits from base Step class:
```python
from aif.pyrogai.steps.step import Step

class MyStep(Step):  # Must inherit from Step
    def run(self) -> None:
        self.logger.info("This works now")
```

### Runtime Parameter Issues

**Problem: Parameters not being passed correctly**

**Debug and fix:**
```python
def run(self) -> None:
    # Debug: Print all available parameters
    self.logger.info(f"Available parameters: {list(self.runtime_parameters.keys())}")
    
    # Get parameter with proper default handling
    param_value = self.runtime_parameters.get("my_param", "default_value")
    
    # Validate parameter exists
    if "required_param" not in self.runtime_parameters:
        raise ValueError("required_param must be provided")
```

**Command line parameter passing:**
```bash
# Correct way to pass parameters
aif pipeline run --pipeline-name my_pipeline -p param1=value1 -p param2=value2

# For step testing
aif step run --step-class my_project.steps.my_step:MyStep -p test_param=test_value
```

### IoContext File Issues

**Problem: `FileNotFoundError` when accessing files**

**Debug IoContext configuration:**
```python
def run(self) -> None:
    # Debug IoContext paths
    self.logger.info(f"Local workdir: {self.ioctx.local_workdir}")
    if hasattr(self.ioctx, 'remote_workdir'):
        self.logger.info(f"Remote workdir: {self.ioctx.remote_workdir}")
    
    # Check if file exists before accessing
    input_file = self.ioctx.get_fn("input/data.csv")
    self.logger.info(f"Looking for file at: {input_file}")
    self.logger.info(f"File exists: {input_file.exists()}")
    
    # List available files in directory
    input_dir = self.ioctx.get_fn("input/")
    if input_dir.exists():
        files = list(input_dir.iterdir())
        self.logger.info(f"Available files: {files}")
```

**Problem: Permission denied when writing files**

**Solutions:**
1. Ensure output directory permissions:
   ```python
   output_file = self.ioctx.get_output_fn("results/data.csv")
   output_file.parent.mkdir(parents=True, exist_ok=True)  # Create directories
   ```

2. Check cloud storage permissions for your service principal or user account

3. For local development, ensure workspace directory is writable:
   ```yaml
   # In provider config
   details:
     workspace_dir: "/tmp/.workspace"  # Use writable directory
   ```

## Configuration Issues

### Pipeline YAML Problems

**Problem: `ValidationError` when loading pipeline**

**Common YAML syntax issues:**
```yaml
# ❌ Wrong: Missing quotes around class path with special characters
steps:
  - name: my_step
    class: my_project.steps.my-step:MyStep

# ✅ Correct: Quoted class path
steps:
  - name: my_step
    class: "my_project.steps.my-step:MyStep"

# ❌ Wrong: Incorrect indentation
steps:
- name: step1
  class: module:Class
- name: step2
    class: module:Class  # Wrong indentation

# ✅ Correct: Consistent indentation
steps:
  - name: step1
    class: module:Class
  - name: step2
    class: module:Class
```

**Problem: Circular dependencies in pipeline steps**

**Debug dependency issues:**
```python
# Check your pipeline dependencies
def debug_pipeline_dependencies(pipeline_config):
    """Debug function to visualize step dependencies."""
    steps = pipeline_config['steps']
    
    print("Step Dependencies:")
    for step in steps:
        step_name = step['name']
        dependencies = step.get('run_after', [])
        print(f"  {step_name} -> depends on: {dependencies}")
    
    # Check for circular dependencies
    # (Add topological sort logic here)
```

### Provider Configuration Issues

**Problem: Provider connection failures**

**Test provider connectivity:**
```bash
# Test specific provider
aif provider test-connection --provider-name "My Provider" --config-module my_project.config

# Validate provider configuration
aif provider validate --config-module my_project.config
```

**Debug provider secrets:**
```python
def debug_provider_setup(self) -> None:
    """Debug provider configuration and connectivity."""
    self.logger.info(f"Platform: {self.platform}")
    self.logger.info(f"Provider name: {self.provider.name}")
    self.logger.info(f"Environment: {self.environment}")
    
    # Test secret access (be careful with logging sensitive data)
    try:
        # Try to access a known secret (without logging its value)
        test_secret = self.secrets.get('test_secret_name')
        self.logger.info("Secret access: SUCCESS")
    except KeyError as e:
        self.logger.error(f"Secret access failed: {e}")
        # List available secrets (names only)
        available = list(self.secrets.keys())
        self.logger.info(f"Available secret names: {available}")
```

## Platform-Specific Issues

### Azure ML Issues

**Problem: `AuthenticationError` in Azure ML**

**Solutions:**
1. Check Azure CLI authentication:
   ```bash
   az login
   az account show  # Verify correct subscription
   ```

2. For service principal authentication, verify environment variables:
   ```bash
   echo $AZURE_CLIENT_ID
   echo $AZURE_TENANT_ID  
   # Don't echo AZURE_CLIENT_SECRET for security
   ```

3. Verify AML workspace access:
   ```python
   def test_aml_connection(self) -> None:
       """Test Azure ML connection."""
       try:
           ml_client = self.ml_client
           workspace_info = ml_client.workspaces.get(ml_client.workspace_name)
           self.logger.info(f"Connected to AML workspace: {workspace_info.name}")
           
           # Test dataset access
           datasets = ml_client.data.list()
           dataset_names = [d.name for d in datasets]
           self.logger.info(f"Available datasets: {dataset_names[:5]}")  # Show first 5
           
       except Exception as e:
           self.logger.error(f"AML connection failed: {e}")
           raise
   ```

### Databricks Issues

**Problem: Spark session not available**

**Debug Spark session setup:**
```python
def debug_spark_setup(self) -> None:
    """Debug Databricks Spark session configuration."""
    if self.platform != Platform.DBR:
        self.logger.info("Not on Databricks platform")
        return
    
    try:
        spark = self.spark_session
        self.logger.info(f"Spark version: {spark.version}")
        self.logger.info(f"Spark app name: {spark.sparkContext.appName}")
        
        # Test basic Spark functionality
        test_df = spark.range(10)
        count = test_df.count()
        self.logger.info(f"Spark test successful, count: {count}")
        
        # List available databases/tables
        databases = spark.catalog.listDatabases()
        self.logger.info(f"Available databases: {[db.name for db in databases]}")
        
    except Exception as e:
        self.logger.error(f"Spark session error: {e}")
        
        # Check if cluster configuration is correct
        provider_name = getattr(self.config.model, 'spark_session_provider_name', None)
        self.logger.info(f"Configured spark_session_provider_name: {provider_name}")
```

**Problem: DBFS file access issues**

**Debug DBFS paths:**
```python
def debug_dbfs_access(self) -> None:
    """Debug DBFS file system access."""
    if self.platform != Platform.DBR:
        return
    
    # Test DBFS paths
    test_paths = [
        "/dbfs/",
        "/dbfs/tmp/",
        "/dbfs/FileStore/",
    ]
    
    for path in test_paths:
        try:
            path_obj = Path(path)
            exists = path_obj.exists()
            self.logger.info(f"Path {path} exists: {exists}")
            
            if exists and path_obj.is_dir():
                contents = list(path_obj.iterdir())
                self.logger.info(f"  Contents count: {len(contents)}")
        except Exception as e:
            self.logger.error(f"Error accessing {path}: {e}")
```

### Vertex AI Issues

**Problem: Google Cloud authentication failures**

**Debug GCP authentication:**
```python
def debug_gcp_setup(self) -> None:
    """Debug Google Cloud Platform setup."""
    if self.platform != Platform.VERTEX:
        return
    
    # Check environment variables
    import os
    gcp_vars = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GOOGLE_CLOUD_PROJECT',
    ]
    
    for var in gcp_vars:
        value = os.environ.get(var)
        if value:
            self.logger.info(f"{var}: {value}")
        else:
            self.logger.warning(f"{var}: Not set")
    
    # Test GCP connectivity
    try:
        from google.auth import default
        credentials, project = default()
        self.logger.info(f"GCP project: {project}")
        self.logger.info(f"Credentials type: {type(credentials).__name__}")
    except Exception as e:
        self.logger.error(f"GCP authentication error: {e}")
```

## MLflow Integration Issues

**Problem: MLflow tracking not working**

**Debug MLflow configuration:**
```python
def debug_mlflow_setup(self) -> None:
    """Debug MLflow tracking setup."""
    try:
        # Check MLflow configuration
        tracking_uri = self.mlflow.get_tracking_uri()
        self.logger.info(f"MLflow tracking URI: {tracking_uri}")
        
        # Check experiment
        if self.experiment_name:
            experiment = self.mlflow.get_experiment_by_name(self.experiment_name)
            self.logger.info(f"Experiment ID: {experiment.experiment_id}")
            self.logger.info(f"Experiment name: {experiment.name}")
        else:
            self.logger.warning("No experiment name configured")
        
        # Test logging
        self.mlflow.log_param("debug_test", "test_value")
        self.logger.info("MLflow logging test successful")
        
    except Exception as e:
        self.logger.error(f"MLflow setup error: {e}")
        
        # Check environment variables
        import os
        mlflow_vars = [
            'MLFLOW_TRACKING_URI',
            'MLFLOW_EXPERIMENT_NAME', 
            'MLFLOW_EXPERIMENT_ID',
            'MLFLOW_RUN_ID',
        ]
        
        for var in mlflow_vars:
            value = os.environ.get(var)
            self.logger.debug(f"{var}: {value or 'Not set'}")
```

**Problem: MLflow artifacts not saving**

**Debug artifact logging:**
```python
def debug_artifact_logging(self) -> None:
    """Debug MLflow artifact logging."""
    try:
        # Create test artifact
        test_file = self.ioctx.get_output_fn("test_artifact.txt")
        test_file.write_text("This is a test artifact")
        
        # Log artifact
        self.mlflow.log_artifact(str(test_file))
        self.logger.info(f"Successfully logged artifact: {test_file}")
        
        # List run artifacts
        run_id = self.mlflow.active_run().info.run_id
        artifacts = self.mlflow.list_artifacts(run_id)
        self.logger.info(f"Run artifacts: {artifacts}")
        
    except Exception as e:
        self.logger.error(f"Artifact logging error: {e}")
```

## Performance and Resource Issues

### Memory Issues

**Problem: Out of memory errors**

**Debug memory usage:**
```python
import psutil
import gc

def debug_memory_usage(self) -> None:
    """Monitor memory usage during step execution."""
    process = psutil.Process()
    
    memory_info = process.memory_info()
    memory_mb = memory_info.rss / 1024 / 1024
    
    self.logger.info(f"Memory usage: {memory_mb:.2f} MB")
    self.mlflow.log_metric("memory_usage_mb", memory_mb)
    
    # Force garbage collection
    collected = gc.collect()
    self.logger.debug(f"Garbage collected: {collected} objects")

def run(self) -> None:
    """Example of memory-aware processing."""
    self.debug_memory_usage()  # Initial memory
    
    # Process data in chunks for large datasets
    chunk_size = int(self.runtime_parameters.get("chunk_size", 10000))
    
    for chunk in self.process_in_chunks(chunk_size):
        # Process chunk
        result = self.process_chunk(chunk)
        
        # Save intermediate results
        self.save_chunk_result(result)
        
        # Clean up chunk data
        del chunk, result
        gc.collect()
        
        self.debug_memory_usage()  # Monitor memory after each chunk
```

### Network and Connectivity Issues

**Problem: Proxy configuration for corporate networks**

**Configure proxy settings:**
```python
def configure_proxy(self) -> None:
    """Configure proxy settings for corporate networks."""
    import os
    
    # Get proxy from provider configuration or environment
    proxy = getattr(self.provider.details, 'default_proxy', None)
    if not proxy:
        proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    
    if proxy:
        self.logger.info(f"Using proxy: {proxy}")
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        
        # For some libraries, you might need to configure proxy differently
        # requests.get(url, proxies={'http': proxy, 'https': proxy})

def run(self) -> None:
    """Step with proxy configuration."""
    self.configure_proxy()
    
    # Use PyrogAI's proxy context manager
    with self.proxy_if_needed():
        # Network operations here will use configured proxy
        # self.download_data()
        pass
```

## Debugging Commands and Tools

### Enable Debug Logging
```bash
# Run with debug logging
aif pipeline run --pipeline-name my_pipeline --debug --config-module my_project.config

# Run specific step with debug
aif step run --step-class my_project.steps.my_step:MyStep --debug
```

### System Diagnostics
```bash
# Get PyrogAI version and dependencies
aif doctor version --json

# Check system configuration
aif doctor version

# Validate configuration files
aif pipeline validate --pipeline-name my_pipeline --config-module my_project.config
```

### Log Analysis
```python
def analyze_step_logs(log_file_path: str) -> None:
    """Analyze PyrogAI step logs for common issues."""
    with open(log_file_path, 'r') as f:
        lines = f.readlines()
    
    # Look for common error patterns
    error_patterns = [
        'ModuleNotFoundError',
        'ValidationError', 
        'ConnectionError',
        'AuthenticationError',
        'FileNotFoundError',
        'PermissionError',
    ]
    
    for i, line in enumerate(lines):
        for pattern in error_patterns:
            if pattern in line:
                print(f"Line {i+1}: Found {pattern}")
                print(f"  {line.strip()}")
                # Print context lines
                context_start = max(0, i-2)
                context_end = min(len(lines), i+3)
                for j in range(context_start, context_end):
                    if j != i:
                        print(f"  {j+1}: {lines[j].strip()}")
                print()
```

This troubleshooting guide covers the most common PyrogAI issues and provides systematic approaches to identify and resolve them. Always start with the debug logging and system diagnostics before diving into code-level debugging.

## Related Resources

- **Framework Reference**: See `pyrogai-framework-reference.md` for understanding core concepts during debugging
- **Implementation Examples**: Check `pyrogai-patterns-examples.md` for working code patterns to compare against
- **Expert Assistance**: Use the `@pyrogai` agent for interactive debugging support  
- **Specialized Debugging**: Use the `pyrogai-debugger` prompt/command for systematic troubleshooting workflows