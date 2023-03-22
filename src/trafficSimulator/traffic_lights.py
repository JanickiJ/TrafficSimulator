traffic_light_T = 30.0

class TrafficSignal:
    def __init__(self, roads, sim, time_steps = [16.0, 18.0, 20.0, 36.0, 38.0, 40.0]) :
        self.roads = roads
        self.state = [(False, True), (True, False)]
        self.state_yellow = [(True, None, False, False, False, None), (False, False, None, True, None, False)]
        self.time_steps = time_steps
        self.state_index = 0
        self.stop_distance = 10.0
        self.T = 40.0
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

    def update_yellow(self, dt) :
        self.t += dt
        if self.t > self.time_steps[self.state_index] :
            if self.state_index == 5: self.t = self.t - self.T
            self.state_index = (self.state_index + 1) % 6

    def get_current_state(self, type) :
        return self.state[self.state_index][type]
    
    def get_current_state_yellow(self, type) :
        return self.state_yellow[type][self.state_index]
        