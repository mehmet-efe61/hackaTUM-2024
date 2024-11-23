import requests
import matplotlib.pyplot as plt

# Step 1: Fetch scenario data from the API
base_url = "http://localhost:8080"
scenario_id = "d42e8223-4031-481e-b576-6a529338f6af"
url = f"{base_url}/scenarios/{scenario_id}"

response = requests.get(url)

if response.status_code == 200:
    print("Success! Scenario data received:")
    scenario_data = response.json()
    print(scenario_data)
else:
    print(f"Error: {response.status_code}, Message: {response.text}")
    exit()

# Step 2: Extract data for visualization
vehicles = scenario_data["vehicles"]
customers = scenario_data["customers"]

# Separate coordinates for vehicles
vehicle_coords = [(v["coordX"], v["coordY"]) for v in vehicles]

# Separate start and destination coordinates for customers
customer_starts = [(c["coordX"], c["coordY"]) for c in customers]
customer_destinations = [(c["destinationX"], c["destinationY"]) for c in customers]

# Step 3: Plot the data
plt.figure(figsize=(10, 8))

# Plot vehicles (add label only once)
for i, coord in enumerate(vehicle_coords):
    plt.scatter(coord[0], coord[1], c="blue", label="Vehicles" if i == 0 else "", s=100)

# Plot customer start locations (add label only once)
for i, coord in enumerate(customer_starts):
    plt.scatter(coord[0], coord[1], c="red", label="Customer Starts" if i == 0 else "", s=100)

# Plot customer destination locations (add label only once)
for i, coord in enumerate(customer_destinations):
    plt.scatter(coord[0], coord[1], c="green", label="Customer Destinations" if i == 0 else "", s=100)

# Add lines connecting customers' start and destination points
for start, destination in zip(customer_starts, customer_destinations):
    plt.plot([start[0], destination[0]], [start[1], destination[1]], c="gray", linestyle="--")

# Set plot title and labels
plt.title("Scenario Visualization")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()  # Automatically handle unique labels
plt.grid()

# Show the plot
plt.show()
