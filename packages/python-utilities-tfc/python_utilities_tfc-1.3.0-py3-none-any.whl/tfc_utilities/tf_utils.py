import json
import re
import base64
import hashlib
import requests
import uuid
import logging
import time
import os

TERRAFORM_CLOUD_TOKEN = os.environ.get("TERRAFORM_CLOUD_TOKEN")
TERRAFORM_ORG_NAME = os.getenv("TERRAFORM_ORG_NAME")

if not TERRAFORM_CLOUD_TOKEN or not TERRAFORM_ORG_NAME:
    logging.error("❌ Environment variable TERRAFORM_CLOUD_TOKEN or TERRAFORM_ORG_NAME is not set.")
    exit(1)


def setup_logging():
    """
    Sets up the logging configuration for the application.

    This function sets the logging level to INFO and the logging format to include the timestamp,
    log level, and the log message.

    Parameters:
        None

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def match_prefixes(resource, prefixes):
    """
    Returns True if any of the given prefixes match the module or instance keys in the given resource.

    Args:
        resource (dict): A dictionary representing a Terraform resource.
        prefixes (list): A list of strings representing the prefixes to match.

    Returns:
        bool: True if any of the prefixes match the module or instance keys in the resource, False otherwise.
    """
    module = resource.get("module", "")
    module_parts = module.split(".")
    if len(module_parts) > 1 and any(module_parts[1].startswith(prefix) for prefix in prefixes):
        return True

    module_matches = re.findall(r'\["([^"]+)"\]', module)
    if any(any(m.startswith(prefix) for prefix in prefixes) for m in module_matches):
        return True

    for instance in resource.get("instances", []):
        index_key = instance.get("index_key")
        if isinstance(index_key, str) and any(index_key.startswith(prefix) for prefix in prefixes):
            return True

    return False

def clean_state_file_by_prefixes(input_path, output_path, keep_prefixes=None, remove_prefixes=None):
    """
    Clean a Terraform state file by filtering resources based on given prefixes.

    Args:
        input_path (str): The path to the input state file.
        output_path (str): The path to the output state file.
        keep_prefixes (list, optional): A list of prefixes to keep. Defaults to None.
        remove_prefixes (list, optional): A list of prefixes to remove. Defaults to None.

    Returns:
        str: The path to the output state file.
    """
    with open(input_path, "r") as f:
        state = json.load(f)

    all_resources = state.get("resources", [])

    # Step 1: KEEP filtering
    if keep_prefixes:
        logging.info(f"🔎 Keeping only resources matching: {keep_prefixes}")
        filtered_resources = [res for res in all_resources if match_prefixes(res, keep_prefixes)]
    else:
        filtered_resources = all_resources

    # Step 2: REMOVE filtering
    if remove_prefixes:
        logging.info(f"🗑️ Removing resources matching: {remove_prefixes}")
        filtered_resources = [res for res in filtered_resources if not match_prefixes(res, remove_prefixes)]

    # Write cleaned state
    state["resources"] = filtered_resources
    with open(output_path, "w") as f:
        json.dump(state, f, indent=2)

    logging.info(f"✅ Final filtered state written to: {output_path}")
    return output_path

def format_resource_address(resource, instance):
    """
    Formats a Terraform resource address for a given resource instance.

    Args:
        resource (dict): A dictionary representing a Terraform resource.
        instance (dict): A dictionary representing a specific instance of the resource.

    Returns:
        str: The formatted resource address.
    """
    parts = []

    if "module" in resource:
        parts.append(resource['module'])

    if resource.get("mode") == "data":
        parts.append(f"data.{resource['type']}.{resource['name']}")
    else:
        parts.append(f"{resource['type']}.{resource['name']}")

    index_key = instance.get("index_key")
    if index_key is not None:
        if isinstance(index_key, str):
            parts[-1] += f'["{index_key}"]'
        else:
            parts[-1] += f"[{index_key}]"

    return ".".join(parts)

def generate_state_list(state_file_path):
    """
    Generates a list of formatted resource addresses from a Terraform state file.

    Args:
        state_file_path (str): The path to the Terraform state file.

    Returns:
        list: A list of formatted resource addresses.
    """
    with open(state_file_path, "r") as file:
        state_data = json.load(file)

    formatted_addresses = []

    for resource in state_data.get("resources", []):
        for instance in resource.get("instances", []):
            formatted_addresses.append(format_resource_address(resource, instance))

    return formatted_addresses

def lock_workspace(workspace_id, token=TERRAFORM_CLOUD_TOKEN):
    """
    Locks a Terraform Cloud workspace.

    Args:
        workspace_id (str): The ID of the workspace to lock.
        token (str): The Terraform Cloud API token.

    Raises:
        Exception: If the workspace fails to lock.

    Returns:
        None
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json"
    }
    url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/actions/lock"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        logging.info("🔒 Workspace locked successfully.")
    else:
        raise Exception(f"❌ Failed to lock workspace: {response.status_code} {response.text}")

def unlock_workspace(workspace_id, token=TERRAFORM_CLOUD_TOKEN):
    """
    Unlocks a Terraform Cloud workspace.

    Args:
        workspace_id (str): The ID of the workspace to unlock.
        token (str): The Terraform Cloud API token.

    Returns:
        None
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json"
    }
    url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/actions/unlock"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        logging.info("🔓 Workspace unlocked successfully.")
    else:
        logging.warning(f"⚠️ Warning: Failed to unlock workspace: {response.status_code} {response.text}")

def push_state_to_terraform_cloud(state_path, workspace_id, token=TERRAFORM_CLOUD_TOKEN):
    """
    Pushes a cleaned Terraform state to Terraform Cloud.

    Args:
        state_path (str): The path to the cleaned state file.
        workspace_id (str): The ID of the Terraform Cloud workspace.
        token (str): The Terraform Cloud API token.

    Raises:
        Exception: If the state upload fails.

    Returns:
        None
    """
    with open(state_path, "rb") as f:
        state_raw = f.read()
        state_json = json.loads(state_raw)
    
    state_str = state_raw.decode("utf-8")
    state_json = json.loads(state_str)

    state_json["lineage"] = str(uuid.uuid4())
    state_json["serial"] = 1

    update_raw_state = json.dumps(state_json, indent=2).encode("utf-8")
    state_json = json.loads(update_raw_state)

    md5_checksum = hashlib.md5(update_raw_state).hexdigest()
    state_encoded = base64.b64encode(update_raw_state).decode("utf-8")

    payload = {
        "data": {
            "type": "state-versions",
            "attributes": {
                "serial": 1,
                "md5": md5_checksum,
                "state": state_encoded
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json"
    }

    url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/state-versions"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        logging.info("✅ Successfully pushed cleaned state to Terraform Cloud.")
    else:
        raise Exception(f"❌ Failed to upload state.\nStatus Code: {response.status_code}\nResponse: {response.text}")

def download_workspace_state(workspace_name, token=TERRAFORM_CLOUD_TOKEN, output_path="downloaded.tfstate"):
    """
    Downloads the state file of a Terraform workspace.

    Args:
        org_name (str): The name of the organization.
        workspace_name (str): The name of the workspace.
        token (str): The Terraform API token.
        output_path (str, optional): The path to save the downloaded state file. Defaults to "downloaded.tfstate".

    Returns:
        str: The path to the downloaded state file.

    Raises:
        Exception: If the current state version cannot be retrieved.
        Exception: If the state file cannot be downloaded.
    """
    # Step 1: Get the workspace ID
    workspace_id = get_workspace_id(workspace_name)

    # Step 2: Get the current state version info
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json"
    }
    url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/current-state-version"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to get current state version: {response.status_code} {response.text}")

    state_data = response.json()
    download_url = state_data["data"]["attributes"]["hosted-state-download-url"]

    # Step 3: Download state file (add auth headers here too!)
    download_response = requests.get(download_url, headers={"Authorization": f"Bearer {token}"})
    if download_response.status_code != 200:
        raise Exception(f"❌ Failed to download state file: {download_response.status_code} {download_response.text}")

    with open(output_path, "wb") as f:
        f.write(download_response.content)

    logging.info(f"✅ Downloaded state file from workspace '{workspace_name}' to '{output_path}'")
    return output_path

def get_workspace_id(workspace_name, org_name=TERRAFORM_ORG_NAME, token=TERRAFORM_CLOUD_TOKEN):
    """
    Retrieves the workspace ID for a given workspace in a Terraform organization.

    Args:
        workspace_name (str): The name of the workspace.
        org_name (str): The name of the organization.
        token (str): The Terraform API token.

    Returns:
        str: The workspace ID.

    Raises:
        Exception: If the workspace cannot be fetched.
        ValueError: If the workspace is not found in the organization.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/vnd.api+json"
    }

    base_url = f"https://app.terraform.io/api/v2/organizations/{org_name}/workspaces"
    page = 1

    def safe_get(url, headers, verify_ssl=True):
        try:
            return requests.get(url, headers=headers, timeout=10, verify=verify_ssl)
        except requests.exceptions.SSLError as e:
            if verify_ssl:
                logging.warning(f"⚠️ SSL verification failed, retrying without SSL verification: {e}")
                return safe_get(url, headers, verify_ssl=False)
            else:
                raise

    while True:
        url = f"{base_url}?page[number]={page}"
        response = safe_get(url, headers)
        
        if response.status_code != 200:
            raise Exception(f"❌ Failed to fetch workspaces: {response.status_code} {response.text}")

        data = response.json()
        for workspace in data.get("data", []):
            if workspace["attributes"]["name"] == workspace_name:
                logging.info(f"✅ Found workspace ID: {workspace['id']}")
                return workspace["id"]

        # Check if there are more pages
        next_page = data.get("links", {}).get("next")
        if not next_page:
            break
        page += 1

    raise ValueError(f"❌ Workspace '{workspace_name}' not found in organization '{org_name}'.")

def get_variable_id(workspace_id, target_variable_name, organization=TERRAFORM_ORG_NAME, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    """
    Retrieve the ID of a specific Terraform variable within a workspace.

    Args:
        api_token (str): The API token for authenticating with the Terraform Cloud API.
        organization (str): The name of the Terraform Cloud organization.
        workspace_id (str): The ID of the workspace containing the variable.
        target_variable_name (str): The name of the variable to retrieve the ID for.
        url (str, optional): The base URL of the Terraform Cloud API. Defaults to "https://app.terraform.io".

    Returns:
        str or None: The ID of the variable if found, otherwise None.

    Logs:
        - Logs an informational message if the variable is not found.
        - Logs an error message if the API request fails.
    """
    url = f'{url}/api/v2/vars?filter[organization][username]={organization}&filter[workspace][id]={workspace_id}'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        variables = response.json()['data']

        for variable in variables:
            if variable['attributes']['key'] == target_variable_name:
                return variable['id']

        logging.info(f'Variable with name "{target_variable_name}" not found.')
        return None

    else:
        logging.info(f'Error listing variables: {response.status_code}\n{response.text}')
        return None

def update_variable(variable_id, new_value, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    """
    Updates a Terraform Cloud workspace variable with a new value.

    Args:
        api_token (str): The API token for authenticating with Terraform Cloud.
        organization (str): The name of the Terraform Cloud organization.
        workspace_id (str): The ID of the workspace containing the variable.
        variable_id (str): The ID of the variable to update.
        new_value (str): The new value to assign to the variable.
        url (str, optional): The base URL for the Terraform Cloud API. Defaults to "https://app.terraform.io".

    Returns:
        None: Logs the result of the update operation.

    Raises:
        None: This function does not raise exceptions but logs errors if the update fails.
    """
    url = f'{url}/api/v2/vars/{variable_id}'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    payload = {
        'data': {
            'type': 'vars',
            'id': variable_id,
            'attributes': {
                'value': new_value
            }
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        logging.info('Variable update successful!')
    else:
        logging.info(f'Error updating variable: {response.status_code}\n{response.text}')

def get_workspace_runs(workspace_id, api_token=TERRAFORM_CLOUD_TOKEN,url="https://app.terraform.io"):
    """
    Retrieve the list of runs for a specific Terraform Cloud workspace.

    Args:
        api_token (str): The API token used for authentication with Terraform Cloud.
        workspace_id (str): The ID of the workspace for which to retrieve runs.
        url (str, optional): The base URL of the Terraform Cloud API. Defaults to "https://app.terraform.io".

    Returns:
        list: A list of runs associated with the specified workspace, if the request is successful.
        None: If the request fails, logs the error and returns None.

    Raises:
        None: This function does not raise exceptions directly but logs errors in case of failed requests.
    """
    url = f'{url}/api/v2/workspaces/{workspace_id}/runs'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data', [])
        return data
    else:
        logging.info(f'Error retrieving runs: {response.status_code}\n{response.text}')
        return None

def discard_run(run_id, api_token=TERRAFORM_CLOUD_TOKEN,url="https://app.terraform.io"):
    url = f'{url}/api/v2/runs/{run_id}/actions/discard'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        logging.info(f"Run {run_id} discarded successfully.")
    elif response.status_code == 409:
        logging.info(f"Cannot discard run {run_id}: Transition not allowed.")
    else:
        logging.info(f'Error discarding run {run_id}: {response.status_code}\n{response.text}')

def cancel_run(run_id, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    url = f'{url}/api/v2/runs/{run_id}/actions/cancel'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 202:
        logging.info(f"Run {run_id} canceled successfully.")
    elif response.status_code == 409:
        logging.info(f"Cannot cancel run {run_id}: Transition not allowed.")
    else:
        logging.info(f'Error canceling run {run_id}: {response.status_code}\n{response.text}')

def trigger_run(workspace_id, auto_apply, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    url = f'{url}/api/v2/runs'

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    payload = {
        'data': {
            'type': 'runs',
            'attributes': {
                'is-destroy': False,
                'message': 'Triggered by Python script',
                'auto-apply': auto_apply
            },
            'relationships': {
                'workspace': {
                    'data': {
                        'type': 'workspaces',
                        'id': workspace_id
                    }
                }
            }
        }
    }

    logging.info(payload)

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        data = response.json().get('data', {})
        run_id = data.get('id', None)
        if run_id:
            logging.info(f'Run triggered successfully! {run_id}') 
            # Discard old runs except the most recent one
            runs = get_workspace_runs(workspace_id)
            if runs:
                # Sort runs by creation time in descending order
                sorted_runs = sorted(runs, key=lambda x: x['attributes']['created-at'], reverse=True)
                
                # Get the ID of the most recent run
                most_recent_run_id = sorted_runs[0]['id']

                # Check if there are any pending runs
                pending_runs = [run for run in sorted_runs if run['attributes']['status'] in ['pending', 'planning']]

                if pending_runs:
                    # [1:] - starting range at 1 because i want to keep the latest pending run
                    for run in pending_runs[1:]:
                        logging.info(f"Pending run: {run['id']} {run['attributes']['status']}")
                        cancel_run(run['id'])
                
                other_runs = [
                    run for run in sorted_runs 
                    if run['id'] != run_id and run['attributes']['status'] not in [
                        'discarded', 'planned_and_finished', 'planning', 'pending', 'applied', 'errored', 'canceled', 'force_canceled'
                    ]
                ]
                # other_runs = [run for run in sorted_runs]
                if other_runs:
                    # [0:] - because these are all the possible stalled runs that are not in pending
                    for run in other_runs[0:]:
                        logging.info(f"Other run: {run['id']} {run['attributes']['status']}")
                        discard_run(run['id'])
                

            return run_id
        else:
            logging.info('Error: Could not retrieve run ID from response.')
            return None
    else:
        logging.info(f'Error triggering run: {response.status_code}\n{response.text}')
        return None
 
def get_run_status(run_id, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }
    url = f'{url}/api/v2/runs/{run_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json().get('data', {})
        attributes = data.get('attributes', {})
        status = attributes.get('status', '')
        return status
    else:
        return None

def monitor_run(run_id):
    """
    Monitor the status of a Terraform run until it completes.
    """
    while True:
        status = get_run_status(run_id)
        if status in ['pending', 'planning', 'applying', 'policy_checking', 'plan_queued', 'post_plan_running', 'apply_queued', 'None' ]:
            logging.info(f"Run status: {status}. {run_id} Waiting for completion...")
            logging.info(f"Run status: {status}. {run_id} Waiting for completion...")
            time.sleep(10)  # Adjust the polling interval as needed
        elif status == 'applied':
            logging.info(f"Run {run_id} applied successfully.")
            logging.info(f"Run {run_id} applied successfully.")
            break
        elif status == 'apply_queued':
            logging.info(f"Run status: {run_id} {status}. Apply Queued, Head to the workspace to approve.")
            logging.info(f"Run status: {run_id} {status}. Apply Queued, Head to the workspace to approve.")
            break    
        elif status == 'errored' or status == 'canceled':
            logging.info(f"Run status: {run_id} {status}. Check the Terraform UI for details.")
            logging.info(f"Run status: {run_id} {status}. Check the Terraform UI for details.")
            raise RuntimeError(f"Run status: {run_id} {status}. Check the Terraform UI for details.")
            break
        elif status == 'planned_and_finished':
            logging.info(f"No change detected on the workspace")
            logging.info(f"No change detected on the workspace")
            break
        else:
            logging.info(f"Unknown status: {run_id} {status}.")
            logging.info(f"Unknown status: {run_id} {status}.")
            break
        
def get_run_outputs(run_id, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    """
    Retrieves the outputs of a Terraform Cloud run.

    Args:
        api_token (str): Terraform Cloud API token.
        run_id (str): The ID of the Terraform run.
        url (str, optional): Terraform Cloud URL. Defaults to 'https://app.terraform.io'.

    Returns:
        dict: A dictionary of output key-value pairs, or an empty dict if no outputs are found.
    """
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }
    outputs_url = f"{url}/api/v2/runs/{run_id}/apply"

    # Step 1: Get the Apply ID from the Run
    response = requests.get(outputs_url, headers=headers)
    if response.status_code != 200:
        logging.error(f"❌ Failed to get apply details: {response.status_code} {response.text}")
        return {}

    apply_data = response.json()
    apply_id = apply_data.get("data", {}).get("id")

    if not apply_id:
        logging.warning("⚠️ No apply ID found for this run.")
        return {}

    # Step 2: Fetch Outputs
    outputs_fetch_url = f"{url}/api/v2/applies/{apply_id}/outputs"
    outputs_response = requests.get(outputs_fetch_url, headers=headers)

    if outputs_response.status_code != 200:
        logging.error(f"❌ Failed to get outputs: {outputs_response.status_code} {outputs_response.text}")
        return {}

    outputs_data = outputs_response.json().get("data", [])

    outputs = {}
    for output in outputs_data:
        output_key = output['attributes']['name']
        output_value = output['attributes']['value']
        outputs[output_key] = output_value

    return outputs

def get_plan_summary(run_id, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    """
    Retrieves the plan summary (additions, changes, deletions) from a Terraform Cloud run.

    Args:
        api_token (str): Terraform Cloud API token.
        run_id (str): The ID of the Terraform run.
        url (str, optional): Terraform Cloud URL. Defaults to 'https://app.terraform.io'.

    Returns:
        dict: A dictionary containing 'add', 'change', 'destroy' counts.
    """
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    # Step 1: Fetch run info to get the Plan ID
    run_url = f"{url}/api/v2/runs/{run_id}"
    response = requests.get(run_url, headers=headers)
    if response.status_code != 200:
        logging.error(f"❌ Failed to get run details: {response.status_code} {response.text}")
        return {}

    run_data = response.json()
    plan_id = run_data.get("data", {}).get("relationships", {}).get("plan", {}).get("data", {}).get("id")

    if not plan_id:
        logging.warning(f"⚠️ No plan found for run {run_id}. The plan may not be ready.")
        return {}

    # Step 2: Fetch the Plan JSON
    plan_url = f"{url}/api/v2/plans/{plan_id}"
    plan_response = requests.get(plan_url, headers=headers)

    if plan_response.status_code != 200:
        logging.error(f"❌ Failed to get plan details: {plan_response.status_code} {plan_response.text}")
        return {}

    plan_data = plan_response.json().get("data", {}).get("attributes", {})

    summary = {
        "add": plan_data.get("resource-additions", 0),
        "change": plan_data.get("resource-changes", 0),
        "destroy": plan_data.get("resource-destructions", 0),
        "has-changes": plan_data.get("has-changes", True)
    }

    return summary

def apply_run(run_id, api_token=TERRAFORM_CLOUD_TOKEN, url="https://app.terraform.io"):
    """
    Applies a Terraform Cloud run (auto-approve).

    Args:
        api_token (str): Terraform Cloud API token.
        run_id (str): The ID of the Terraform run.
        url (str, optional): Terraform Cloud URL. Defaults to 'https://app.terraform.io'.
    """
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/vnd.api+json'
    }

    apply_url = f"{url}/api/v2/runs/{run_id}/actions/apply"

    response = requests.post(apply_url, headers=headers)

    if response.status_code == 202:
        logging.info(f"🚀 Apply triggered successfully for run {run_id}.")
    else:
        logging.error(f"❌ Failed to apply run: {response.status_code} {response.text}")
