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
        self.count = 0

    def create_car(self, conf, param) :
        self.cars.append(Car(simulation=self, conf=conf, parameters=param))

    def set_vehicles(self, vehicles) :
        for vehicle in vehicles:
            self.create_car(vehicle[0], vehicle[1])

    def create_road(self, start, end, id, speed_limit = 13.83):
        road = Road(start, end, speed_limit)
        self.roads[id] = road
        return road

    def set_roads(self, road_list):
        for road in road_list:
            print(road)
            if len(road) > 3 : #if road has a special speed limit
                self.create_road(road[0], road[1], road[2], road[3])
            else :
                self.create_road(road[0], road[1], road[2])

    def set_generator(self, generator) :
        self.generator = generator

    def run(self, steps) :
        start = time.time()
        end = time.time()
        dt = 0
        for _ in range(steps) :
            end = start
            start = time.time()            
            dt = max(0.001, start - end)
            self.simulation_time += dt * self.speed
            for i in range(1000000) :
                i += 1
            for road in self.roads.values() :
                road.move_cars(dt = dt * self.speed)
            if self.generator != None :
                self.generator.generate(self.speed, self.simulation_time, dt)
            
    def can_add_car(self, road, position, length) :
        # print(self.roads, road)
        for car in self.roads[road].vehicles :
            if np.abs(car.x - position) < 2.0 * (length + car.length) :
                # print(False)
                return False
        self.count += 1
        # print(self.count, True)
        return True
            
