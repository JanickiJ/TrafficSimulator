from scipy.spatial import distance
from queue import LifoQueue
import numpy as np

from src.trafficSimulator.generator import max_car_length

# from generator import max_car_length

save_distance = 5.0
break_distance = 25.0
stop_distance = 15.0



def det_3(a,b,c):
    a_x, a_y = a
    b_x, b_y = b
    c_x, c_y = c
    matrix = np.array([[a_x, a_y, 1],
                      [b_x, b_y, 1],
                      [c_x, c_y, 1]])
    return np.linalg.det(matrix)


def detect_collision(source1, destination1, source2, destination2, debug = False) :
    # if debug: print(source1, destination1, source2, destination2, "\n", det_3(source1, destination1, source2), det_3(source1, destination1, destination2))
    return det_3(source1, destination1, source2) * det_3(source1, destination1, destination2) < 0 or destination1[0] == destination2[0] or destination1[1] == destination2[1]


class Road:
    def __init__(self, id, start, end, sim, max_speed=13.83, right_of_way=True, do_move = False):
        self.id = id
        self.start = start
        self.end = end
        self.end_ = end
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
        if do_move:
            dx, dy = 2.0 * self.angle_sin, -2.0 * self.angle_cos
            self.start = (self.start[0] - dx, self.start[1] - dy)
            self.end = (self.end[0] - dx, self.end[1] - dy)
        self.vehicles = set()
        self.max_speed = max_speed
        self.has_right_of_way = right_of_way
        self.has_signal = False
        self.simulation = sim
        self.vehicle_array = []
        self.expected_time = self.length / self.max_speed
        self.timeQueue = LifoQueue()
        self.right_roads = []
        self.ahead_roads = []
        self.left_roads = []
        for _ in range(10) :
            self.timeQueue.put(self.expected_time)
        self.do_set_coincident = False

    def add_vehicle(self, vehicle):
        self.vehicles.add(vehicle)

    def remove_vehicle(self, vehicle, dt):
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            if dt:
                old_dt = self.timeQueue.get()
                self.expected_time = (10.0 * self.expected_time - old_dt + dt) / 10.0
                self.timeQueue.put(dt)
    
    def get_car_move(self):
        for car in self.vehicle_array:
            return car.get_planned_move()
        return None
    
    def get_move_type(self, own_move) :
        # 0 - right
        # 1 - ahead
        # 2 - left
        for road in self.right_roads :
            if distance.euclidean(road.start, own_move[1]) < 10.0 :
                return 0
        for road in self.ahead_roads :
            if distance.euclidean(road.start, own_move[1]) < 10.0 :
                return 1
        return 2
    
    def avoid_collision(self, own_move, road) :
        other_move = road.get_car_move()
        if other_move:
            if detect_collision(own_move[0], own_move[1], other_move[0], other_move[1]):
                for car in road.vehicle_array:
                    if car.current_road_index < len(car.path) \
                        and distance.euclidean(car.get_position(), self.end) - car.v / 1.8 - max_car_length < 2 * save_distance :
                            return False
                    break
        return True
    
    def check_right(self, own_move, do_check_with = False) :
        for road in self.right_roads:
            if road.has_right_of_way or (not self.has_right_of_way and do_check_with):
                if not self.avoid_collision(own_move, road): return False
        return True

    def check_ahead(self, own_move, do_check_with = False):
        for road in self.ahead_roads:
            if road.has_right_of_way or (not self.has_right_of_way and do_check_with):
                if not self.avoid_collision(own_move, road): return False
        return True
    
    def check_left(self, own_move, do_check_with = False):
        for road in self.left_roads:
            if road.has_right_of_way or (not self.has_right_of_way and do_check_with):
                if not self.avoid_collision(own_move, road): return False
        return True
                
    
    def check_crossroad(self) :
        # True  -  can move
        # False -  cannot move
        own_move = self.get_car_move()
        if not own_move:
            return True
        move_type = self.get_move_type(own_move)
        if self.has_right_of_way:
            if move_type == 0:
                return True
            if move_type == 1:
                return self.check_right(own_move)
            if move_type == 2:
                return self.check_right(own_move) and self.check_ahead(own_move)
        else:
            if move_type == 0:
                return self.check_right(own_move) and self.check_ahead(own_move) and self.check_left(own_move)
            if move_type == 1:
                return self.check_right(own_move, do_check_with=True) and self.check_ahead(own_move) and self.check_left(own_move)
            if move_type == 2:
                return self.check_right(own_move, do_check_with=True) and self.check_ahead(own_move, do_check_with=True) and self.check_left(own_move)                   
            
    def speed_up_vehicles(self, speed):
        for vehicle in self.vehicle_array:
            vehicle.speedUp(speed)

    def stop_cars(self, break_distance, stop_distance):
        if len(self.vehicle_array) > 0:
            if self.vehicle_array[0].x >= self.length - break_distance:
                self.vehicle_array[0].slowDown(
                    self.max_speed * (self.length - stop_distance - self.vehicle_array[0].x) / (
                            break_distance - stop_distance))
            if self.vehicle_array[0].x >= self.length - stop_distance:
                self.vehicle_array[0].stop()

    def move_cars(self, dt=0.01):
        self.vehicle_array = sorted(list(self.vehicles), key=lambda car: car.x, reverse=True)

        if not self.has_signal:
            # brak pierszeństwa przejazdu i sygnalizacji świetlnej
            if not self.check_crossroad():
                self.stop_cars(break_distance, stop_distance)
            else :
                self.speed_up_vehicles(self.max_speed)
        else:
            if self.traffic_signal_state():
                self.speed_up_vehicles(self.max_speed)
            elif len(self.vehicle_array) > 0 and self.has_signal:
                self.stop_cars(self.signal.break_distance, self.signal.stop_distance)

        for i in range(len(self.vehicle_array)):
            leader = None
            if i > 0: leader = self.vehicle_array[i - 1]
            self.vehicle_array[i].move(dt=dt, leader=leader)

    def set_traffic_signal(self, signal, index):
        self.signal = signal
        self.signal_index = index
        self.has_signal = True

    def traffic_signal_state(self):
        if self.has_signal:
            return self.signal.get_current_state(self.signal_index)
        return True

    def get_angle(self, road) :
        vector_multiplication = (self.end[0] - self.start[0]) * (road.end[1] - road.start[1]) - (self.end[1] - self.start[1]) * (road.end[0] - road.start[0])
        angle_sin = vector_multiplication / np.sqrt(self.length ** 2 + road.length ** 2)
        return angle_sin


    def set_direction_roads(self, roads) :
        self.do_set_coincident = True
        roads = sorted(roads, key = lambda x: self.get_angle(x))
        index = 0
        for road in roads :
            if road.id != self.id:
                if index == 0 and self.get_angle(road) < 0: 
                    self.right_roads.append(road)
                    index += 1
                elif index <= 1 and self.get_angle(road) <= 0: 
                    self.ahead_roads.append(road)
                    index += 1
                else : 
                    self.left_roads.append(road)
        for road in self.right_roads:
            print("right:", road)
        for road in self.ahead_roads:
            print("ahead:", road)
        for road in self.left_roads:
            print("left:", road)
        print("\n\n")

    def __str__(self) :
        return f"Road {self.id}, {self.start}, {self.end}, {self.has_right_of_way}"