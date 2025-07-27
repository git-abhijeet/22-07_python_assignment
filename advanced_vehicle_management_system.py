from datetime import datetime, timedelta


class Vehicle:
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage=0, fuel_type="Gasoline"):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.is_available = True
        self.mileage = mileage
        self.fuel_type = fuel_type
    
    def rent(self):
        if self.is_available:
            self.is_available = False
            return f"Vehicle {self.vehicle_id} rented successfully"
        return "Vehicle not available"
    
    def return_vehicle(self):
        if not self.is_available:
            self.is_available = True
            return f"Vehicle {self.vehicle_id} returned successfully"
        return "Vehicle was not rented"
    
    def calculate_rental_cost(self, days):
        return self.daily_rate * days
    
    def get_vehicle_info(self):
        return f"{self.year} {self.make} {self.model} - ID: {self.vehicle_id}"
    
    def get_fuel_efficiency(self):
        return 25.0


class Car(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, seating_capacity, transmission_type, has_gps, mileage=0, fuel_type="Gasoline"):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, fuel_type)
        self.seating_capacity = seating_capacity
        self.transmission_type = transmission_type
        self.has_gps = has_gps
    
    def get_vehicle_info(self):
        base_info = super().get_vehicle_info()
        return f"{base_info} - Seats: {self.seating_capacity}, Transmission: {self.transmission_type}, GPS: {self.has_gps}"
    
    def get_fuel_efficiency(self):
        if self.transmission_type.lower() == "automatic":
            return {"city_mpg": 25, "highway_mpg": 32}
        else:
            return {"city_mpg": 28, "highway_mpg": 35}


class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, engine_cc, bike_type, mileage=0, fuel_type="Gasoline"):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, fuel_type)
        self.engine_cc = engine_cc
        self.bike_type = bike_type
    
    def calculate_rental_cost(self, days):
        base_cost = super().calculate_rental_cost(days)
        if days < 7:
            return base_cost * 0.8
        return base_cost
    
    def get_vehicle_info(self):
        base_info = super().get_vehicle_info()
        return f"{base_info} - Engine: {self.engine_cc}cc, Type: {self.bike_type}"
    
    def get_fuel_efficiency(self):
        return 50.0


class Truck(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, cargo_capacity, license_required, max_weight, mileage=0, fuel_type="Diesel"):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, fuel_type)
        self.cargo_capacity = cargo_capacity
        self.license_required = license_required
        self.max_weight = max_weight
    
    def calculate_rental_cost(self, days):
        base_cost = super().calculate_rental_cost(days)
        return base_cost * 1.5
    
    def get_vehicle_info(self):
        base_info = super().get_vehicle_info()
        return f"{base_info} - Cargo: {self.cargo_capacity}kg, License: {self.license_required}, Max Weight: {self.max_weight}kg"
    
    def get_fuel_efficiency(self):
        return {"empty_mpg": 18, "loaded_mpg": 12}


if __name__ == "__main__":
    # Test Case 1: Basic vehicle creation and inheritance
    car = Car("CAR001", "Toyota", "Camry", 2023, 45.0, 5, "Automatic", True)
    motorcycle = Motorcycle("BIKE001", "Harley", "Street 750", 2022, 35.0, 750, "Cruiser")
    truck = Truck("TRUCK001", "Ford", "F-150", 2023, 85.0, 1200, "CDL-A", 5000)

    assert car.seating_capacity == 5
    assert motorcycle.engine_cc == 750
    assert truck.cargo_capacity == 1200
    print("Test Case 1: PASSED")

    # Test Case 2: Vehicle availability and rental logic
    assert car.is_available == True
    rental_result = car.rent()
    assert car.is_available == False
    assert "rented successfully" in rental_result.lower()

    return_result = car.return_vehicle()
    assert car.is_available == True
    print("Test Case 2: PASSED")

    # Test Case 3: Type-specific rental calculations
    car_cost = car.calculate_rental_cost(3)
    assert car_cost == 45.0 * 3

    bike_cost = motorcycle.calculate_rental_cost(5)
    expected_bike = 35.0 * 5 * 0.8
    assert abs(bike_cost - expected_bike) < 0.01

    truck_cost = truck.calculate_rental_cost(2)
    expected_truck = 85.0 * 2 * 1.5
    assert abs(truck_cost - expected_truck) < 0.01
    print("Test Case 3: PASSED")

    # Test Case 4: Polymorphism - treating all vehicles uniformly
    vehicles = [car, motorcycle, truck]
    total_fleet_value = 0
    for vehicle in vehicles:
        info = vehicle.get_vehicle_info()
        assert vehicle.make in info
        assert vehicle.model in info
        if hasattr(vehicle, 'seating_capacity'):
            assert str(vehicle.seating_capacity) in info
        elif hasattr(vehicle, 'engine_cc'):
            assert str(vehicle.engine_cc) in info
    print("Test Case 4: PASSED")

    # Test Case 5: Fuel efficiency calculations
    car_efficiency = car.get_fuel_efficiency()
    assert isinstance(car_efficiency, dict)
    assert 'city_mpg' in car_efficiency
    assert 'highway_mpg' in car_efficiency

    bike_efficiency = motorcycle.get_fuel_efficiency()
    assert isinstance(bike_efficiency, (int, float))
    assert bike_efficiency > 40

    truck_efficiency = truck.get_fuel_efficiency()
    assert isinstance(truck_efficiency, dict)
    assert 'empty_mpg' in truck_efficiency
    assert 'loaded_mpg' in truck_efficiency
    print("Test Case 5: PASSED")

    print("\nAll tests passed! Vehicle Management System is working correctly.")
    print(f"Car rental cost (3 days): ${car_cost}")
    print(f"Motorcycle rental cost (5 days): ${bike_cost}")
    print(f"Truck rental cost (2 days): ${truck_cost}")