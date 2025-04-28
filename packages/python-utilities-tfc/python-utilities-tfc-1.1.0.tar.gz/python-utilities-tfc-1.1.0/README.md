# tf_utils.py

A Python utility module for advanced management and automation of Terraform Cloud workspaces and state files.

## Features

- **State File Filtering:**  
  Clean and filter Terraform state files by resource/module prefixes.

- **Terraform Cloud API Automation:**  
  - Download/upload state files.
  - Lock/unlock workspaces.
  - Trigger, monitor, and manage runs (cancel, discard, apply).
  - Manage workspace variables.
  - Retrieve run outputs and plan summaries.

- **Logging:**  
  Consistent, timestamped logging for all operations.

## Usage

### 1. Setup

Install dependencies:

```bash
pip3 install requests
pip3 install python-utilities-tfc
```

Import the module in your Python script:

```python
from python_utilities_tfc import tf_utils
```

```bash
export TERRAFORM_CLOUD_TOKEN="your-token"
export TERRAFORM_ORG_NAME="your-org-name"
```

### 2. Example Operations

#### Clean a State File

```python
tf_utils.clean_state_file_by_prefixes(
    input_path="input.tfstate",
    output_path="cleaned.tfstate",
    keep_prefixes=["module1"],
    remove_prefixes=["module2"]
)
```

#### Download Workspace State

```python
tf_utils.download_workspace_state(
    org_name="my-org",
    workspace_name="my-workspace",
    token="TERRAFORM_API_TOKEN"
)
```

#### Trigger and Monitor a Run

```python
run_id = tf_utils.trigger_run(
    workspace_id="ws-xxxx",
    auto_apply=True
)
tf_utils.monitor_run(
    run_id=run_id
)
```

#### Get Run Outputs

```python
outputs = tf_utils.get_run_outputs(
    run_id="run-xxxx"
)
print(outputs)
```

## Functions Overview

- `setup_logging()`: Configure logging.
- `clean_state_file_by_prefixes()`: Filter resources in a state file.
- `download_workspace_state()`: Download the latest state from Terraform Cloud.
- `push_state_to_terraform_cloud()`: Upload a state file to Terraform Cloud.
- `lock_workspace()`, `unlock_workspace()`: Lock/unlock a workspace.
- `trigger_run()`, `monitor_run()`, `cancel_run()`, `discard_run()`, `apply_run()`: Manage runs.
- `get_run_outputs()`, `get_plan_summary()`: Retrieve outputs and plan details.
- `get_variable_id()`, `update_variable()`: Manage workspace variables.

## Requirements

- Python 3.11+
- `requests` library

## Notes

- All API operations require a valid Terraform Cloud API token.
- Use caution when discarding or canceling runs, as this may affect your infrastructure state.

## License

MIT License
