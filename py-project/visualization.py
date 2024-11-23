import matplotlib.pyplot as plt
import os

def visualize_scenario(vehicles, customers, output_path="static/visualization.png"):
    """Visualize vehicles and customers on a map and save the plot."""
    plt.figure(figsize=(10, 8))

    # Plot vehicles
    for i, vehicle in enumerate(vehicles):
        plt.scatter(vehicle["coordX"], vehicle["coordY"], c="blue", label="Vehicles" if i == 0 else "", s=100)

    # Plot customer start locations
    for i, customer in enumerate(customers):
        plt.scatter(customer["coordX"], customer["coordY"], c="red", label="Customer Starts" if i == 0 else "", s=100)
        plt.plot(
            [customer["coordX"], customer["destinationX"]],
            [customer["coordY"], customer["destinationY"]],
            c="gray", linestyle="--"
        )

    # Plot customer destination locations
    for i, customer in enumerate(customers):
        plt.scatter(customer["destinationX"], customer["destinationY"], c="green", label="Customer Destinations" if i == 0 else "", s=100)

    # Add title and labels
    plt.title("Scenario Visualization")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid()

    # Save the plot
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
