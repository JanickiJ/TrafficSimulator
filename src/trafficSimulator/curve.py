import math

from src.trafficSimulator.parameters import curve_number
from src.trafficSimulator.road import Road

class Curve(Road):
    def __init__(self, id, start, end, sim, control_point, speed_limit=None, right_of_way=None):
        super().__init__(id, start, end, sim, max_speed=speed_limit, right_of_way=right_of_way)
        self.control_point = control_point
        self.bezier_points = self.get_curve_points(curve_number)
        self.length = self.distance_between_points(self.bezier_points)
        self.roads_substitute = self.as_roads(curve_number)

    @staticmethod
    def distance_between_points(points):
        distance = 0
        for idx, point in enumerate(points):
            if idx < len(points) - 1:
                distance += math.dist(point, points[idx + 1])
        return distance

    def get_curve_points(self, resolution=10):
        if (self.start[0] - self.end[0]) * (self.start[1] - self.end[1]) == 0:
            return [self.start, self.end]

        path = []

        for i in range(resolution + 1):
            t = i / resolution
            x = (1 - t) ** 2 * self.start[0] + 2 * (1 - t) * t * self.control_point[0] + t ** 2 * self.end[0]
            y = (1 - t) ** 2 * self.start[1] + 2 * (1 - t) * t * self.control_point[1] + t ** 2 * self.end[1]
            path.append((x, y))
        return path

    def get_y(self, x):
        closest_point = min(self.get_curve_points(), key=lambda point: abs(point[0] - x))
        return closest_point[1]

    def as_roads(self, resolution=10):
        roads = []
        points = self.get_curve_points(resolution)
        for i, point in enumerate(points):
            if i < len(points) - 1:
                roads.append(Road(-1, point, points[i + 1], None))
        return roads

    def get_vehicle_current_road_substitute(self, x):
        for road in self.roads_substitute:
            x -= road.length
            if x < 0:
                return road

    def get_road_substitute_start_length(self, road):
        length = 0
        for road_substitute in self.roads_substitute:
            if road == road_substitute:
                return length
            length += road_substitute.length
