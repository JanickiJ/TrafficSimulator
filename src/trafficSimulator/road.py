from scipy.spatial import distance

from src.trafficSimulator.generator import max_car_length
from queue import LifoQueue

# from generator import max_car_length

save_distance = 5.0
break_distance = 25.0
stop_distance = 10.0


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

    def closest_distance(self):
        min_distance = 100.0
        if self.do_set_coincident :
            for road in self.coincident_roads :
                for car in road.vehicle_array :
                    if car.current_road_index < len(car.path):
                        min_distance = min(min_distance, distance.euclidean(car.get_position(), self.end) - car.v / 1.8 - max_car_length)
                    break
        else :
            for car in self.simulation.cars:
                if car.current_road_index < len(car.path) and car.path[car.current_road_index] > self.id:
                    min_distance = min(min_distance, distance.euclidean(car.get_position(), self.end) - car.v / 1.8 - max_car_length)
        return min_distance

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

        if not self.has_right_of_way and not self.has_signal:
            # brak pierszeństwa przejazdu i sygnalizacji świetlnej
            if self.closest_distance() < 2.0 * save_distance:
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
    
    def set_coincident_roads(self, roads):
        self.do_set_coincident = True
        self.coincident_roads = []
        self.potential_coincident = []
        for road in roads:
            if road.id != self.id:
                if self.has_right_of_way:
                    if road.has_right_of_way:
                        if (self.end[0] - self.start[0]) * (road.end[1] - road.start[1]) - (self.end[1] - self.start[1]) * (road.end[0] - road.start[0]) > 0 :
                            self.coincident_roads.append(road)
                        elif (self.end[0] - self.start[0]) * (road.end[1] - road.start[1]) - (self.end[1] - self.start[1]) * (road.end[0] - road.start[0]) == 0 :
                            self.potential_coincident.append(road)
                else :
                    if road.has_right_of_way or (self.end[0] - self.start[0]) * (road.end[1] - road.start[1]) - (self.end[1] - self.start[1]) * (road.end[0] - road.start[0])  > 0 :
                        self.coincident_roads.append(road)
                    elif (self.end[0] - self.start[0]) * (road.end[1] - road.start[1]) - (self.end[1] - self.start[1]) * (road.end[0] - road.start[0])  == 0 :
                        self.potential_coincident.append(road)
        print(f"Road {self.id}", "coincident: ")
        for road in self.coincident_roads :
            print(road)
        print(f"Potential coincident: ")
        for road in self.potential_coincident :
            print(road)
        print()

        
    def __str__(self) :
        return f"Road {self.id}"