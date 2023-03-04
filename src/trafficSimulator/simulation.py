from .road import Road
from .car import Car
import time
import numpy as np


class Simulation:
    def __init__(self, speed = 100):
        self.roads = {}
        self.cars = []
        self.speed = speed
        self.simulation_time = 0.0
        self.generator = None

    def create_car(self, conf, param) :
        self.cars.append(Car(simulation=self, conf=conf, parameters=param))

    def set_vehicles(self, vehicles) :
        for vehicle in vehicles:
            self.create_car(vehicle[0], vehicle[1])

    def create_road(self, start, end, id):
        road = Road(start, end)
        self.roads[id] = road
        return road

    def set_roads(self, road_list):
        for road in road_list:
            print(road)
            self.create_road(road[0], road[1], road[2])

    def set_generator(self, generator, intensityFuntion) :
        self.generator = generator
        self.intensity_function = intensityFuntion

    def run(self, steps) :
        start = time.time()
        end = time.time()
        dt = 0
        for _ in range(steps) :
            end = start
            start = time.time()            
            dt = max(0.001, start - end)
            self.simulation_time += dt
            for i in range(1000000) :
                i += 1
            for road in self.roads.values() :
                road.move_cars(dt = dt * self.speed)
            if self.generator != None and np.random.uniform(0, 1.0) <= self.speed * self.intensity_function(self.simulation_time) * dt : 
                self.generator.generateCars(1)
            
            
