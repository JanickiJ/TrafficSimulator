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
        ((300, 100), (160, 100), 1, 20.00, True, True, 2),
        ((0, 100), (160, 100), 2, 20.00, True, True, 2),
        ((180, 60), (0, 60), 3, 13.83, True, True, 1),
        ((220, 55), (180, 60), 4, 13.83, True, True, 1),
        ((300, 30), (220, 55), 5, 13.83, True, True, 1),
        ((180, 60), (160, 100), 6, 13.83, True, True, 1),
        ((160, 130), (300, 130), 7, 25.00, True, True, 2),
        ((0, 180), (300, 180), 8, 40.0, True, True, 2),
        ((300, 180), (0, 180), 9, 40.0, True, True, 2),
        ((160, 100), (160, 140), 10, 16.66, True, True, 1),
        ((160, 100), (0, 100), 11, 20.00, True, True, 2),
        ((160, 100), (300, 100), 12, 20.00, True, True, 2),
        ((0, 140), (160, 140), 13, 13.83, False, False, 1),
        ((160, 140), (160, 180), 14, 13.83, True, True, 1)
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5], "lines": x[6]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)
    sim.set_lights(set_traffic_light(sim))

def set_roads_2(sim):
    data =[
        ((300, 100), (160, 100), 1, 20.00, True, True, 2),
        ((0, 100), (160, 100), 2, 20.00, True, True, 2),
        ((180, 60), (0, 60), 3, 13.83, True, True, 1),
        ((220, 55), (180, 60), 4, 13.83, True, True, 1),
        ((300, 30), (220, 55), 5, 13.83, True, True, 1),
        ((180, 60), (160, 100), 6, 13.83, True, True, 1),
        ((160, 130), (300, 130), 7, 25.00, True, True, 2),
        ((0, 180), (300, 180), 8, 40.0, True, True, 2),
        ((300, 180), (0, 180), 9, 40.0, True, True, 2),
        ((160, 100), (160, 140), 10, 16.66, True, True, 2),
        ((160, 100), (0, 100), 11, 20.00, True, True, 2),
        ((160, 100), (300, 100), 12, 20.00, True, True, 2),
        ((0, 140), (160, 140), 13, 13.83, False, False, 1),
        ((160, 140), (160, 180), 14, 13.83, True, True, 2)
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5], "lines": x[6]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)
    sim.set_lights(set_traffic_light(sim))


def set_traffic_light(sim):
    return [TrafficSignal([(1, 2), (6, 14)], sim)]      


def test1():
    """Road lines tests - pararell to X-axis and Y-axis""" 
    sim = Simulation("TEST_7_1")
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
        (1, (5, (0, 60), True)),
        (1, (8, (0, 180), True)),
        (1, (4, (0, 60), True)),
        (1, (6, (160, 180), True)),
        (1, [3]),
        (1, [7]),
        (1, (13, (160, 180), True)),
        (1, (2, (300, 100), True)),
        (1, (2, (160, 180), True)),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)

def test2():
    """Road lines tests - different angles""" 
    sim = Simulation("TEST_7_2")
    set_roads_2(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, (5, (0, 60), True)),
        (1, (8, (0, 180), True)),
        (1, (4, (0, 60), True)),
        (1, (6, (160, 180), True)),
        (1, [3]),
        (1, [7]),
        (1, (13, (160, 180), True)),
        (1, (2, (300, 100), True)),
        (1, (2, (160, 180), True)),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)


def runTests():
    test1()
    # test2()


if __name__ == "__main__":
    runTests()