import requests
import numpy as np

BASE_URL = "http://localhost:8080"  # Replace with your API base URL

def get_scenarios():
    """Fetch all scenarios."""
    url = f"{BASE_URL}/scenarios"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

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
        vehicles = response.json()
        for vehicle in vehicles:
            vehicle["vehicleSpeed"] = generate_vehicle_speed()
        return vehicles
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def update_scenario(scenario_id, payload):
    """Update a specific scenario with new data."""
    url = f"{BASE_URL}/scenarios/update_scenario/{scenario_id}"
    response = requests.put(url, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def generate_vehicle_speed():
    speed = np.random.uniform(8.33, 13.89)  # speed in meters per second (m/s)
    print("speed: ",speed)
    return speed