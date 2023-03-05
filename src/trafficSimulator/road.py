from scipy.spatial import distance

save_distance = 25.0
break_distance = 50.0
stop_distance = 5.0

class Road:
    def __init__(self, id, start, end, sim, max_speed = 13.83, right_of_way = True) :
        self.id = id
        self.start = start
        self.end = end
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
        self.vehicles = set()
        self.max_speed = max_speed
        self.has_right_of_way = right_of_way
        self.has_signal = False
        self.simulation = sim

    def add_vehicle(self, vehicle) :
        self.vehicles.add(vehicle)

    def remove_vehicle(self, vehicle) :
        if vehicle in self.vehicles :
            self.vehicles.remove(vehicle)

    def closest_distance(self) :
        min_distance = 100.0
        for car in self.simulation.cars :
            if car.current_road_index < len(car.path) and car.path[car.current_road_index] != self.id :
                min_distance = min(min_distance, distance.euclidean(car.get_position(), self.end))
        return min_distance

    def move_cars(self, dt = 0.01) :
        vehicle_array = list(self.vehicles)
        vehicle_array = sorted(vehicle_array, key = lambda car : car.x, reverse = True)
        if not self.has_right_of_way and not self.has_signal :
            if self.closest_distance() < save_distance :
                if len(vehicle_array) > 0 :
                    if vehicle_array[0].x >= self.length - break_distance :
                        vehicle_array[0].slowDown(self.max_speed * (self.length - stop_distance - vehicle_array[0].x) / (break_distance - stop_distance))
                    if vehicle_array[0].x >= self.length - stop_distance :
                        vehicle_array[0].stop()
            elif self.closest_distance() < 3.0 * save_distance:
                for vehicle in vehicle_array :
                    vehicle.speedUp(self.max_speed)
        else :
            if self.traffic_signal_state() :
                for vehicle in vehicle_array :
                    vehicle.speedUp(self.max_speed)
            elif len(vehicle_array) > 0 and self.has_signal :
                if vehicle_array[0].x >= self.length - self.signal.break_distance :
                    vehicle_array[0].slowDown(self.max_speed * (self.length - self.signal.stop_distance - vehicle_array[0].x) / (self.signal.break_distance - self.signal.stop_distance))
                if vehicle_array[0].x >= self.length - self.signal.stop_distance :
                    vehicle_array[0].stop()
        for i in range(len(vehicle_array)) :
            leader = None
            if i > 0 : leader = vehicle_array[i - 1]
            vehicle_array[i].move(dt = dt, leader = leader)

    def set_traffic_signal(self, signal, index):
        self.signal = signal
        self.signal_index = index
        self.has_signal = True

    def traffic_signal_state(self):
        if self.has_signal :
            return self.signal.get_current_state(self.signal_index)
        return True
        
