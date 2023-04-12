from src.trafficSimulator.generator import Generator
from src.trafficSimulator.simulation import Simulation
from src.trafficSimulator.window import Window


def set_roads(sim):
    roads = [
        ((800, 100), (200, 100), 1, 20.00, True, True),
        ((-500, 100), (120, 100), 2, 20.00, True, True),
        ((120, 100), (-500, 100), 3, 20.00, True, True),
        ((200, 100), (800, 100), 4, 20.00, True, True),

        ((160, 140), (160, 700), 5, 20.00, True, True),
        ((160, 700), (160, 140), 6, 20.00, True, True),
        ((160, 60), (160, -500), 7, 20.00, True, True),
        ((160, -500), (160, 60), 8, 20.00, True, True),
    ]

    curves = [
        ((120, 100), (160, 60), (120, 60), 9, 20.0, True, True),
        ((160, 60), (200, 100), (200, 60), 10, 20.0, True, True),
        ((200, 100), (160, 140), (200, 140), 11, 20.0, True, True),
        ((160, 140), (120, 100), (120, 140), 12, 20.0, True, True),
    ]

    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3],
                                                 "right_of_way": x[4], "do_move": x[5]}

    def curve_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[3], "control_point": x[2],
                                                  "speed_limit": x[4],
                                                  "right_of_way": x[5], "do_move": x[6]}

    sim.set_roads(list(map(road_with_speed_limit_mapper, roads))
                  + list(map(curve_with_speed_limit_mapper, curves)),
                  True)
<<<<<<< Updated upstream


def test():
=======
    
def set_roads_2(sim):
    data = [
        ((1440, 100), (200, 100), 1, 20.00, True, True),
        ((-1160, 100), (120, 100), 2, 20.00, True, True),
        ((120, 100), (-500, 100), 3, 20.00, True, True),
        ((200, 100), (800, 100), 4, 20.00, True, True),

        ((160, 140), (160, 700), 5, 20.00, True, True),
        ((160, 700), (160, 140), 6, 20.00, True, True),
        ((160, 60), (160, -500), 7, 20.00, True, True),
        ((160, -500), (160, 60), 8, 20.00, True, True),
    ]

    curves = [
        ((120, 100), (160, 60), (120, 60), 9, 20.0, True, True),
        ((160, 60), (200, 100), (200, 60), 10, 20.0, True, True),
        ((200, 100), (160, 140), (200, 140), 11, 20.0, True, True),
        ((160, 140), (120, 100), (120, 140), 12, 20.0, True, True),
    ]

    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3],
                                                 "right_of_way": x[4], "do_move": x[5]}

    def curve_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[3], "control_point": x[2],
                                                  "speed_limit": x[4],
                                                  "right_of_way": x[5], "do_move": x[6]}

    sim.set_roads(list(map(road_with_speed_limit_mapper, data))
                  + list(map(curve_with_speed_limit_mapper, curves)),
                  True)


def test1():
>>>>>>> Stashed changes
    sim = Simulation("TRAFFIC_CIRCLE_SIM", speed=2)
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
        # (1, [1, 11, 12, 9,10, 4]),
        (1, [1, 11, 12, 9, 7]),
        (1, [1, 11, 12, 3]),
        (1, [1, 11, 5]),

        # (1, [2, 9, 10, 11, 12, 3]),
        (1, [2, 9, 10, 11, 5]),
        (1, [2, 9, 10, 4]),
        (1, [2, 9, 7]),

        # (1, [8, 10, 11, 12, 9, 7]),
        (1, [8, 10, 11, 12, 3]),
        (1, [8, 10, 11, 5]),
        (1, [8, 10, 4]),

        # (1, [6, 12, 9, 10, 11, 5]),
        (1, [6, 12, 9, 10, 4]),
        (1, [6, 12, 9, 7]),
        (1, [6, 12, 3]),

    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)


<<<<<<< Updated upstream
=======
def test2():
    sim = Simulation("TRAFFIC_CIRCLE_SIM", speed=2)
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
        # (1, [1, 11, 12, 9,10, 4]),
        (2, [1, 11, 12, 9, 7]),
        (2, [1, 11, 12, 3]),
        (2, [1, 11, 5]),

        # (1, [2, 9, 10, 11, 12, 3]),
        (2, [2, 9, 10, 11, 5]),
        (2, [2, 9, 10, 4]),
        (2, [2, 9, 7]),

        # (1, [8, 10, 11, 12, 9, 7]),
        (1, [8, 10, 11, 12, 3]),
        (1, [8, 10, 11, 5]),
        (1, [8, 10, 4]),

        # (1, [6, 12, 9, 10, 11, 5]),
        (1, [6, 12, 9, 10, 4]),
        (1, [6, 12, 9, 7]),
        (1, [6, 12, 3]),

    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)


>>>>>>> Stashed changes
def intensityFunction(t):
    return max(0.0, (100.0 - t) / 5.0)


def run_simulation(sim):
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()


def runTests():
<<<<<<< Updated upstream
    test()


if __name__ == "__main__":
    runTests()
=======
    # test1()
    test2()


if __name__ == "__main__":
    runTests()
>>>>>>> Stashed changes
