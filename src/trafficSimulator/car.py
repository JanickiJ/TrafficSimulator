from scipy.spatial import distance
from time import time

import numpy as np
import pygame

from src.trafficSimulator.parameters import max_car_length, max_vehicle_width, save_distance, stop_distance, default_car_parameters, debug_car
# from parameters import max_car_length, max_vehicle_width, save_distance, stop_distance, default_car_parameters, debug_car

class Car:
    def __init__(self, parameters=None, conf={}, simulation=None):
        """Class representing car"""
        self.register_path = []
        self.simulation = simulation
        self.set_vehicle_parameters(parameters)
        self.road_times = [time()]
        self.count = 0

        for attr, val in conf.items():
            setattr(self, attr, val)

    def set_vehicle_parameters(self, parameters):
        """Setting default vehicle parameters"""
        default = default_car_parameters

        if parameters == None:
            parameters = default

        if "id" not in parameters.keys(): parameters["id"] = default["id"]
        if "length" not in parameters.keys(): parameters["length"] = default["length"]
        if "width" not in parameters.keys(): parameters["width"] = default["width"]
        if "delta_s0" not in parameters.keys(): parameters["delta_s0"] = default["delta_s0"]
        if "break_reaction_time" not in parameters.keys(): parameters["break_reaction_time"] = default[
            "break_reaction_time"]
        if "avarage_reaction_time" not in parameters.keys(): parameters["avarage_reaction_time"] = default[
            "avarage_reaction_time"]
        if "stand_dev_reaction_time" not in parameters.keys(): parameters["stand_dev_reaction_time"] = default[
            "stand_dev_reaction_time"]
        if "maximum_speed" not in parameters.keys(): parameters["maximum_speed"] = default["maximum_speed"]
        if "a_max" not in parameters.keys(): parameters["a_max"] = default["a_max"]
        if "b_max" not in parameters.keys(): parameters["b_max"] = default["b_max"]
        if "road_index" not in parameters.keys(): parameters["road_index"] = default["road_index"]
        if "path" not in parameters.keys(): parameters["path"] = default["path"]
        if "position" not in parameters.keys(): parameters["position"] = default["position"]

        self.set_parameters(parameters)

        self.add_to_road()
    
    def add_to_road(self, debug = debug_car):
        """Metohd responsible for registring vehicle as present on a certain road"""
        if self.current_road_index < len(self.path) and self.path[0] != False:
            current_road = self.path[self.current_road_index]
            self.simulation.roads[current_road].add_vehicle(self)
            self.slowDown(self.simulation.roads[current_road].max_speed)
            if debug: print(self.register_path)
        else:
            self.finish()

    def set_parameters(self, parameters):
        """Setting vehicle parameters"""
        self.id = parameters["id"]
        self.length = min(max_car_length, parameters["length"])
        self.width = min(max_vehicle_width, parameters["width"])
        self.s0 = self.length + parameters["delta_s0"]
        self.break_reaction_time = parameters[
            "break_reaction_time"]  # czas potrzebny na przeniesienie nacisku na pedał hamulca na koła

        # czas reakcji waha się w zakresie od 0.7s do 1.0s
        self.T = self.break_reaction_time + max(0.0, np.random.normal(parameters["avarage_reaction_time"],
                                                                      parameters["stand_dev_reaction_time"]))

        self.v_max = parameters[
            "maximum_speed"]  # maksymalna prędkość (przyjęto ekwiwalent prędkości 60km/h wyrażoną w m/s)
        self._v_max = self.v_max
        self.a_max = parameters[
            "a_max"]  # maksymalne przyspieszenie https://www.autocentrum.pl/nasze-pomiary/ranking-przyspieszenia/
        self.b_max = parameters[
            "b_max"]  # maksymalne opóźnienie przy hamowaniu https://motofakty.pl/droga-hamowania-to-nie-wszystko-ile-miejsca-potrzeba-by-zatrzymac-auto/ar/c4-16232753

        if isinstance(parameters["path"], tuple) and len(parameters["path"]) > 2:
            start_road = parameters["path"][0]
            self.end_point = parameters["path"][1]
            next_hop = self.simulation.roads[start_road].vertex.get_next_hop(self.end_point)
            self.dynamic = True
            self.path = [start_road, next_hop]
            self.current_road_index = 0
        else:
            self.dynamic = False
            self.path = parameters["path"]
            self.current_road_index = parameters["road_index"]

        self.x = parameters["position"]
        self.v = 0
        self.a = 0
        self.stopped = False
        self.slowedDown = False
        self.finished = False
        self.counter = 0
        self.register_path.append(self.path[0])

    def find_next_hop(self):
        """Finding next road to choose"""
        """It's always done one step forward"""
        next_hop = None
        if self.path[1] != False:
            next_hop = self.simulation.roads[self.path[1]].vertex.get_next_hop(self.end_point)
        self.register_path.append(next_hop)
        self.path = [self.path[1], next_hop]

    def actualize_x(self, current_road):
        """Actualize vehicle position on new road"""
        self.x -= self.simulation.roads[current_road].length
        self.x = max(-0.25 * self.length, self.x)

    def remove_from_road(self, current_road):
        """Passing information about removing vehicle from current road"""
        """with information about time of passing this particular road"""
        self.simulation.roads[current_road].remove_vehicle(self, dt = self.road_times[-1] - self.road_times[-2], index = self.count)

    def change_road(self, current_road):
        """Registering road change (time fo trevel, next_hop)"""
        if self.handle_potential_leader():
            return
        self.actualize_x(current_road)
        self.road_times.append(time())
        self.remove_from_road(current_road)
        if self.dynamic:
            self.find_next_hop()
        else:
            self.current_road_index += 1
        self.count += 1
        self.add_to_road()

    def get_position(self):
        """Get current position of the vehicle on the map (cartesian plain)"""
        r = self.path[self.current_road_index]
        road = self.simulation.roads[r]
        return ((road.end[0] * self.x + road.start[0] * (road.length - self.x)) / road.length,
                (road.end[1] * self.x + road.start[1] * (road.length - self.x)) / road.length)

    def detect_potential_leader(self):
        """Detecting potential collision before choosing new road"""
        if self.current_road_index + 1 < len(self.path) and self.path[self.current_road_index + 1] != False:
            next_road_idx = self.path[self.current_road_index + 1]
            next_road = self.simulation.roads[next_road_idx]
            if len(next_road.vehicle_array) > 0:
                return next_road.vehicle_array[-1]
        return None
    
    def handle_potential_leader(self):
        """Handle situation when potential leader was detected"""
        potential_leader = self.detect_potential_leader()
        if potential_leader:
            if potential_leader.x < self.length + save_distance: 
                self.stop()
                return True
        return False

    def move(self, dt=1.0, leader=None):
        """Actualize current vehicle position, speed and acceleration"""
        if self.finished:
            return
        dx = max(0.0, self.v * dt + self.a * dt * dt / 2)
        self.x += dx
        self.v = max(0.0, self.v + self.a * dt)

        follow_correction = 0

        potential_leader = self.detect_potential_leader()
        # jeśeli pojazd podąża za kimś
        if leader:
            delta_x = leader.x - self.x - leader.length
            delta_v = self.v - leader.v
            follow_correction = (self.s0 + max(0, self.T * self.v + delta_v * self.v / (
                    2 * np.sqrt(self.a_max * self.b_max)))) / delta_x
        elif potential_leader:
            delta_x = potential_leader.x + self.simulation.roads[
                self.path[self.current_road_index]].length - self.x - potential_leader.length
            if delta_x < save_distance + self.length : delta_x = self.simulation.roads[self.path[self.current_road_index]].length - self.x - stop_distance
            delta_v = self.v - potential_leader.v
            follow_correction = (self.s0 + max(0, self.T * self.v + delta_v * self.v / (
                    2 * np.sqrt(self.a_max * self.b_max)))) / delta_x
        if self.v > self.v_max:
            delta_x = 2 * self.length
            delta_v = self.v - self.v_max
            follow_correction = (self.s0 + max(0, self.T * self.v + delta_v * self.v / (
                    2 * np.sqrt(self.a_max * self.b_max)))) / delta_x
        if self.v_max == 0.0:
            self.a = -self.a_max
        else:
            self.a = self.a_max * (1 - (self.v / self.v_max) ** 4 - follow_correction ** 2)

        if self.stopped:
            if self.v_max == 0.0:
                self.a = -self.a_max
            else:
                self.a = -self.b_max * self.v / self.v_max

        current_road = self.path[self.current_road_index]
        if self.x > self.simulation.roads[current_road].length - 0.75 * self.length:
            self.x = self.simulation.roads[current_road].length - 0.75 * self.length
        if self.x >= self.simulation.roads[current_road].length - 0.75 * self.length:
            self.change_road(current_road)

    def finish(self, debug = debug_car):
        """Signalize travel end for the vehicle"""
        self.finished = True
        if debug: print(self.register_path)

    def stop(self):
        """Stop the car"""
        if self.x < self.simulation.roads[self.path[self.current_road_index]].length - 2.0 * save_distance / 3.0 :
            self.stopped = True

    def stop_cond(self):
        # dorzucić warunki
        self.stop()

    def start(self):
        """Start the car"""
        self.stopped = False

    def slowDown(self, v):
        """Slow down to given speed"""
        self.slowedDown = True
        self.v_max = max(0.0, v)

    def slow_down_cond(self, v):
        # dorzucić warunki
        self.slowDown(v)

    def speedUp(self, v):
        """Speeding up to given speed"""
        self.start()
        self.slowedDown = False
        self.v_max = min(v, self._v_max)

    def get_planned_move(self) :
        """Get planned move (information where the vehicle will go after the nearest crossroad)"""
        if self.current_road_index + 1 < len(self.path) and self.path[self.current_road_index] != False and self.path[self.current_road_index + 1] != False:
            source = self.simulation.roads[self.path[self.current_road_index]].start
            destination = self.simulation.roads[self.path[self.current_road_index + 1]].end
            return (source, destination)
        return None
