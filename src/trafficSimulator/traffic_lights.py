traffic_light_T = 30.0

class TrafficSignal:
    def __init__(self, roads, sim) :
        self.roads = roads
        self.state = [(False, True), (True, False)]
        self.state_index = 0
        self.stop_distance = 10.0
        self.T = 30.0
        self.t = 0
        self.simulation = sim
        self.init_properties()

    def init_properties(self) :
        max_speed = 5.0
        for i in range(len(self.roads)) :
            for r in self.roads[i] :
                self.simulation.roads[r].set_traffic_signal(self, i)
                max_speed = max(max_speed, self.simulation.roads[r].max_speed)
        self.break_distance = self.stop_distance + 1.8 * max_speed

    def update(self, dt) :
        self.t += dt
        if self.t > self.T :
            self.t = self.t - self.T
            self.state_index = (self.state_index + 1) % 2

    def get_current_state(self, type) :
        return self.state[self.state_index][type]
        