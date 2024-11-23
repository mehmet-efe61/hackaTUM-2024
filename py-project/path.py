import numpy as np

class Path():

    def __init__(self, car, customer) -> None:
        self.car: dict = car
        self.customer: dict = customer
        self.distance = 0  # in meters
        self.travel_time = 0  # in seconds
        self.co2_emission = 0  # in grams
        self.energy_consumption = 0  # in joules
        self.trip_cost = 0  # in currency unit
        self.set_car_speed()
        self.calculate_all()
    
    def set_car_speed(self):
        speed = np.random.uniform(8.33, 13.89)  # speed in meters per second (m/s)
        self.car["speed"] = speed
    
    def calculate_distance(self):

        # Convert latitude and longitude from degrees to radians
        lat1 = np.radians(self.car["coordY"])
        lon1 = np.radians(self.car["coordX"])
        lat2 = np.radians(self.customer["coordY"])
        lon2 = np.radians(self.customer["coordX"])

        # Radius of the Earth in meters
        R = 6371000

        # Haversine formula to calculate the distance
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        self.distance = R * c  # distance in meters (m)
    
    def calculate_travel_time(self):    
        self.travel_time = self.distance / self.car["speed"]  # travel time in seconds (s)
    
    def calculate_co2_emission(self): #TODO: Use a better formula to calculate CO2 emission
        self.co2_emission = self.travel_time * self.car["co2_emission_per_second"]  # CO2 emission in grams (g)
    
    def calculate_energy_consumption(self): #TODO: Use a better formula to calculate energy consumption
        self.energy_consumption = self.travel_time * self.car["energy_consumption_per_second"]  # energy consumption in joules (J)

    def calculate_trip_cost(self):
        self.trip_cost = (self.distance / 1000) * self.car["cost_per_km"]  # trip cost in currency unit (e.g., USD)
    
    def calculate_all(self):
        self.calculate_distance()
        self.calculate_travel_time()
        self.calculate_co2_emission()
        self.calculate_energy_consumption()
        self.calculate_trip_cost()
