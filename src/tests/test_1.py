from src.trafficSimulator import *

def run_simulation(sim) :
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()

def set_simple_roads(sim) :
    sim.set_roads([
        ((300, 98), (0, 98), 1),
        ((0, 102), (300, 102), 2),
        ((180, 60), (0, 60), 3),
        ((220, 55), (180, 60), 4),
        ((300, 30), (220, 55), 5),
        ((180, 60), (160, 98), 6),
        ((158, 130), (300, 130), 7),
        ((0, 178), (300, 178), 8),
        ((300, 182), (0, 182), 9),
        ((160, 102), (155, 180), 10)
    ])

def set_roads_with_speed_limits(sim) :
    sim.set_roads([
        ((300, 98), (0, 98), 1, 40.00),
        ((0, 102), (300, 102), 2, 40.00),
        ((180, 60), (0, 60), 3, 13.83),
        ((220, 55), (180, 60), 4, 13.83),
        ((300, 30), (220, 55), 5, 13.83),
        ((180, 60), (160, 98), 6, 13.83),
        ((158, 130), (300, 130), 7, 25.00),
        ((0, 178), (300, 178), 8, 40.0),
        ((300, 182), (0, 182), 9, 40.0),
        ((160, 102), (155, 180), 10, 16.66)
    ])

def test1() :
    sim = Simulation()
    set_simple_roads(sim)
    sim.set_vehicles([
                    ({}, {"id" : 1, "maximum_speed" : 10.0, "path" : [5, 4, 3], "position" : 60}),
                    ({}, {"id" : 2, "maximum_speed" : 20.0, "path" : [5, 4, 3], "position" : 40}),
                    ({}, {"id" : 3, "maximum_speed" : 16.6, "path" : [5, 4, 3], "position" : 15}),
                    ({}, {"id" : 4, "maximum_speed" : 18.6, "path" : [5, 4, 3], "position" : 0}),
                    ({}, {"id" : 5, "maximum_speed" : 15.0, "path" : [8, 7]}),
                    ({}, {"id" : 6, "maximum_speed" : 17.6, "path" : [1, 2]}),
                    ({}, {"id" : 7, "maximum_speed" : 16.0, "path" : [4, 6, 10]}),
                ])
    run_simulation(sim)
    
def test2() :
    # all cars created in one moment (befor starting simulation)
    sim = Simulation()
    set_simple_roads(sim)
    gen = Generator(carTypes=[
                                (2, {"length" : 8.0, "break_reaction_time" : 0.33, "maximum_speed" : 15.0, "a_max" : 2.5, "b_max" : 5.0}), 
                                (1, {"length" : 4.6, "break_reaction_time" : 0.25, "maximum_speed" : 30.0, "a_max" : 4.5, "b_max" : 7.2}), 
                                (4, {}),
                                (2, {}),
                                (1, {"avarage_reaction_time" : 0.75, "maximum_speed" : 35.0})
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

def intensityFunction(t) :
    return max(0.0, (20.0 - t) / 20.0)

def test3() :
    # car are being created during simulation
    sim = Simulation()
    set_simple_roads(sim)
    gen = Generator(carTypes=[
                                (2, {"length" : 8.0, "break_reaction_time" : 0.33, "maximum_speed" : 15.0, "a_max" : 2.5, "b_max" : 5.0}), 
                                (1, {"length" : 4.6, "break_reaction_time" : 0.25, "maximum_speed" : 30.0, "a_max" : 4.5, "b_max" : 7.2}), 
                                (4, {}),
                                (2, {}),
                                (1, {"avarage_reaction_time" : 0.75, "maximum_speed" : 35.0})
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

def intensityFunction2(t) :
    return 2.0 * max(0.0, (100.0 - t) / 100.0)

def test4() :
    # more cars are being created during simulation 
    sim = Simulation()
    set_simple_roads(sim)
    gen = Generator(carTypes=[
                                (2, {"length" : 8.0, "break_reaction_time" : 0.33, "maximum_speed" : 15.0, "a_max" : 2.5, "b_max" : 5.0}), 
                                (1, {"length" : 4.6, "break_reaction_time" : 0.25, "maximum_speed" : 30.0, "a_max" : 4.5, "b_max" : 7.2}), 
                                (4, {}),
                                (2, {}),
                                (1, {"avarage_reaction_time" : 0.75, "maximum_speed" : 35.0})
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

def test5() :
    # speed limit test 
    sim = Simulation()
    set_roads_with_speed_limits(sim)
    gen = Generator(carTypes=[
                                (2, {"length" : 8.0, "break_reaction_time" : 0.33, "maximum_speed" : 25.0, "a_max" : 2.5, "b_max" : 5.0}), 
                                (1, {"length" : 4.6, "break_reaction_time" : 0.25, "maximum_speed" : 35.0, "a_max" : 4.5, "b_max" : 7.2}), 
                                (4, {"maximum_speed" : 25.0}),
                                (2, {"maximum_speed" : 20.0}),
                                (1, {"avarage_reaction_time" : 0.75, "maximum_speed" : 50.0})
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

def runTests() :
    # test1()
    # test2()
    # test3()
    # test4()
    test5()

if __name__ == "__main__" :
    runTests()