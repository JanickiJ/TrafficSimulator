inf = 1000000000

class Vertex :
    def __init__(self, position) : 
        self.x = position[0]
        self.y = position[1]
        self.neighbor_list = []
        self.distance_map = {}
        self.path_map = {}
        self.roads = []
        self.out_road_map = {}
        self.distance_vector = {}
        self.path_vector = {}

    def add_edge(self, vertex) :
        self.neighbor_list.append(vertex)

    def add_road(self, road) :
        self.roads.append(road)

    def add_out_road(self, road, vertex):
        self.out_road_map[vertex] = road

    def set_coincidence(self) :
        for road in self.roads :
            road.set_direction_roads(self.roads, self)

    def __eq__(self, other) :
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f"Vertex = ({self.x}, {self.y})"

    def update_vertex_distance(self, vertex, distance, direction = None):
        if (vertex.x, vertex.y) not in self.distance_map.keys():
            self.distance_map[(vertex.x, vertex.y)] = distance
            self.path_map[(vertex.x, vertex.y)] = direction
        elif self.distance_map[(vertex.x, vertex.y)] > distance:
            self.distance_map[(vertex.x, vertex.y)] = distance
            self.path_map[(vertex.x, vertex.y)] = direction

    def is_neighbor(self, other) :
        return other in self.neighbor_list
    
    def get_distance(self, v):
        return self.distance_map[(v.x, v.y)]
    
    def get_predecesor(self, v):
        return self.path_map[(v.x, v.y)]

    def update(self):
        for vertex in self.neighbor_list:
            for v in self.distance_map.keys():
                distance1 = vertex.distance_map[(v[0], v[1])]
                distance2 = self.out_road_map[vertex].expected_time
                self.update_vertex_distance(Vertex(v), distance1 + distance2, vertex)

    def get_next_hop(self, point, debug = False):
        if self.x == point[0] and self.y == point[1]:
            return False
        if debug:
            print(self, point, self.path_map[point])
            print(self.out_road_map[self.path_map[point]])
        return self.out_road_map[self.path_map[point]].id

    def print_distance_vector(self):
        for key in self.distance_map.keys():
            print(key, self.distance_map[key], self.path_map[key])


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
        self.vertex_map[start].add_out_road(road, self.vertex_map[finish])
        self.vertex_map[finish].add_road(road)

    def print(self):
        for vertex in self.vertex_map.values():
            print(vertex, vertex.out_road_map)

    def set_concidence(self) :
        for vertex in self.vertex_map.values() :
            vertex.set_coincidence()

    def get_distance(self, v_1, v_2):
        return v_1.get_distance(v_2)
    
    def get_predecesor(self, v_1, v_2):
        return v_1.get_predecesor(v_2)

    def print_distance_vectors(self, debug = True):
        if debug: print("=============================Distance vector=============================")
        for position, vertex in self.vertex_map.items():
            if debug: print(position, vertex)
            vertex.print_distance_vector()
            if debug: print()

    def floyd_warshall(self, debug = True) :
        # Floyd Warshall table initialization
        for vertex_1 in self.vertex_map.values():
            for vertex_2 in self.vertex_map.values():
                if vertex_1 == vertex_2:
                    vertex_1.update_vertex_distance(vertex_2, 0, vertex_1)
                elif vertex_1.is_neighbor(vertex_2):
                    distance = vertex_1.out_road_map[vertex_2].expected_time
                    vertex_1.update_vertex_distance(vertex_2, distance, vertex_2)
                else:
                    vertex_1.update_vertex_distance(vertex_2, inf, None)

        if debug: self.print_distance_vectors()

        for u in self.vertex_map.values():
            for vertex_1 in self.vertex_map.values():
                for vertex_2 in self.vertex_map.values():
                    distance_1 = self.get_distance(vertex_1, u)
                    distance_2 = self.get_distance(u, vertex_2)
                    predecesor = self.get_predecesor(vertex_1, u)
                    vertex_1.update_vertex_distance(vertex_2, distance_1 + distance_2, predecesor)

        if debug: self.print_distance_vectors()

    def update(self):
        for vertex in self.vertex_map.values():
            vertex.update()