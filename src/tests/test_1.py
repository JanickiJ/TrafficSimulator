from src.trafficSimulator.generator import Generator
from src.trafficSimulator.simulation import Simulation
from src.trafficSimulator.traffic_lights import TrafficSignal
from src.trafficSimulator.window import Window


def run_simulation(sim):
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()


def set_simple_roads(sim):
    data = [
        ((300, 98), (0, 98), 1),
        ((0, 102), (300, 102), 2),
        ((180, 60), (0, 60), 3),
        ((220, 55), (180, 60), 4),
        ((300, 30), (220, 55), 5),
        ((180, 60), (160, 100), 6),
        ((158, 130), (300, 130), 7),
        ((0, 178), (300, 178), 8),
        ((300, 182), (0, 182), 9),
        ((160, 100), (155, 180), 10)
    ]
    def simple_road_mapper(x): return {"start": x[0], "end": x[1], "id": x[2]}
    sim.set_roads(list(map(simple_road_mapper, data)))


def set_roads_with_speed_limits(sim):
    data = [
        ((300, 98), (0, 98), 1, 40.00),
        ((0, 102), (300, 102), 2, 40.00),
        ((180, 60), (0, 60), 3, 13.83),
        ((220, 55), (180, 60), 4, 13.83),
        ((300, 30), (220, 55), 5, 13.83),
        ((180, 60), (160, 100), 6, 13.83),
        ((158, 130), (300, 130), 7, 25.00),
        ((0, 178), (300, 178), 8, 40.0),
        ((300, 182), (0, 182), 9, 40.0),
        ((160, 100), (155, 180), 10, 16.66)
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)))


def set_roads_with_traffic_light(sim):
    data = [
        ((300, 98), (160, 98), 1, 20.00),  # przeciąć 1
        ((0, 102), (160, 102), 2, 20.00),  # przeciąć 1
        ((180, 60), (0, 60), 3, 13.83),
        ((220, 55), (180, 60), 4, 13.83),
        ((300, 30), (220, 55), 5, 13.83),
        ((180, 60), (160, 100), 6, 13.83),  # 0
        ((158, 130), (300, 130), 7, 25.00),
        ((0, 178), (300, 178), 8, 40.0),
        ((300, 182), (0, 182), 9, 40.0),
        ((160, 100), (155, 180), 10, 16.66),  # 0
        ((160, 98), (0, 98), 11, 20.00),  # 1
        ((160, 102), (300, 102), 12, 20.00),  # 1
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)))
    sim.set_lights(set_traffic_light(sim))


def set_roads_with_right_of_way(sim):
    data =[
        ((300, 98), (160, 98), 1, 20.00, True),  # przeciąć 1
        ((0, 102), (160, 102), 2, 20.00, True),  # przeciąć 1
        ((180, 60), (0, 60), 3, 13.83, True),
        ((220, 55), (180, 60), 4, 13.83, True),
        ((300, 30), (220, 55), 5, 13.83, True),
        ((180, 60), (160, 100), 6, 13.83, True),  # 0
        ((158, 130), (300, 130), 7, 25.00, True),
        ((0, 178), (300, 178), 8, 40.0, True),
        ((300, 182), (0, 182), 9, 40.0, True),
        ((160, 100), (158, 140), 10, 16.66, True),
        ((160, 98), (0, 98), 11, 20.00, True),  # 1
        ((160, 102), (300, 102), 12, 20.00, True),  # 1
        ((0, 140), (156, 140), 13, 13.83, False),
        ((158, 140), (155, 180), 14, 13.83, True)  # 0
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)))
    sim.set_lights(set_traffic_light(sim))

def set_roads_with_right_of_way_modified(sim):
    data =[
        ((300, 100), (160, 100), 1, 20.00, True),  # przeciąć 1
        ((0, 100), (160, 100), 2, 20.00, True),  # przeciąć 1
        ((180, 60), (0, 60), 3, 13.83, True),
        ((220, 55), (180, 60), 4, 13.83, True),
        ((300, 30), (220, 55), 5, 13.83, True),
        ((180, 60), (160, 100), 6, 13.83, True),  # 0
        ((160, 130), (300, 130), 7, 25.00, True),
        ((0, 180), (300, 180), 8, 40.0, True),
        ((300, 190), (0, 190), 9, 40.0, True),
        ((160, 100), (160, 140), 10, 16.66, True),
        ((160, 100), (0, 100), 11, 20.00, True),  # 1
        ((160, 100), (300, 100), 12, 20.00, True),  # 1
        ((0, 140), (160, 140), 13, 13.83, False),
        ((160, 140), (160, 180), 14, 13.83, True)  # 0
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), do_set_coincident = True)
    sim.set_lights(set_traffic_light(sim))

def set_simple_crossroad(sim):
    data =[
        ((0, 200), (200, 200), 1, 15.00, False, True),
        ((150, 0), (200, 200), 2, 15.00, True, True),
        ((400, 200), (200, 200), 3, 15.00, False, True),
        ((200, 400), (200, 200), 4, 15.00, True, True),
        ((200, 200), (0, 200), 5, 15.00, True, True),
        ((200, 200), (150, 0), 6, 15.00, True, True),
        ((200, 200), (400, 200), 7, 15.00, True, True),
        ((200, 200), (200, 400), 8, 15.00, True, True),
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), do_set_coincident = True)


def set_traffic_light(sim):
    return [TrafficSignal([(1, 2), (6, 12)], sim)]


def test1():
    sim = Simulation("TEST_1_1")
    set_simple_roads(sim)
    sim.set_vehicles([
        ({}, {"id": 1, "maximum_speed": 10.0, "path": [5, 4, 3], "position": 60}),
        ({}, {"id": 2, "maximum_speed": 20.0, "path": [5, 4, 3], "position": 40}),
        ({}, {"id": 3, "maximum_speed": 16.6, "path": [5, 4, 3], "position": 15}),
        ({}, {"id": 4, "maximum_speed": 18.6, "path": [5, 4, 3], "position": 0}),
        ({}, {"id": 5, "maximum_speed": 15.0, "path": [8, 7]}),
        ({}, {"id": 6, "maximum_speed": 17.6, "path": [1, 2]}),
        ({}, {"id": 7, "maximum_speed": 16.0, "path": [4, 6, 10]}),
    ])
    run_simulation(sim)


def test2():
    # all cars created in one moment (befor starting simulation)
    sim = Simulation("TEST_1_2")
    set_simple_roads(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 15.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 30.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {}),
        (2, {}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 35.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 2]),
        (1, [4, 3]),
        (1, [6, 10]),
        (1, [3]),
        (1, [7]),
        (1, [2]),
        (1, [10]),
    ], simulation=sim)
    gen.generateCars(5)
    run_simulation(sim)


def intensityFunction(t):
    return max(0.0, (20.0 - t) / 20.0)


def test3():
    # car are being created during simulation
    sim = Simulation("TEST_1_3")
    set_simple_roads(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 15.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 30.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {}),
        (2, {}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 35.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 2]),
        (1, [4, 3]),
        (1, [6, 10]),
        (1, [3]),
        (1, [7]),
        (1, [2]),
        (1, [10]),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.set_generator(gen)
    run_simulation(sim)


def intensityFunction2(t):
    return 2.0 * max(0.0, (100.0 - t) / 100.0)


def test4():
    # more cars are being created during simulation 
    sim = Simulation("TEST_1_4")
    set_simple_roads(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 15.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 30.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {}),
        (2, {}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 35.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 2]),
        (1, [4, 3]),
        (1, [6, 10]),
        (1, [3]),
        (1, [7]),
        (1, [2]),
        (1, [10]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    run_simulation(sim)


def test5():
    # speed limit test 
    sim = Simulation("TEST_1_5")
    set_roads_with_speed_limits(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 2]),
        (1, [4, 3]),
        (1, [6, 10]),
        (1, [3]),
        (1, [7]),
        (1, [2]),
        (1, [10]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    run_simulation(sim)


def test6():
    # traffic light test
    sim = Simulation("TEST_1_6")
    set_roads_with_traffic_light(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 11, 2, 12]),
        (1, [4, 3]),
        (1, [6, 10]),
        (1, [3]),
        (1, [7]),
        (1, [2, 12]),
        (1, [10]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    run_simulation(sim)


def test7():
    # traffic light and right of way test
    sim = Simulation("TEST_1_7")
    set_roads_with_right_of_way(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 11, 2, 12]),
        (1, [4, 3]),
        (1, [6, 10, 14]),
        (1, [3]),
        (1, [7]),
        (1, [13, 14]),
        (1, [2, 12]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    run_simulation(sim)


def test8():
    # traffic light and right of way test
    sim = Simulation("TEST_1_8")
    set_roads_with_right_of_way(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 11, 2, 12]),
        (1, [4, 3]),
        (1, [6, 10, 14]),
        (1, [3]),
        (1, [7]),
        (1, [13, 14]),
        (1, [2, 12]),
        (1, [2, 10, 14]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    run_simulation(sim)


def test9():
    # traffic light and right of way test
    sim = Simulation("TEST_1_9")
    set_roads_with_right_of_way_modified(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 45.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 45.0}),
        (2, {"maximum_speed": 40.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "a_max": 2.5, "width": 1.2})
    ], paths=[
        (1, [5, 4, 3]),
        (1, [8, 7]),
        (1, [1, 11, 2, 12]),
        (1, [4, 3]),
        (1, [6, 10, 14]),
        (1, [3]),
        (1, [7]),
        (1, [13, 14]),
        (1, [2, 12]),
        (1, [2, 10, 14]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    run_simulation(sim)

def test10() :
    # Crossroad deadlock avoidance test
    sim = Simulation("TEST_1_10")
    set_simple_crossroad(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 45.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 45.0}),
        (2, {"maximum_speed": 40.0}),
    ], paths=[
        (1, [1, 8]),
        (1, [1, 7]),
        (1, [1, 8]),
        (1, [2, 5]),
        (1, [2, 7]),
        (1, [2, 8]),
        (1, [3, 5]),
        (1, [3, 6]),
        (1, [3, 8]),
        (1, [4, 5]),
        (1, [4, 6]),
        (1, [4, 7]),
    ], simulation=sim, intensity_function=intensityFunction2)
    sim.set_generator(gen)
    # gen.generateCars(10)
    run_simulation(sim)


     


def runTests():
    # test1()
    # test2()
    # test3()
    # test4()
    # test5()
    # test6()
    test7()
    # test8()
    # test9()
    # test10()


if __name__ == "__main__":
    runTests()