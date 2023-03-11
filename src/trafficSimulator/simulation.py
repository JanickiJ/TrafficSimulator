import time

import numpy as np

from src.trafficSimulator.car import Car
from src.trafficSimulator.curve import Curve
from src.trafficSimulator.road import Road


class Simulation:
    def __init__(self, speed=25):
        self.roads = {}
        self.cars = []
        self.traffic_lights = []
        self.speed = speed
        self.simulation_time = 0.0
        self.generator = None
        self.count = 0

    def create_car(self, conf, param):
        self.cars.append(Car(simulation=self, conf=conf, parameters=param))

    def set_vehicles(self, vehicles):
        for vehicle in vehicles:
            self.create_car(vehicle[0], vehicle[1])

    def create_road(self, start, end, id, speed_limit=13.83, right_of_way=True, control_point=None):
        if control_point:
            road = Curve(id, start, end, self, control_point, speed_limit=speed_limit, right_of_way=right_of_way)
        else:
            road = Road(id, start, end, self, speed_limit, right_of_way)
        self.roads[id] = road
        return road

    def set_roads(self, road_list):
        for road in road_list:
            self.create_road(**road)

    def set_generator(self, generator):
        self.generator = generator

    def set_lights(self, traffic_lights):
        self.traffic_lights = traffic_lights

    def run(self, steps):
        start = time.time()
        end = time.time()
        dt = 0
        for _ in range(steps):
            end = start
            start = time.time()
            dt = max(0.001, start - end)
            self.simulation_time += dt * self.speed
            for light in self.traffic_lights:
                light.update(dt * self.speed)
            for road in self.roads.values():
                road.move_cars(dt=dt * self.speed)
            if self.generator is not None:
                self.generator.generate(self.speed, self.simulation_time, dt)

    def can_add_car(self, road, position, length):
        # print(self.roads, road)
        for car in self.roads[road].vehicles:
            if np.abs(car.x - position) < 2.0 * (length + car.length):
                # print(False)
                return False
        self.count += 1
        # print(self.count, True)
        return True
