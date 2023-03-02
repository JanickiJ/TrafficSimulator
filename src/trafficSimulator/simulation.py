from .road import Road


class Simulation:
    def __init__(self):
        self.roads = []

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def set_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def run(self, steps):
        pass
