from src.trafficSimulator.simulation import Simulation
from src.trafficSimulator.window import Window

sim = Simulation()

# Add multiple roads
sim.set_roads([
    {"start": (90, 100), "end": (140, 100), "id": 1},
    {"start": (140, 100), "end": (200, 100), "id": 6},
    {"start": (140, 100), "end": (150, 110), "control_point": (150, 100), "id": 2},
    {"start": (150, 110), "end": (140, 120), "control_point": (150, 120), "id": 3},
    {"start": (140, 120), "end": (130, 110), "control_point": (130, 120), "id": 4},
    {"start": (130, 110), "end": (140, 100), "control_point": (130, 100), "id": 5},
])


sim.set_vehicles([
    ({}, {"id": 1, "maximum_speed": 1.0,
          "path": [1] + list(range(2, 6)) + list(range(2, 6)) + list(range(2, 6)) + list(range(2, 6)) + [6],
          "position": 10}),
    ({}, {"id": 2, "maximum_speed": 2.0,
          "path": [1] + list(range(2, 6)) + list(range(2, 6)) + list(range(2, 6)) + list(range(2, 6)) + [6],
          "position": 40}),
])

# Start simulation
win = Window(sim)
win.offset = (-150, -110)
win.run(steps_per_update=5)
