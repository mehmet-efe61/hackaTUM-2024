import numpy as np
from path import Path  
import json
import os

def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def assign_vehicles_to_customers(vehicles, customers, weights):
    normalization_params = normalize_metrics(vehicles, customers)
    assignments = []

    for customer in customers:
        nearest_vehicle = None
        highest_score = float("-inf")

        for vehicle in vehicles:
            if vehicle["isAvailable"]:
                path = Path(vehicle, customer)
                score = path.compute_score(weights, normalization_params)
                if score > highest_score:
                    highest_score = score
                    nearest_vehicle = vehicle
                    best_path = path

        if nearest_vehicle:
            assignments.append({
                "customer_id": customer["id"],
                "vehicle_id": nearest_vehicle["id"],
                "path_metrics": best_path.metrics,
                "score": highest_score
            })
            nearest_vehicle["isAvailable"] = False

    return assignments

def normalize_metrics(vehicles, customers):
    all_metrics = {
        "total_dist": [],
        "co2_emission": [],
        "energy_consumption": [],
        "cost": [],
        "profit": []
    }

    # Collect all values for normalization
    for vehicle in vehicles:
        for customer in customers:
            path = Path(vehicle, customer)
            for metric, value in path.metrics.items():
                all_metrics[metric].append(value)

    # Compute min and max for each metric
    normalization_params = {
        metric: {"min": min(values), "max": max(values)} for metric, values in all_metrics.items()
    }

    return normalization_params


def calculate_avg_metrics(assignments):
    """Calculate average metrics for a list of assignments."""
    total_metrics = {
        "total_dist": 0,
        "co2_emission": 0,
        "energy_consumption": 0,
        "cost": 0,
        "profit": 0
    }

    for assignment in assignments:
        metrics = assignment["path_metrics"]
        for key, value in metrics.items():
            total_metrics[key] += value

    num_assignments = len(assignments)
    avg_metrics = {key: (total_metrics[key] / num_assignments if num_assignments > 0 else 0) for key in total_metrics}
    return avg_metrics

def dump_avg_metrics_to_json(payload,filename = "index.json"):
    """Dump assignments to a JSON file."""
    with open(os.path.join("static", filename), "w") as file:
        json.dump(payload, file, indent=4)

def move_vehicles_toward_customers(vehicles, customers, assignments, step=0.01):
    """Move vehicles incrementally toward their assigned customers."""
    for assignment in assignments:
        vehicle = next(v for v in vehicles if v["id"] == assignment["vehicle_id"])
        customer = next(c for c in customers if c["id"] == assignment["customer_id"])

        if vehicle and customer:
            dx = customer["coordX"] - vehicle["coordX"]
            dy = customer["coordY"] - vehicle["coordY"]
            distance = calculate_distance(vehicle["coordX"], vehicle["coordY"], customer["coordX"], customer["coordY"])

            if distance > step:
                vehicle["coordX"] += step * (dx / distance)
                vehicle["coordY"] += step * (dy / distance)
            else:
                vehicle["coordX"] = customer["coordX"]
                vehicle["coordY"] = customer["coordY"]
                vehicle["isAvailable"] = True
    return vehicles
