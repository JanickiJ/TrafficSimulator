from src.trafficSimulator.generator import Generator
from src.trafficSimulator.simulation import Simulation
from src.trafficSimulator.traffic_lights import TrafficSignal
from src.trafficSimulator.window import Window

def run_simulation(sim):
    win = Window(sim)
    win.offset = (-150, -110)
    win.run()

def intensityFunction(t):
    """Morning intensity road"""
    t = t - 400.0 * int(t / 400)
    return max(0.0, abs(200.0 - t) / 100.0)

def intensityFunction(t):
    """Afternoon intensity road"""
    t = t - 400.0 * int((t + 100) / 400)
    return max(0.0, abs(200.0 - t) / 100.0)

def set_roads_with_right_of_way(sim):
    """Cracow road map with extra roads"""
    data =[
        ((0, 300), (280, 360), 1, 25.00, False, True),
        ((280, 360), (0, 300), 2, 25.00, True, True),
        ((400, 100), (280, 360), 3, 25.00, True, True),
        ((280, 360), (400, 100), 4, 25.00, True, True),
        ((500, 300), (680, 590), 5, 25.00, False, True),
        ((680, 590), (500, 300), 6, 25.00, True, True),
        ((680, 590), (280, 360), 7, 40.00, True, True),
        ((280, 360), (680, 590), 8, 40.00, True, True),
        ((280, 360), (0, 600), 9, 40.00, True, True),
        ((0, 600), (280, 360), 10, 40.00, True, True),
        ((0, 400), (0, 600), 11, 25.00, False, True),
        ((0, 600), (0, 400), 12, 25.00, True, True),
        ((-100, 700), (0, 600), 13, 25.00, False, True),
        ((0, 600), (-100, 700), 14, 25.00, True, True),
        ((0, 600), (40, 960), 15, 40.00, True, True),
        ((40, 960), (0, 600), 16, 40.00, True, True),
        ((40, 960), (30, 1170), 17, 40.00, True, True),
        ((30, 1170), (40, 960), 18, 40.00, True, True),
        ((-100, 1150), (30, 1170), 19, 25.00, False, True),
        ((30, 1170), (-100, 1150), 20, 25.00, True, True),
        ((30, 1170), (390, 1720), 21, 40.00, True, True),
        ((390, 1720), (30, 1170), 22, 40.00, True, True),
        ((320, 1800), (390, 1720), 23, 25.00, False, True),
        ((390, 1720), (320, 1800), 24, 25.00, True, True),
        ((390, 1720), (870, 1800), 25, 40.00, True, True),
        ((870, 1800), (390, 1720), 26, 40.00, True, True),
        ((800, 2000), (870, 1800), 27, 25.00, False, True),
        ((870, 1800), (800, 2000), 28, 25.00, True, True),
        ((870, 1800), (1710, 1630), 29, 40.00, True, True),
        ((1710, 1630), (870, 1800), 30, 40.00, True, True),
        ((1900, 1800), (1710, 1630), 31, 25.00, False, True),
        ((1710, 1630), (1900, 1800), 32, 25.00, True, True),
        ((1710, 1630), (2060, 1510), 33, 40.00, True, True),
        ((2060, 1510), (1710, 1630), 34, 40.00, True, True),
        ((2060, 1510), (2080, 1200), 35, 33.33, True, True),
        ((2080, 1200), (2060, 1510), 36, 33.33, False, True),
        ((2060, 1510), (2700, 1450), 37, 40.00, True, True),
        ((2700, 1450), (2060, 1510), 38, 40.00, True, True),
        ((2080, 1200), (2160, 920), 39, 33.33, True, True),
        ((2160, 920), (2080, 1200), 40, 33.33, True, True),
        ((2160, 920), (2700, 750), 41, 25.00, True, True),
        ((2700, 750), (2160, 920), 42, 25.00, False, True),
        ((2160, 920), (1770, 690), 43, 33.33, True, True),
        ((1770, 690), (2160, 920), 44, 33.33, True, True),
        ((2200, 300), (1770, 690), 45, 25.00, True, True),
        ((1770, 690), (2200, 300), 46, 25.00, True, True),
        ((1770, 690), (1540, 610), 47, 33.33, True, True),
        ((1540, 610), (1770, 690), 48, 33.33, True, True),
        ((1180, 630), (1540, 610), 49, 33.33, True, True),
        ((1540, 610), (1180, 630), 50, 33.33, True, True),
        ((1180, 630), (1300, 200), 51, 25.00, True, True),
        ((1300, 200), (1180, 630), 52, 25.00, False, True),
        ((1180, 630), (930, 570), 53, 33.33, True, True),
        ((930, 570), (1180, 630), 54, 33.33, True, True),
        ((1000, 100), (930, 570), 55, 25.00, True, True),
        ((930, 570), (1000, 100), 56, 25.00, False, True),
        ((680, 590), (930, 570), 57, 33.33, True, True),
        ((930, 570), (680, 590), 58, 33.33, True, True),
        ((30, 1170), (790, 1090), 59, 15.00, False, True),
        ((790, 1090), (30, 1170), 60, 15.00, False, True),
        ((1110, 1270), (390, 1720), 61, 15.00, False, True),
        ((390, 1720), (1110, 1270), 62, 15.00, False, True),
        ((1060, 1230), (870, 1800), 63, 15.00, False, True),
        ((870, 1800), (1060, 1230), 64, 15.00, False, True),
        ((1060, 1230), (1110, 1270), 65, 20.00, True, True),
        ((1110, 1270), (1060, 1230), 66, 20.00, True, True),
        ((1710, 1630), (1110, 1270), 67, 20.00, True, True),
        ((1110, 1270), (1710, 1630), 68, 20.00, True, True),
        ((2080, 1200), (1320, 1130), 69, 20.00, True, True),
        ((1320, 1130), (2080, 1200), 70, 20.00, False, True),
        ((1600, 840), (1770, 690), 71, 20.00, False, True),
        ((1770, 690), (1600, 840), 72, 20.00, True, True),
        ((1600, 840), (1320, 1130), 73, 15.00, False, True),
        ((1320, 1130), (1600, 840), 74, 15.00, False, True),
        ((1600, 840), (1540, 610), 75, 15.00, False, True),
        ((1540, 610), (1600, 840), 76, 15.00, False, True),
        ((1320, 1130), (1230, 1160), 77, 15.00, True, True),
        ((1230, 1160), (1320, 1130), 78, 15.00, False, True),
        ((1230, 1160), (1110, 1270), 79, 15.00, False, True),
        ((1110, 1270), (1230, 1160), 80, 15.00, True, True),
        ((40, 960), (560, 900), 81, 15.00, True, True),
        ((560, 900), (40, 960), 82, 15.00, False, True),
        ((380, 1030), (560, 900), 83, 11.11, False, True),
        ((560, 900), (380, 1030), 84, 11.11, True, True),
        ((610, 870), (560, 900), 85, 11.11, False, True),
        ((560, 900), (610, 870), 86, 11.11, True, True),
        ((660, 780), (610, 870), 87, 11.11, True, False),
        ((660, 780), (680, 590), 88, 11.11, False, True),
        ((680, 590), (660, 780), 89, 11.11, True, True),
        ((1100, 770), (1180, 630), 90, 15.00, False, True),
        ((1180, 630), (1100, 770), 91, 15.00, False, True),
        ((1230, 960), (1600, 840), 92, 15.00, True, True),
        ((1600, 840), (1230, 960), 93, 15.00, True, True),
        ((1320, 1130), (1230, 960), 94, 15.00, False, True),
        ((1230, 960), (1320, 1130), 95, 15.00, True, True),
        ((1230, 960), (1100, 770), 96, 15.00, True, True),
        ((1100, 770), (1230, 960), 97, 15.00, True, True),
        ((1230, 960), (1090, 1020), 98, 15.00, True, True),
        ((1090, 1020), (1230, 960), 99, 15.00, True, True),
        ((1230, 1160), (1090, 1020), 100, 15.00, False, True),
        ((1090, 1020), (1230, 1160), 101, 15.00, False, True),
        ((1060, 1230), (1010, 1100), 102, 15.00, True, True),
        ((1010, 1100), (1060, 1230), 103, 15.00, True, True),
        ((1010, 1100), (1090, 1020), 104, 15.00, True, True),
        ((1090, 1020), (1010, 1100), 105, 15.00, True, True),
        ((1060, 990), (1090, 1020), 106, 11.11, True, False),
        ((790, 1090), (1010, 1100), 107, 20.00, True, True),
        ((1010, 1100), (790, 1090), 108, 20.00, True, True),
        ((980, 1010), (790, 1090), 109, 15.00, False, True),
        ((790, 1090), (980, 1010), 110, 15.00, False, True),
        ((1100, 770), (940, 860), 111, 16.66, True, True),
        ((940, 860), (1100, 770), 112, 16.66, True, False),
        ((1100, 770), (1090, 870), 113, 15.00, False, True),
        ((780, 990), (560, 900), 114, 15.00, True, True),
        ((560, 900), (780, 990), 115, 15.00, True, True),
        ((660, 780), (940, 860), 116, 15.00, True, True),
        ((940, 860), (660, 780), 117, 15.00, False, True),
        ((610, 870), (790, 920), 118, 11.11, False, False),
        ((930, 990), (790, 920), 119, 11.11, True, False),
        ((790, 920), (780, 990), 120, 11.11, False, False),
        ((930, 990), (780, 990), 121, 15.00, True, True),
        ((780, 990), (930, 990), 122, 15.00, True, True),
        ((930, 990), (960, 980), 123, 15.00, True, True),
        ((960, 980), (930, 990), 124, 15.00, True, True),
        ((940, 860), (960, 980), 125, 16.66, True, True),
        ((960, 980), (940, 860), 126, 16.66, True, True),
        ((980, 1010), (1010, 1100), 127, 16.66, False, True),
        ((1010, 1100), (980, 1010), 128, 16.66, True, True),
        ((1020, 980), (960, 980), 129, 15.00, False, False),
        ((1090, 870), (1010, 890), 130, 11.11, True, False),
        ((1060, 990), (1090, 870), 131, 11.11, True, False),
        ((1020, 980), (1060, 990), 132, 11.11, True, False),
        ((980, 1010), (960, 980), 133, 15.00, True, True),
        ((960, 980), (980, 1010), 134, 15.00, True, True),
        ((1010, 890), (1020, 980), 135, 11.11, True, False)
    ]
    def road_with_speed_limit_mapper(x): return {"start": x[0], "end": x[1], "id": x[2], "speed_limit": x[3], "right_of_way": x[4], "do_move": x[5]}
    sim.set_roads(list(map(road_with_speed_limit_mapper, data)), True)


def set_traffic_light(sim):
    return [TrafficSignal([(1, 2), (6, 14)], sim)]      


def test1():
    """Traffic light and right of way test in Crocow roadmap - one generator"""
    sim = Simulation("TEST_6_1")
    set_roads_with_right_of_way(sim)
    gen = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, (2, (930, 990), True)),
        (1, (122, (280, 360), True)),
        (1, (31, (960, 980), True)),
        (1, (59, (980, 1010), True)),
        (1, (60, (-100, 1150), True)),
        (1, (19, (320, 1800), True)),
        (1, (23, (1060, 1230), True)),
        (1, (5, (280, 360), True)),
        (1, (18, (2160, 920), True)),
        (1, (43, (960, 980), True)),
        (1, (27, (790, 1090), True)),
        (1, (62, (1090, 870), True)),
        (1, (131, (390, 1720), True)),
        (1, (31, (960, 980), True)),
        (1, (134, (1900, 1800), True)),
        (1, (31, (30, 1170), True)),
        (1, (21, (1900, 1800), True)),
        (1, (38, (1600, 840), True)),
        (1, (38, (980, 1010), True)),
        (1, (45, (960, 980), True)),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generator(gen)
    run_simulation(sim)

def test2():
    """Traffic light and right of way test in Crocow roadmap - two generator"""
    sim = Simulation("TEST_6_2")
    set_roads_with_right_of_way(sim)
    gen1 = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, (2, (930, 990), True)),
        (1, (122, (280, 360), True)),
        (1, (31, (960, 980), True)),
        (1, (59, (980, 1010), True)),
        (1, (60, (-100, 1150), True)),
        (1, (19, (320, 1800), True)),
        (1, (23, (1060, 1230), True)),
        (1, (5, (280, 360), True)),
        (1, (18, (2160, 920), True))
    ], simulation=sim, intensity_function=intensityFunction)
    gen2 = Generator(carTypes=[
        (2, {"length": 8.0, "break_reaction_time": 0.33, "maximum_speed": 25.0, "a_max": 2.5, "b_max": 5.0}),
        (1, {"length": 4.6, "break_reaction_time": 0.25, "maximum_speed": 35.0, "a_max": 4.5, "b_max": 7.2}),
        (4, {"maximum_speed": 25.0}),
        (2, {"maximum_speed": 20.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 50.0}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 12.0, "length": 1.6, "a_max": 2.0, "width": 0.8}),
        (1, {"avarage_reaction_time": 0.75, "maximum_speed": 25.0, "length": 1.75, "a_max": 2.5, "width": 1.2}),
    ], paths=[
        (1, (43, (960, 980), True)),
        (1, (27, (790, 1090), True)),
        (1, (62, (1090, 870), True)),
        (1, (131, (390, 1720), True)),
        (1, (31, (960, 980), True)),
        (1, (134, (1900, 1800), True)),
        (1, (31, (30, 1170), True)),
        (1, (21, (1900, 1800), True)),
        (1, (38, (1600, 840), True)),
        (1, (38, (980, 1010), True)),
        (1, (45, (960, 980), True)),
    ], simulation=sim, intensity_function=intensityFunction)
    sim.init_distance_vector()
    sim.set_generators([gen1, gen2])
    run_simulation(sim)

def runTests():
    # test1()
    test2()


if __name__ == "__main__":
    runTests()