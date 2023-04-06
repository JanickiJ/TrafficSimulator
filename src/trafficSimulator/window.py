import numpy as np
import pygame
from pygame import gfxdraw

from src.trafficSimulator.parameters import road_width
from src.trafficSimulator.parameters import bg_color, fps, height, width, zoom
from src.trafficSimulator.parameters import rect_color, arrow_color, axes_color, grid_color, stop_line_color, major_grid_color, minor_grid_color
from src.trafficSimulator.parameters import grid_unit, major_grid_unit, minor_grid_unit
from src.trafficSimulator.parameters import traffic_color_coefficient, traffic_color_coefficient_2, red_basic, green_basic
from src.trafficSimulator.parameters import stop_line_size
from src.trafficSimulator.parameters import change_lane_time
from src.trafficSimulator.car import Car
from src.trafficSimulator.curve import Curve
from src.trafficSimulator.road import Road

# from parameters import road_width
# from parameters import bg_color, fps, height, width, zoom
# from parameters import rect_color, arrow_color, axes_color, grid_color, stop_line_color, major_grid_color, minor_grid_color, car_color
# from parameters import grid_unit, major_grid_unit, minor_grid_unit
# from parameters import traffic_color_coefficient, traffic_color_coefficient_2, red_basic, green_basic
# from parameters import stop_line_size
# from parameters import change_lane_time
# from car import Car
# from curve import Curve
# from road import Road

class Window:
    def __init__(self, sim, config={}):
        self.sim = sim
        self.set_default_config()
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        """Set default configuration"""
        self.width = width
        self.height = height
        self.bg_color = bg_color

        self.fps = fps
        self.zoom = zoom
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

    def loop(self, loop=None):
        """Shows a window visualizing the simulation and runs the loop function."""

        # Create a pygame window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()

        # Fixed fps
        clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()
        self.text_font = pygame.font.SysFont('Lucida Console', 16)

        # Draw loop
        running = True
        while running:
            # Update simulation
            if loop: loop(self.sim)

            # Draw simulation
            self.draw()

            # Update window
            pygame.display.update()
            clock.tick(self.fps)

            # Handle all events
            for event in pygame.event.get():
                # print(event)
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False
                # Handle mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse button down
                    if event.button == 1:
                        # Left click
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_last = (x - x0 * self.zoom, y - y0 * self.zoom)
                        self.mouse_down = True
                    if event.button == 4:
                        # Mouse wheel up
                        self.zoom *= (self.zoom ** 2 + self.zoom / 4 + 1) / (self.zoom ** 2 + 1)
                    if event.button == 5:
                        # Mouse wheel down 
                        self.zoom *= (self.zoom ** 2 + 1) / (self.zoom ** 2 + self.zoom / 4 + 1)
                elif event.type == pygame.MOUSEMOTION:
                    # Drag content
                    if self.mouse_down:
                        x1, y1 = self.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2 - x1) / self.zoom, (y2 - y1) / self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False

    def run(self, steps_per_update=1):
        """Runs the simulation by updating in every loop."""

        def loop(sim):
            sim.run(steps_per_update)

        self.loop(loop)

    def convert(self, x, y=None):
        """Converts simulation coordinates to screen coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(self.width / 2 + (x + self.offset[0]) * self.zoom),
            int(self.height / 2 + (y + self.offset[1]) * self.zoom)
        )

    def inverse_convert(self, x, y=None):
        """Converts screen coordinates to simulation coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.width / 2) / self.zoom),
            int(-self.offset[1] + (y - self.height / 2) / self.zoom)
        )

    def background(self, r, g, b):
        """Fills screen with one color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Draws a line."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)

        vertex = lambda e1, e2: (
            x + (e1 * l * cos + e2 * h * sin) / 2,
            y + (e1 * l * sin - e2 * h * cos) / 2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1, -1), (-1, 1), (1, 1), (1, -1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0, -1), (0, 1), (2, 1), (2, -1)]]
            )

        self.polygon(vertices, color, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=rect_color):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=arrow_color):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)

        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )

    def draw_axes(self, color=axes_color):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=grid_unit, color=grid_color):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.width, self.height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit) + 1
        m_y = int(y_end / unit) + 1

        for i in range(n_x, m_x):
            self.line(
                self.convert((unit * i, y_start)),
                self.convert((unit * i, y_end)),
                color
            )
        for i in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit * i)),
                self.convert((x_end, unit * i)),
                color
            )

    def draw_roads(self):
        for road in self.sim.roads.values():
            if isinstance(road, Curve):
                self.draw_curve(road)
            else:
                self.draw_road(road)
        self.draw_stop_lines()

    def draw_curve(self, curve: Curve):
        roads = curve.as_roads(resolution=10)
        for road in roads:
            self.draw_road(road)

    def draw_road(self, road: Road):
        """Drawing one road with all its lines"""
        for i in range(road.lines):
            dx, dy = road_width * road.angle_sin, -road_width * road.angle_cos
            start = (road.start[0] - i * dx, road.start[1] - i * dy)
            self.draw_lane(road.length, road.max_speed, road.expected_time, start, road.angle_cos, road.angle_sin)

    def draw_lane(self, length, max_speed, expected_time, start, angle_cos, angle_sin):
        """Drawing one road lane"""
        def_time = length  / max_speed
        traffic = traffic_color_coefficient * (expected_time - def_time) / def_time
        r, g = min(255, red_basic + traffic_color_coefficient_2 * traffic), max(0, green_basic - traffic_color_coefficient_2 * np.abs(traffic - 1.0))
        b = g
        self.rotated_box(
            start,
            (length, road_width),
            cos=angle_cos,
            sin=angle_sin,
            color=(r, g, b),
            centered=False
        )
        # Draw road lines
        # self.rotated_box(
        #     road.start,
        #     (road.length, 0.25),
        #     cos=road.angle_cos,
        #     sin=road.angle_sin,
        #     color=(0, 0, 0),
        #     centered=False
        # )
        if length > 5:
            for i in np.arange(-0.5 * length, 0.5 * length, 10):
                pos = (
                    start[0] + (length / 2 + i + 3) * angle_cos,
                    start[1] + (length / 2 + i + 3) * angle_sin
                )

                self.arrow(
                    pos,
                    (-1.25, 0.2),
                    cos=angle_cos,
                    sin=angle_sin
                )
    
    def draw_stop_lines(self) :
        for road in self.sim.roads.values():
            if not road.has_right_of_way:
                for j in range(road.lines):                        
                    a = (2 * road_width + 1.0) / road.length
                    dx, dy = road_width * road.angle_sin, -road_width * road.angle_cos
                    start = (road.start[0] - j * dx, road.start[1] - j * dy)
                    end = (road.end[0] - j * dx, road.end[1] - j * dy)
                    position = (
                        (1.0 - a) * end[0] + a * start[0],
                        (1.0 - a) * end[1] + a * start[1]
                    )
                    self.rotated_box(
                        position,
                        stop_line_size,
                        cos=road.angle_cos,
                        sin=road.angle_sin,
                        color=stop_line_color,
                        centered=True
                    )

    def draw_vehicle(self, vehicle: Car, road: Road):
        l, h = vehicle.length, vehicle.width
        vehicle_x = vehicle.x
        road_substitute = road
        dt = vehicle.t - vehicle.last_lane_change_t
        if isinstance(road, Curve):
            road_substitute = road.get_vehicle_current_road_substitute(vehicle.x)
            vehicle_x -= road.get_road_substitute_start_length(road_substitute)
            dx, dy = 0, 0 #TODO
        else:
            dx, dy = (vehicle.line - vehicle.angle * max(0, change_lane_time - dt) / change_lane_time) * road_width * road.angle_sin, -(vehicle.line - vehicle.angle * max(0, change_lane_time - dt) / change_lane_time) * road_width * road.angle_cos

        t = max(0, change_lane_time / 2 - abs(change_lane_time / 2 - min(change_lane_time, dt))) / change_lane_time
        turn_angle = vehicle.angle * t * 0.2
        sin, cos = road_substitute.angle_sin, road_substitute.angle_cos

        x = road_substitute.start[0] + cos * (vehicle_x - 1.0) - dx
        y = road_substitute.start[1] + sin * (vehicle_x - 1.0) - dy

        color = car_color

        self.rotated_box((x, y), (l, h), cos=cos - np.sign(sin) * turn_angle, sin=sin + np.sign(cos) * turn_angle, color=color, centered=True)

    def draw_vehicles(self):
        for road in self.sim.roads.values():
            for vehicle in road.vehicles:
                self.draw_vehicle(vehicle, road)

    def draw_signals(self):
        for signal in self.sim.traffic_lights:
            for i in range(len(signal.roads)):
                for r in signal.roads[i]:
                    road = self.sim.roads[r]
                    for j in range(road.lines):                        
                        a = (2 * road_width + 1.0) / road.length
                        dx, dy = road_width * road.angle_sin, -road_width * road.angle_cos
                        start = (road.start[0] - j * dx, road.start[1] - j * dy)
                        end = (road.end[0] - j * dx, road.end[1] - j * dy)
                        position = (
                            (1.0 - a) * end[0] + a * start[0],
                            (1.0 - a) * end[1] + a * start[1]
                        )
                        if signal.get_current_state_yellow(i):
                            color = (0, 255, 0)
                            self.rotated_box(position, (1, 3), cos=road.angle_cos, sin=road.angle_sin, color=color)
                        elif signal.get_current_state_yellow(i)==None:
                            color = (255, 255, 0)
                            self.rotated_box(position, (1, 3), cos=road.angle_cos, sin=road.angle_sin, color=color)
                        else:
                            color = (255, 0, 0)
                            self.rotated_box(position, (1, 3), cos=road.angle_cos, sin=road.angle_sin, color=color)

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.sim.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.sim.frame_count}', False, (0, 0, 0))

        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))

    def draw(self):
        # Fill background
        self.background(*self.bg_color)

        # Major and minor grid and axes
        self.draw_grid(major_grid_unit, major_grid_color)
        self.draw_grid(minor_grid_unit, minor_grid_color)
        self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()  # TODO
        self.draw_signals()  # TODO

        # Draw status info
        # self.draw_status() #TODO
