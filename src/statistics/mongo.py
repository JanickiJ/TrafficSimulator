import pymongo as pymongo


class Mongo:
    PROD_DB_URL = "mongodb+srv://traffic-simulator:traffic-simulator@cluster0.nckdlwd.mongodb.net/?retryWrites=true&w=majority"

    def __init__(self, ):
        client = pymongo.MongoClient(self.PROD_DB_URL)
        db = client.TrafficSimulator
        self.simulations_collection = db.simulations
        self.cars_collection = db.cars

    def get_simulations(self, simulation_id=None):
        if simulation_id:
            return list(self.simulations_collection.find({"id": {"$eq": simulation_id}}))
        return list(self.simulations_collection.find())

    def get_cars(self, car_id=None, simulation_id=None):
        if car_id:
            return list(self.cars_collection.find({"id": {"$eq": car_id}}))
        if simulation_id:
            return list(self.cars_collection.find({"simulationId": {"$eq": simulation_id}}))
        return list(self.cars_collection.find())

    def save_simulation(self, map_name, speed):
        """simulation stats can be added, like medium v of every vehicle"""
        return self.simulations_collection.insert_one({"mapName": map_name,
                                                       "speed": speed})

    def save_car(self, car_id, maximum_speed, road_times, simulation_id):
        """car stats can be added, like medium v """
        return self.cars_collection.insert_one({"simulationId": simulation_id,
                                                "carId": car_id,
                                                "maximum_speed": maximum_speed,
                                                "roadTimes": road_times})
