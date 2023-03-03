from src.trafficSimulator import *

sim = Simulation()

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

sim.set_vehicles([
                (sim, {}, {"id" : 1, "maximum_speed" : 10.0, "path" : [5, 4, 3], "position" : 60}),
                (sim, {}, {"id" : 2, "maximum_speed" : 20.0, "path" : [5, 4, 3], "position" : 40}),
                (sim, {}, {"id" : 3, "maximum_speed" : 16.6, "path" : [5, 4, 3], "position" : 15}),
                (sim, {}, {"id" : 4, "maximum_speed" : 18.6, "path" : [5, 4, 3], "position" : 0}),
                (sim, {}, {"id" : 5, "maximum_speed" : 15.0, "path" : [8, 7]}),
                (sim, {}, {"id" : 6, "maximum_speed" : 17.6, "path" : [1, 2]}),
                (sim, {}, {"id" : 7, "maximum_speed" : 16.0, "path" : [4, 6, 10]}),
              ])


win = Window(sim)
win.offset = (-150, -110)
win.run()
