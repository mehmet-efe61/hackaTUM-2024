from visualization import visualize_scenario

import requests

BASE_URL = "http://localhost:8080"

def get_customers(scenario_id):
    """Fetch all customers for a specific scenario."""
    url = f"{BASE_URL}/scenarios/{scenario_id}/customers"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_vehicles(scenario_id):
    """Fetch all vehicles for a specific scenario."""
    url = f"{BASE_URL}/scenarios/{scenario_id}/vehicles"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def create_scenario(payload):
    """Create a new scenario."""
    url = f"{BASE_URL}/scenario/create"
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example Usage:
scenario_id = "d42e8223-4031-481e-b576-6a529338f6af"  # Replace with your scenario ID
customers = get_customers(scenario_id)
print("Customers:", customers)

vehicles = get_vehicles(scenario_id)
print("Vehicles:", vehicles)

# Example payload for creating a scenario
payload = {
    "num_vehicles": 5,
    "num_customers": 5
}
new_scenario = create_scenario(payload)
print("New Scenario:", new_scenario)
