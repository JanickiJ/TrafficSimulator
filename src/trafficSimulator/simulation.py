import sys
import time

import numpy as np
import pygame

from src.statistics.measurements import Measurements
from src.trafficSimulator.car import Car
from src.trafficSimulator.curve import Curve
from src.trafficSimulator.road import Road
from src.trafficSimulator.graph import Graph


class Simulation:
    def __init__(self, map_name, speed=2):
        self.map_name = map_name
        self.roads = {}
        self.cars = []
        self.traffic_lights = []
        self.speed = speed
        self.generator = None
        self.count = 0
        self.start_time = time.time()
        self.previous = time.time()
        self.measurement_module = Measurements()
        self.graph = Graph()

    def create_car(self, conf, param):
        self.cars.append(Car(simulation=self, conf=conf, parameters=param))

    def set_vehicles(self, vehicles):
        for vehicle in vehicles:
            self.create_car(vehicle[0], vehicle[1])

    def create_road(self, start, end, id, speed_limit=13.83, right_of_way=True, control_point=None, do_move = False):
        if control_point:
            road = Curve(id, start, end, self, control_point, speed_limit=speed_limit, right_of_way=right_of_way)
        else:
            road = Road(id, start, end, self, speed_limit, right_of_way, do_move)
        self.roads[id] = road
        self.graph.add_edge(start, end, road)
        return road

    def set_roads(self, road_list, do_set_coincident = False):
        for road in road_list:
            self.create_road(**road)
        if do_set_coincident: self.set_coincidence()

    def set_generator(self, generator):
        self.generator = generator

    def set_lights(self, traffic_lights):
        self.traffic_lights = traffic_lights

    def run(self, steps):
        start = time.time()
        for i in range(steps):
            end = start
            if i == 0 : end = self.previous
            start = time.time()
            print(start, end)
            # dt = max(0.1, (start - end) * self.speed)
            dt = (start - end) * self.speed
            print(dt)
            for light in self.traffic_lights:
                light.update(dt)
            for road in self.roads.values():
                road.move_cars(dt=dt)
            if self.generator:
                self.generator.generate(time.time() - self.start_time, dt)
        self.previous = time.time()
        if self.finished():
            self.measurement_module.save_measurements(self)
            pygame.quit()
            sys.exit()

    def can_add_car(self, road, position, length):
        for car in self.roads[road].vehicles:
            if np.abs(car.x - position) < 2.0 * (length + car.length):
                return False
        self.count += 1
        return True

    def finished(self):
        if not self.cars:
            return False
        for car in self.cars:
            if not car.finished:
                return False
        return True
    
    def set_coincidence(self):
        self.graph.set_concidence()

