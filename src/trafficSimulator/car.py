import numpy as np

class Car :
    def __init__(self, parameters = None, conf = {}, simulation = None) :
        self.simulation = simulation

        self.set_vehicle_parameters(parameters)

        for attr, val in conf.items():
            setattr(self, attr, val)

    def set_vehicle_parameters(self, parameters) :
        default = {
                    "id" : 0,
                    "length" : 5.0, 
                    "delta_s0" : 1.0, 
                    "break_reaction_time" : 0.3, 
                    "avarage_reaction_time" : 0.85, 
                    "stand_dev_reaction_time" : 0.15, 
                    "maximum_speed" : 16.6, 
                    "a_max" : 3.3, 
                    "b_max" : 6.25, 
                    "road_index" : 0, 
                    "path" : [],
                    "position" : 0
                  }
        
        if parameters == None :
            parameters = default
        
        if "id" not in parameters.keys() : parameters["id"] = default["id"]
        if "length" not in parameters.keys() : parameters["length"] = default["length"]
        if "delta_s0" not in parameters.keys() : parameters["delta_s0"] = default["delta_s0"]
        if "break_reaction_time" not in parameters.keys() : parameters["break_reaction_time"] = default["break_reaction_time"]
        if "avarage_reaction_time" not in parameters.keys() : parameters["avarage_reaction_time"] = default["avarage_reaction_time"]
        if "stand_dev_reaction_time" not in parameters.keys() : parameters["stand_dev_reaction_time"] = default["stand_dev_reaction_time"]
        if "maximum_speed" not in parameters.keys() : parameters["maximum_speed"] = default["maximum_speed"]
        if "a_max" not in parameters.keys() : parameters["a_max"] = default["a_max"]
        if "b_max" not in parameters.keys() : parameters["b_max"] = default["b_max"]
        if "road_index" not in parameters.keys() : parameters["road_index"] = default["road_index"]
        if "path" not in parameters.keys() : parameters["path"] = default["path"] 
        if "position" not in parameters.keys() : parameters["position"] = default["position"] 

        self.set_parameters(parameters)

        self.add_to_road()

    def add_to_road(self) :
        if self.current_road_index < len(self.path) :
            current_road = self.path[self.current_road_index]
            self.simulation.roads[current_road].add_vehicle(self)
        else :
            self.finish()

    def set_parameters(self, parameters) : 
        self.id = parameters["id"]        
        self.length = parameters["length"]
        self.s0 = self.length + parameters["delta_s0"]
        self.break_reaction_time = parameters["break_reaction_time"]    # czas potrzebny na przeniesienie nacisku na pedał hamulca na koła

        # czas reakcji waha się w zakresie od 0.7s do 1.0s
        self.T = self.break_reaction_time + max(0.0, np.random.normal(parameters["avarage_reaction_time"], parameters["stand_dev_reaction_time"])) 
        
        self.v_max = parameters["maximum_speed"]    # maksymalna prędkość (przyjęto ekwiwalent prędkości 60km/h wyrażoną w m/s)
        self._v_max = self.v_max
        self.a_max = parameters["a_max"]            # maksymalne przyspieszenie https://www.autocentrum.pl/nasze-pomiary/ranking-przyspieszenia/
        self.b_max = parameters["b_max"]            # maksymalne opóźnienie przy hamowaniu https://motofakty.pl/droga-hamowania-to-nie-wszystko-ile-miejsca-potrzeba-by-zatrzymac-auto/ar/c4-16232753

        self.path = parameters["path"]
        self.current_road_index = parameters["road_index"]

        self.x = parameters["position"]
        self.v = self.v_max     # pewnie będzie można zmienić na self.v = 0
        self.a = 0
        self.stopped = False
        self.finished = False

    def change_road(self, current_road) :
        self.x -= self.simulation.roads[current_road].length
        self.simulation.roads[current_road].remove_vehicle(self)
        self.current_road_index += 1
        self.add_to_road()

    def move(self, dt = 1.0, leader = None) :
        if self.finished :
            return
        self.x += self.v * dt + self.a * dt* dt / 2
        self.v = max(0.0, self.v + self.a * dt)
        
        follow_corection = 0

        # jeśeli pojazd podąża za kimś
        if leader :
            # print(self.id, ". leader.x =", leader.x, "self.x =", self.x)
            delta_x = leader.x - self.x - leader.length
            delta_v = self.v - leader.v

            follow_corection = (self.s0 + max(0, self.T * self.v + delta_v * self.v/(2 * np.sqrt(self.a_max * self.b_max)))) / delta_x
        # else :
        #     print(self.id, ". leader.x =", "None", "self.x =", self.x)

        self.a = self.a_max * (1 - (self.v / self.v_max)**4 - follow_corection**2)

        if self.stopped : 
            self.a = -self.b_max * self.v / self.v_max  

        current_road = self.path[self.current_road_index]
        if self.x > self.simulation.roads[current_road].length :
            self.change_road(current_road)

    def finish(self) :
        self.finished = True

    def stop(self) :
        self.stopped = True

    def start(self) :
        self.stopped = False

    def slowDown(self, v) :
        self.v_max = v

    def speedUp(self) :
        self.v_max = self._v_max  
