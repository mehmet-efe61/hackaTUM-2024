from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from api_interaction import get_scenarios, get_customers, get_vehicles
from fleet_logic import assign_vehicles_to_customers, move_vehicles_toward_customers
import io
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

# Global dictionary to store visualizations for each scenario
visualization_data = {}


@app.route("/")
def index():
    """Serve the main webpage."""
    return render_template("index.html")


@app.route("/scenarios", methods=["GET"])
def fetch_scenarios():
    """Fetch all scenarios."""
    scenarios = get_scenarios()
    if scenarios:
        return jsonify(scenarios)
    return jsonify({"error": "Unable to fetch scenarios"}), 500


@app.route("/simulate/<scenario_id>", methods=["POST"])
def simulate_movement(scenario_id):
    """Simulate vehicle movement toward customers and generate visualizations."""
    customers = get_customers(scenario_id)
    vehicles = get_vehicles(scenario_id)

    if not customers or not vehicles:
        return jsonify({"error": "Unable to fetch customers or vehicles"}), 500

    # Assign vehicles to customers
    assignments = assign_vehicles_to_customers(vehicles, customers)

    # Simulate movement over 10 steps and save plots for each step
    simulation_steps = []
    visualization_files = []

    for step in range(10):
        vehicles = move_vehicles_toward_customers(vehicles, customers, assignments)
        simulation_steps.append({
            "step": step + 1,
            "vehicles": vehicles.copy(),
            "assignments": assignments
        })

        # Create a matplotlib plot
        fig, ax = plt.subplots()
        ax.set_title(f"Step {step + 1}")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Plot customers
        for customer in customers:
            ax.plot(customer["coordX"], customer["coordY"], "ro", label="Customer Start" if step == 0 else "")
            # Add customer ID as a label above the point
            ax.text(customer["coordX"], customer["coordY"] + 0.0005, customer["id"][:6], color="red", fontsize=8)

        # Plot vehicles
        for vehicle in vehicles:
            ax.plot(vehicle["coordX"], vehicle["coordY"], "go", label="Vehicle" if step == 0 else "")
            # Add vehicle ID as a label above the point
            ax.text(vehicle["coordX"], vehicle["coordY"] + 0.0005, vehicle["id"][:6], color="green", fontsize=8)

        ax.legend()

        # Save the plot to a BytesIO buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        visualization_files.append(buf)
        plt.close(fig)

    # Store the visualizations in the global dictionary
    visualization_data[scenario_id] = visualization_files

    print(f"Stored visualization for {scenario_id}: {len(visualization_files)} steps created.")

    return jsonify({
        "message": "Simulation completed",
        "steps": simulation_steps,
        "visualization_files": [f"Step {i + 1}" for i in range(len(visualization_files))]
    })


@app.route("/visualize_step/<scenario_id>/<step_index>", methods=["GET"])
def visualize_step(scenario_id, step_index):
    """Serve the visualization for a specific simulation step."""
    print(f"Requested scenario_id: {scenario_id}, step_index: {step_index}")  # Debug log
    try:
        step_index = int(step_index)
        files = visualization_data.get(scenario_id)

        if not files:
            print(f"No visualization data for scenario {scenario_id}.")  # Debug log
            return jsonify({"error": "No visualizations found for this scenario"}), 404

        buf = files[step_index]
        return send_file(buf, mimetype="image/png")
    except (IndexError, TypeError) as e:
        print(f"Visualization error for scenario {scenario_id}: {e}")  # Debug log
        return jsonify({"error": "Invalid step index"}), 404


if __name__ == "__main__":
    app.run(debug=True)
