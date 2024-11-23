import numpy as np
from path import Path


def calculate_distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def assign_vehicles_to_customers(vehicles, customers, weights):
    """Assign nearest available vehicles to customers."""
    assignments = []

    for customer in customers:
        nearest_vehicle = None
        shortest_distance = float("inf")

        for vehicle in vehicles:
            if vehicle["isAvailable"]:
                path = Path(vehicle, customer)
                distance = 1 / path.compute_score(weights)
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_vehicle = vehicle

        if nearest_vehicle:
            assignments.append({
                "customer_id": customer["id"],
                "vehicle_id": nearest_vehicle["id"],
                "path": path.metrics
            })
            nearest_vehicle["isAvailable"] = False
    print(assignments)
    return assignments


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
