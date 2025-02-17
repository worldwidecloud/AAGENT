import os
import time
import requests

# Configuration: Set these values via environment variables or directly here
API_BASE_URL = os.getenv("AAICC_BASE_URL", "https://aihw-composer.draco.res.ibm.com/api")
API_TOKEN = os.getenv("AAICC_API_TOKEN", "hF2Ns0wR0ncuUpusPhJBH29OiTXn6KKxbOoDACe3ou3C3Pkudwizb+68Mkwu8yfmVQb/rbUvKcF75ZmJWn5pFg==")

# Function to submit an experiment
def submit_experiment():
    endpoint = f"{API_BASE_URL}/experiments/submit"
    headers = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "name": "Test Experiment",
        "parameters": {
            "network_type": "AnalogLinear",
            "device_preset": "PCM_Default",
            "optimizer": "AnalogSGD",
            "learning_rate": 0.1
        }
    }
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        experiment_info = response.json()
        print("Experiment submitted successfully!")
        print("Experiment ID:", experiment_info.get("experiment_id"))
        return experiment_info.get("experiment_id")
    except requests.exceptions.RequestException as e:
        print("Error submitting experiment:", e)
        return None

# Function to poll for experiment status
def poll_experiment_status(experiment_id):
    endpoint = f"{API_BASE_URL}/experiments/status/{experiment_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    while True:
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            status_info = response.json()
            print("Current status:", status_info.get("status"))
            
            if status_info.get("status") in ["Completed", "Failed"]:
                print("Experiment finished with status:", status_info.get("status"))
                break
            else:
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print("Error polling status:", e)
            break

if __name__ == "__main__":
    print("Starting the agent...")
    exp_id = submit_experiment()
    if exp_id:
        print("Polling experiment status for ID:", exp_id)
        poll_experiment_status(exp_id)