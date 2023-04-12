# car size parameters
max_car_length = 12.5
max_vehicle_width = 3.0
default_car_parameters = {
                            "id": 0,
                            "length": 4.6,
                            "width": 2.0,
                            "delta_s0": 1.0,
                            "break_reaction_time": 0.3,
                            "avarage_reaction_time": 0.85,
                            "stand_dev_reaction_time": 0.15,
                            "maximum_speed": 16.6,
                            "a_max": 3.3,
                            "b_max": 6.25,
                            "road_index": 0,
                            "path": [],
                            "position": 0
                        }

# road safety parameters
break_distance = 25.0
save_distance = 10.0
stop_distance = 15.0
default_speed_limit = 13.83

# program parameters
inf = 1000000000
queue_size = 5

# traffic light parameters
default_traffic_light_T = 72.0
default_traffic_state = [(False, True), (True, False)]
default_traffic_state_yellow = [(True, None, False, False, False, None), (False, False, None, True, None, False)]
# default_traffic_time_steps = [32.0, 36.0, 40.0, 72.0, 76.0, 80.0]
default_traffic_time_steps = [32.0, 34.0, 36.0, 68.0, 70.0, 72.0]

# road parameters
road_width = 4.0
curve_number = 10

# visualisation parameters
bg_color = (229, 255, 204)
fps = 60
height = 900
width = 1400
zoom = 5

#color parameters
rect_color = (0, 0, 255)
arrow_color = (150, 150, 190)
axes_color = (100, 100, 100)
grid_color = (150, 150, 150)
stop_line_color = (224, 224, 224)
major_grid_color = (220, 220, 220)
minor_grid_color = (200, 200, 200)

# unit parameters
grid_unit = 50
major_grid_unit = 10
minor_grid_unit = 100

# traffic visualization coefficients
traffic_color_coefficient = 3.0
traffic_color_coefficient_2 = 64
red_basic = 128
green_basic = 192

# stop line parameters
stop_line_size = (1, 3.7)
stop_line_distance = 4.0

# measurements parameters
SAVE_RESULTS_IN_DB = False

# debug parameters
debug = False
debug_graph = False
simulation_debug = False
debug_car = False
