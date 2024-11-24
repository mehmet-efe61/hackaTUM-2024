import numpy as np
import yaml
import os

from constants import *

class Path():

    def __init__(self, vehicle, customer) -> None:
        self.vehicle: dict = vehicle
        self.customer: dict = customer
        self.dist_to_customer = self.calculate_distance(vehicle['coordX'], vehicle['coordY'], customer['coordX'], customer['coordY'])
        self.dist_to_goal = self.calculate_distance(customer['coordX'], customer['coordY'], customer['destinationX'], customer['destinationY'])
        self.time_to_goal = self.dist_to_goal / self.vehicle["vehicleSpeed"]
        self.total_time = (self.dist_to_customer + self.dist_to_goal) / self.vehicle["vehicleSpeed"]
        self.metrics: dict = {
            "total_dist": self.dist_to_customer + self.dist_to_goal,  # in meters
        }
        self.calculate_all()
            
    def calculate_distance(self, start_x, start_y, end_x, end_y):
        lat1 = np.radians(start_y)
        lon1 = np.radians(start_x)
        lat2 = np.radians(end_y)
        lon2 = np.radians(end_x)
        R = 6371000
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        return R * c  # distance in meters (m)
    

    def calculate_co2_emission(self): #TODO: Use a better formula to calculate CO2 emission
        self.metrics["co2_emission"] = self.total_time * CO2_EMISSION_PER_SECOND + 0.5 * self.total_time ** 2 # CO2 emission in grams (g)
    
    def calculate_energy_consumption(self): #TODO: Use a better formula to calculate energy consumption
        self.metrics["energy_consumption"] = self.total_time * ENERGY_CONSUMPTION_PER_SECOND + 2 * self.total_time # energy consumption in joules (J)

    def calculate_cost(self):
        self.metrics["cost"] = (self.metrics["total_dist"] / 1000) * COST_PER_KM + np.log(self.total_time) # trip cost in currency unit (e.g., USD)
    
    def calculate_profit(self):
        self.metrics["profit"] = (self.dist_to_goal / 1000 * REVENUE_PER_KM + self.time_to_goal * REVENUE_PER_SECOND) - self.metrics["cost"]

    def compute_score(self, weights, normalization_params):
        score = 0
        for metric, value in self.metrics.items():
            normalized_value = (
                (value - normalization_params[metric]["min"])
                / (normalization_params[metric]["max"] - normalization_params[metric]["min"])
                if normalization_params[metric]["max"] != normalization_params[metric]["min"]  # Avoid division by zero
                else 0
            )
            score += weights[metric] * normalized_value
        return score

    def calculate_all(self):
        self.calculate_co2_emission()
        self.calculate_energy_consumption()
        self.calculate_cost()
        self.calculate_profit()
