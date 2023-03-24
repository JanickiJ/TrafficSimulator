from src.statistics.mongo import Mongo

from src.trafficSimulator.parameters import SAVE_RESULTS_IN_DB

class Measurements:
    def __init__(self):
        self.mongo = Mongo()

    def save_measurements(self, simulation):
        print("=== RESULTS ===")
        print(simulation)
        print("======")
        for car in simulation.cars:
            print(car)
            print("======")
        if SAVE_RESULTS_IN_DB:
            db_simulation = self.mongo.save_simulation(simulation.map_name, simulation.speed)
            print()
            for car in simulation.cars:
                self.mongo.save_car(car.id, car.v_max, car.road_times, db_simulation.inserted_id)

