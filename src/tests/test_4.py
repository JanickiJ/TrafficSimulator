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

def set_roads_with_right_of_way_1(sim):
    data =[
        ((390, 250), (0, 0), 1, 33.33, True, True),
        ((0, 0), (390, 250), 2, 33.33, True, True),
        ((430, -390), (0, 0), 3, 25.00, True, True),
        ((0, 0), (430, -390), 4, 25.00, True, True),
        ((0, 0), (-230, -8), 5, 33.33, True, True),
        ((-230, -8), (0, 0), 6, 33.33, True, True),        
        ((-170, 150), (0, 0), 7, 20.00, False, True),
        ((0, 0), (-170, 150), 8, 20.00, True, True),
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)
    # sim.set_lights(set_traffic_light(sim))

def set_roads_with_right_of_way_2(sim):
    data =[        
        ((0, 0), (-720, 450), 1, 15.00, False, True),
        ((-720, 450), (0, 0), 2, 15.00, False, True), #False
        ((-50, -40), (0, 0), 3, 20.00, True, True),
        ((0, 0), (-50, -40), 4, 20.00, True, True),
        ((600, 360), (0, 0), 5, 20.00, True, True),
        ((0, 0), (600, 360), 6, 20.00, True, True),
        ((120, -110), (0, 0), 7, 15.00, False, True), #False
        ((0, 0), (120, -110), 8, 15.00, True, True),
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)
    # sim.set_lights(set_traffic_light(sim))


def set_traffic_light(sim):
    return [TrafficSignal([(1, 2), (6, 14)], sim)]      


def test1():
    # traffic light and right of way test
    sim = Simulation("TEST_4_1")
    set_roads_with_right_of_way_1(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, [6, 2]),
        (1, [7, 2]),
        (1, [1, 8]),
        (1, [1, 8]),
        (1, [3, 8]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.set_generator(gen)
    run_simulation(sim)

def test2():
    # traffic light and right of way test
    sim = Simulation("TEST_4_2")
    set_roads_with_right_of_way_2(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, [5, 8]),
        (1, [2, 4]),
        (1, [7, 1]),
        (1, [2, 4]),
        (1, [5, 4]),
        (1, [5, 4]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.set_generator(gen)
    run_simulation(sim)

def test3():
    # traffic light and right of way test
    sim = Simulation("TEST_4_2")
    set_roads_with_right_of_way_2(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, [2, 4]),
        (1, [7, 1]),
        (1, [2, 4]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.set_generator(gen)
    run_simulation(sim)


def runTests():
    test3()


if __name__ == "__main__":
    runTests()