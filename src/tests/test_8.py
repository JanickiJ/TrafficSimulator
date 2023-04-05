from src.trafficSimulator.generator import Generator
from src.trafficSimulator.simulation import Simulation
from src.trafficSimulator.traffic_lights import TrafficSignal
from src.trafficSimulator.window import Window

def run_simulation(sim):
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()

def intensityFunction(t):
    return max(0.0, (200.0 - t) / 20.0)

def set_roads(sim):
    data =[
        ((0, 100), (100, 100), 1, 20.00, True, True, 1),
        ((100, 100), (0, 100), 2, 20.00, True, True, 1),
        ((100, 200), (100, 100), 3, 20.00, True, True, 1),
        ((100, 100), (100, 200), 4, 20.00, True, True, 1),
        ((100, 0), (100, 100), 5, 20.00, True, True, 1),
        ((100, 100), (100, 0), 6, 20.00, True, True, 1),
        ((200, 100), (100, 100), 7, 20.00, True, True, 1),
        ((100, 100), (200, 100), 8, 20.00, True, True, 1),
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5], "lines": x[6]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)

def set_traffic_light(sim):
    return [TrafficSignal([(1, 2), (6, 14)], sim)]      


def test1():
    """Fully symetrical crossroad.""" 
    sim = Simulation("TEST_8_1")
    set_roads(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, [1, 4]),
        (1, [1, 6]),
        (1, [1, 8]),
        (1, [3, 2]),
        (1, [3, 6]),
        (1, [3, 8]),
        (1, [5, 2]),
        (1, [5, 4]),
        (1, [5, 8]),
        (1, [7, 2]),
        (1, [7, 4]),
        (1, [7, 6]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.set_generator(gen)
    run_simulation(sim)

def runTests():
    test1()


if __name__ == "__main__":
    runTests()