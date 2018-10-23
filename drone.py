import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from route_planner import RoutePlanner
from world import World


class Drone:
    def __init__(self, world):
        self.actual_world = world
        self.block = np.array([[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]])
        #self.block = np.array([[-1,-1],[0,-1],[1,-1],[1,0],[0,0],[1,1],[0,1],[-1,1],[-1,0]])
        self.drone_location = [int(self.actual_world.y_max/2), int(self.actual_world.x_max/2)]
        self.drone_height = int(self.actual_world.MAX_OBJECT_HEIGHT/2)

        #put drones in the actual_world
        self.under_drone_map_value = self.actual_world.map[tuple(self.drone_location)]
        self.actual_world.map[tuple(self.drone_location)] = self.drone_height

        # this is what the drone believes about the world
        self.world = World(self.actual_world.x_max, self.actual_world.y_max)

    def move(self):
        self.move_random_by_height()



    def move_random (self):
        points = self.drone_location + self.block
        #print(points)
        drone_new_location = random.choice (points)
        #print('Drone-location:', drone_new_location)
        self.move_to_point(drone_new_location)

    def move_random_by_height (self):
        points = self.drone_location + self.block
        #print(points)
        self.update_drone_world(points)

        valid_points = []
        for point in points:
            if point[0] in range(self.actual_world.y_max) and point[1] in range(self.actual_world.x_max):
                if self.actual_world.map[tuple(point)] < self.drone_height:
                    valid_points.append(point)

        drone_new_location = random.choice (valid_points)
        #print('Drone-location:', drone_new_location)
        self.move_to_point(drone_new_location)

    def update_drone_world (self, points):
        for point in points:
            if point[0] in range(self.world.y_max) and point[1] in range(self.world.x_max):
                self.world.map[tuple(point)] = self.actual_world.map[tuple(point)]


    def move_to_point (self, point):
        self.actual_world.map[tuple(self.drone_location)] = self.under_drone_map_value
        self.under_drone_map_value = self.actual_world.map[tuple(point)]

        self.actual_world.map[tuple(point)] = self.drone_height
        self.drone_location = point
