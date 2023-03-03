from scipy.spatial import distance


class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
        self.vehicles = set()

    def add_vehicle(self, vehicle) :
        self.vehicles.add(vehicle)

    def remove_vehicle(self, vehicle) :
        if vehicle in self.vehicles :
            self.vehicles.remove(vehicle)

    def move_cars(self, dt = 0.01) :
        vehicle_array = list(self.vehicles)
        vehicle_array = sorted(vehicle_array, key = lambda car : car.x, reverse = True)
        for i in range(len(vehicle_array)) :
            leader = None
            if i > 0 : leader = vehicle_array[i - 1]
            vehicle_array[i].move(dt = dt, leader = leader)
    
