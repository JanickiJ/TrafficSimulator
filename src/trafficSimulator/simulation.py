import sys
import time

import numpy as np
import pygame

from src.statistics.measurements import Measurements
from src.trafficSimulator.parameters import default_speed_limit, simulation_debug
from src.trafficSimulator.car import Car
from src.trafficSimulator.curve import Curve
from src.trafficSimulator.road import Road
from src.trafficSimulator.graph import Graph

# from measurements import Measurements
# from parameters import default_speed_limit, simulation_debug
# from car import Car
# from curve import Curve
# from road import Road
# from graph import Graph


class Simulation:
    def __init__(self, map_name, speed=2):
        self.map_name = map_name
        self.roads = {}
        self.cars = []
        self.traffic_lights = []
        self.speed = speed
        self.generator = None
        self.count = 0
        self.distance_vector_initiate = False
        self.start_time = time.time()
        self.previous = time.time()
        self.measurement_module = Measurements()
        self.graph = Graph()

    def create_car(self, conf, param):
        """Create new car"""
        self.cars.append(Car(simulation=self, conf=conf, parameters=param))

    def set_vehicles(self, vehicles):
        """Create new cars basing on array of parameter maps"""
        for vehicle in vehicles:
            self.create_car(vehicle[0], vehicle[1])

    def create_road(self, start, end, id, speed_limit=default_speed_limit, right_of_way=True, control_point=None, do_move = False):
        """Create new road with given parameters"""
        if control_point:
            road = Curve(id, start, end, self, control_point, speed_limit=speed_limit, right_of_way=right_of_way)
        else:
            road = Road(id, start, end, self, speed_limit, right_of_way, do_move)
        self.roads[id] = road
        self.graph.add_edge(start, end, road)
        return road

    def set_roads(self, road_list, do_set_coincident = False):
        """Create new road for an array of parameter maps"""
        for road in road_list:
            self.create_road(**road)
        if do_set_coincident: self.set_coincidence()

    def set_generator(self, generator):
        """Set car generator"""
        self.generator = generator

    def set_lights(self, traffic_lights):
        """Set lights"""
        self.traffic_lights = traffic_lights

    def update_roads(self, dt):
        for road in self.roads.values():
            road.move_cars(dt=dt)

    def update_lights(self, dt):
        for light in self.traffic_lights:
            light.update_yellow(dt)

    def update_generator(self, dt):
        if self.generator:
            self.generator.generate(time.time() - self.start_time, dt)

    def upadate_graph(self, dt):
        if self.distance_vector_initiated:
            self.graph.update()


    def run(self, steps, debug = simulation_debug):
        """Run certain number of steps"""
        start = time.time()
        for i in range(steps):
            end = start
            if i == 0 : end = self.previous
            start = time.time()
            if debug: print(start, end)
            dt = (start - end) * self.speed
            if debug: print(dt)
            self.update_lights(dt)
            self.update_roads(dt)
            self.update_generator(dt)
            self.upadate_graph(dt)            
        self.previous = time.time()
        if self.finished():
            self.measurement_module.save_measurements(self)
            pygame.quit()
            sys.exit()

    def can_add_car(self, road, position, length, debug = simulation_debug):
        """Check if adding car on a certain position will not cause collision"""
        if debug: print("Road:", road)
        for car in self.roads[road].vehicles:
            if debug: print(car.x ,"=?=",position, np.abs(car.x - position) < 2.0 * (length + car.length))
            if np.abs(car.x - position) < 2.0 * (length + car.length):
                return False
        self.count += 1
        return True

    def finished(self):
        """Check if simulation is not finished"""
        if not self.cars:
            return False
        for car in self.cars:
            if not car.finished:
                return False
        return True
    
    def set_coincidence(self, debug = simulation_debug):
        """Set coincident roads (crossroad awareness)"""
        self.graph.set_concidence()
        if debug: self.graph.print()

    def init_distance_vector(self):
        """Initiate distance vectors in the road graph"""
        self.distance_vector_initiated = True
        self.graph.floyd_warshall()
        

