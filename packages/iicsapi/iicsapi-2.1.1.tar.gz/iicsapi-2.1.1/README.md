# IICSAPI

This is a Python package for interacting with Informatica Intelligent Cloud Services (IICS) Data Integration REST API. It provides a simple and efficient way to retrieve information on IICS Data Integration taskflows, mappings, and other related resources.

## Features
- Retrieve taskflow run details
- Retrieve mapping task run details
- Full-depth search for taskflows and mappings

## Requirements
- Python (tested on 3.11.11)
- Libaries in `requirements.txt`
- Informatica Intelligent Cloud Services (IICS) account with appropriate permissions

## Installation
You can install the package using pip:

```bash
pip install iicsapi
```

## Usage
```python
from iicsapi import IICSAPI

iicsClient = IICSAPI(
    username="my_username",
    password="my_password",
    pod="use6", # see Informatica Cloud documentation for pod names
    provider_url="https://dm-us.informaticacloud.com" # see Informatica Cloud documentation for provider URLs
)

# Execute a taskflow
tf_run_id = iicsClient.execute_tf(taskflow_name="MY_TASKFLOW")
# Returns the taskflow run ID. You can then use this to check the status of the taskflow run.
run_details_df = iicsClient.get_tf_audit_logs(tf_run_id)

###############################################

# Get the latest run for a specific taskflow
latest_run_df = iicsClient.get_tf_audit_logs("123456789012345678")

# Convert the result pandas DataFrame to a CSV
latest_run_df.to_csv("iics_audit.csv", index=False)

```
