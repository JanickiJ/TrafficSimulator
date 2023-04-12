from src.trafficSimulator.generator import Generator
from src.trafficSimulator.simulation import Simulation
from src.trafficSimulator.traffic_lights import TrafficSignal
from src.trafficSimulator.window import Window


def run_simulation(sim):
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()


def intensityFunction(t):
    return max(0.0, (100.0 - t) / 5.0)


def set_roads(sim):
    data = [
        ((800, 100), (160, 100), 1, 20.00, True, True),
        ((-500, 100), (160, 100), 2, 20.00, True, True),
        ((160, 100), (-500, 100), 3, 20.00, True, True),
        ((160, 100), (800, 100), 4, 20.00, True, True),

        ((160, 100), (160, 700), 5, 20.00, True, True),
        ((160, 700), (160, 100), 6, 20.00, True, True),
        ((160, 100), (160, -500), 7, 20.00, True, True),
        ((160, -500), (160, 100), 8, 20.00, True, True),
    ]

    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3],
                                                 "right_of_way": x[4], "do_move": x[5]}

    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)
    sim.set_lights(set_traffic_light(sim))

def set_roads_2(sim):
    data = [
        ((1440, 100), (160, 100), 1, 20.00, True, True),
        ((-1160, 100), (160, 100), 2, 20.00, True, True),
        ((160, 100), (-500, 100), 3, 20.00, True, True),
        ((160, 100), (800, 100), 4, 20.00, True, True),

        ((160, 100), (160, 700), 5, 20.00, True, True),
        ((160, 700), (160, 100), 6, 20.00, True, True),
        ((160, 100), (160, -500), 7, 20.00, True, True),
        ((160, -500), (160, 100), 8, 20.00, True, True),
    ]

    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3],
                                                 "right_of_way": x[4], "do_move": x[5]}

    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)
    sim.set_lights(set_traffic_light(sim))


def set_traffic_light(sim):
    return [TrafficSignal([(1, 2), (6, 8)], sim)]


def test1():
    sim = Simulation("CROSSING_LIGHTS_SIM", speed=2)
    set_roads(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.25, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.25, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.25, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, [2, 4]),
        (1, [2, 7]),
        (1, [2, 5]),
        (1, [8, 3]),
        (1, [8, 4]),
        (1, [8, 5]),
        (1, [1, 7]),
        (1, [1, 5]),
        (1, [1, 3]),
        (1, [6, 3]),
        (1, [6, 7]),
        (1, [6, 4]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)

def test2():
    sim = Simulation("CROSSING_LIGHTS_SIM", speed=2)
    set_roads_2(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.25, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.25, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.25, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (2, [2, 4]),
        (2, [2, 7]),
        (2, [2, 5]),
        (1, [8, 3]),
        (1, [8, 4]),
        (1, [8, 5]),
        (2, [1, 7]),
        (2, [1, 5]),
        (2, [1, 3]),
        (1, [6, 3]),
        (1, [6, 7]),
        (1, [6, 4]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)


def runTests():
    # test1()
    test2()


if __name__ == "__main__":
    runTests()

