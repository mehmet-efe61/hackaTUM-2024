from api_interaction import get_customers, get_vehicles
from visualization import visualize_scenario

# use this for local visualize without webpage


def main():
    # Fetch and visualize data for an existing scenario

    scenario_id = input("Enter the scenario ID: ").strip()
    customers = get_customers(scenario_id)
    vehicles = get_vehicles(scenario_id)

    if customers and vehicles:
        print("Customers:", customers)
        print("Vehicles:", vehicles)

        # Visualize the scenario
        visualize_scenario(vehicles, customers)
    else:
        print(f"Failed to fetch data for scenario ID: {scenario_id}")

if __name__ == "__main__":
    main()
