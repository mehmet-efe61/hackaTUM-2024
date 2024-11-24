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
        total_time = (self.dist_to_customer + self.dist_to_goal) / self.vehicle["vehicleSpeed"]
        self.metrics = {
            "total_dist": self.dist_to_customer + self.dist_to_goal,  # in meters
            "total_time": total_time,  # in seconds
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
        self.metrics["co2_emission"] = self.metrics["total_time"] * CO2_EMISSION_PER_SECOND # CO2 emission in grams (g)
    
    def calculate_energy_consumption(self): #TODO: Use a better formula to calculate energy consumption
        self.metrics["energy_consumption"] = self.metrics["total_time"] * ENERGY_CONSUMPTION_PER_SECOND  # energy consumption in joules (J)

    def calculate_cost(self):
        self.metrics["cost"] = (self.metrics["total_dist"] / 1000) * COST_PER_KM  # trip cost in currency unit (e.g., USD)
    
    def calculate_profit(self):
        self.metrics["profit"] = (self.dist_to_goal / 1000 * REVENUE_PER_KM + self.time_to_goal * REVENUE_PER_SECOND) - self.metrics["cost"]

    def compute_score(self, weights):
        score = 0
        normalized_metrics = self.normalize_metrics()
        for metric, value in normalized_metrics.items():
            score += weights[metric] * value
        return score

    def normalize_metrics(self):
        normalized_metrics = {}
        for metric, value in self.metrics.items():
            if metric == "total_dist":
                normalized_metrics[metric] = value / 10000 
            elif metric == "total_time":
                normalized_metrics[metric] = value / 3600  
            elif metric == "co2_emission":
                normalized_metrics[metric] = value / 1000  
            elif metric == "energy_consumption":
                normalized_metrics[metric] = value / 1000   
            elif metric == "cost":
                normalized_metrics[metric] = value / 100  
            elif metric == "profit":
                normalized_metrics[metric] = value / 100  
        return normalized_metrics

    def calculate_all(self):
        self.calculate_co2_emission()
        self.calculate_energy_consumption()
        self.calculate_cost()
        self.calculate_profit()
