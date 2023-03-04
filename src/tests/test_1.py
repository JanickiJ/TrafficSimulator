from src.trafficSimulator import *

def runSimulation(sim) :
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()

def setSimpleRoads(sim) :
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

def test1() :
    sim = Simulation()
    setSimpleRoads(sim)
    sim.set_vehicles([
                    ({}, {"id" : 1, "maximum_speed" : 10.0, "path" : [5, 4, 3], "position" : 60}),
                    ({}, {"id" : 2, "maximum_speed" : 20.0, "path" : [5, 4, 3], "position" : 40}),
                    ({}, {"id" : 3, "maximum_speed" : 16.6, "path" : [5, 4, 3], "position" : 15}),
                    ({}, {"id" : 4, "maximum_speed" : 18.6, "path" : [5, 4, 3], "position" : 0}),
                    ({}, {"id" : 5, "maximum_speed" : 15.0, "path" : [8, 7]}),
                    ({}, {"id" : 6, "maximum_speed" : 17.6, "path" : [1, 2]}),
                    ({}, {"id" : 7, "maximum_speed" : 16.0, "path" : [4, 6, 10]}),
                ])
    runSimulation(sim)
    
def test2() :

    # all cars created in one moment
    
    sim = Simulation()
    setSimpleRoads(sim)
    gen = Generator([
        (2, {"length" : 8.0, "break_reaction_time" : 0.33, "maximum_speed" : 15.0, "a_max" : 2.5, "b_max" : 5.0, "path" : [5, 4, 3]}), 
        (1, {"length" : 4.6, "break_reaction_time" : 0.25, "maximum_speed" : 30.0, "a_max" : 4.5, "b_max" : 7.2, "path" : [4, 3]}), 
        (4, {"path" : [8, 7]}),
        (2, {"path" : [5, 4, 6, 10]}),
        (1, {"avarage_reaction_time" : 0.75, "maximum_speed" : 35.0, "path" : [4, 6, 10]})], sim)
    gen.generateCars(10)
    runSimulation(sim)

def runTests() :
    # test1()
    test2()

if __name__ == "__main__" :
    runTests()