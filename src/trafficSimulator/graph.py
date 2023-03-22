class Vertex :
    def __init__(self, position) : 
        self.x = position[0]
        self.y = position[1]
        self.neighbor_list = []
        self.distance_map = {}
        self.path_map = {}
        self.roads = []

    def add_edge(self, vertex) :
        self.neighbor_list.append(vertex)

    def add_road(self, road) :
        self.roads.append(road)

    def set_coincidence(self) :
        print(self.roads)
        for road in self.roads :
            road.set_direction_roads(self.roads)

class Graph :
    def __init__(self) :
        self.vertex_map = {}

    def add_vertex(self, position) :
        if position not in self.vertex_map.keys() :
            self.vertex_map[position] = Vertex(position=position)

    def add_edge(self, start, finish, road) :
        self.add_vertex(start)
        self.add_vertex(finish)
        self.vertex_map[start].add_edge(self.vertex_map[finish])
        self.vertex_map[finish].add_road(road)

    def set_concidence(self) :
        for vertex in self.vertex_map.values() :
            vertex.set_coincidence()
        # sys.exit()

    def floyd_warshall(self) :
        pass

    