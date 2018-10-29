import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from route_planner import RoutePlanner
from world import World
from message import Message
from search.astar import astar

class Drone:
    def __init__(self, uid, world, message_dispatcher, cooperate):
        self.uid = uid
        self.actual_world = world
        self.block = np.array([[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]])
        #self.block = np.array([[-1,-1],[0,-1],[1,-1],[1,0],[0,0],[1,1],[0,1],[-1,1],[-1,0]])

        #put drones in the actual_world
        self.location = [int(self.actual_world.y_max/2), int(self.actual_world.x_max/2)]
        if self.actual_world.map[tuple(self.location)] is 0:
            self.drone_height = int(self.actual_world.MAX_OBJECT_HEIGHT/2)
        else:
            self.drone_height = 5 + self.actual_world.map[tuple(self.location)] #int(self.actual_world.MAX_OBJECT_HEIGHT/2)
        #self.location_as_grid = np.zeros((self.actual_world.y_max, self.actual_world.x_max))
        #self.under_drone_map_value = self.actual_world.map[tuple(self.location)]
        #self.actual_world.map[tuple(self.location)] = self.drone_height

        # Views, to be set by the simulator
        self.world_plot = None
        self.world_image = None
        self.location_plot = None

        # this is what the drone believes about the world
        self.world = World(self.actual_world.x_max, self.actual_world.y_max)


        # cooperation
        self.cooperate = cooperate
        self.message_dispatcher = message_dispatcher
        self.message_dispatcher.register(self)

        # profile
        self.owner = 'COMPANY-'+random.choice(['X','Y','Z'])

        # goal is pick & drop for all drones
        # self.goal =
        self.paths = []
        self.current_path = []

    def receive(self, message):
        if self.cooperate:
            if message.sender is not self: #avoid own messages
                if isinstance(message, Message):
                    print ('Message Recieved {} from Agent {}, points {}'.format(message.uid, message.sender.uid, len(message.points)))
                    for index, point in enumerate(message.points):
                        if point[0] in range(self.world.y_max) and point[1] in range(self.world.x_max):
                            self.world.map[tuple(point)] = message.points_info[index]

    def send(self, points, points_info):
        if self.cooperate:
            message = Message(self, points, points_info)
            self.message_dispatcher.broadcast(message)

    def move(self):
        self.update_drone_world()
        self.share_info() # cooperation

        self.move_in_own_world ()

    def move_in_actual_world(self):
        print('Drone {} Height:{}'.format(self.uid, self.drone_height))
        if len(self.current_path) is 0:

            self.impassable_map = (self.actual_world.map >  self.drone_height).astype(int)

            print('impassable {}'.format(self.impassable_map))
            start = tuple(self.location) #(0, 0)
            #index = random.choice(range(len(self.actual_world.resource_points[0])))
            #random.choice(self.actual_world.resource_objects)
            obj_id, self.destination_object = random.choice(list(self.actual_world.resource_objects.items()))
            # goal = (self.actual_world.resource_points[0][index], self.actual_world.resource_points[1][index])#(9, 9)
            #self.goal_location = tuple(resource.location)
            self.current_path = astar(self.impassable_map, start, tuple(self.destination_object.location), moore=True)
            print(self.current_path)
        else:
            #point = self.current_path.pop(0)
            #if len(self.current_path) is 1: # at destination
            self.move_to_point(list(self.current_path.pop(0)))

        if self.destination_object:
            if self.location == self.destination_object.location:
                self.destination_object.apply_drone(self)
                self.destination_object = None

        #self.move_random_by_height()

    def move_in_own_world(self):
        print('Drone {} Height:{}'.format(self.uid, self.drone_height))
        if len(self.current_path) is 0:
            # Drone considers own assumption about the world for routing
            self.impassable_map = (self.world.map >  self.drone_height).astype(int)

            print('impassable {}'.format(self.impassable_map))
            start = tuple(self.location) #(0, 0)
            #index = random.choice(range(len(self.actual_world.resource_points[0])))
            #random.choice(self.actual_world.resource_objects)
            obj_id, self.destination_object = random.choice(list(self.actual_world.resource_objects.items()))
            # goal = (self.actual_world.resource_points[0][index], self.actual_world.resource_points[1][index])#(9, 9)
            #self.goal_location = tuple(resource.location)
            self.current_path = astar(self.impassable_map, start, tuple(self.destination_object.location), moore=True)
            print(self.current_path)
        else:
            #point = self.current_path.pop(0)
            #if len(self.current_path) is 1: # at destination
            if self.move_to_point(list(self.current_path.pop(0))) is False: # Hit a road block
                #Re-routing
                self.impassable_map = (self.world.map >  self.drone_height).astype(int)
                start = tuple(self.location)
                self.current_path = astar(self.impassable_map, start, tuple(self.destination_object.location), moore=True)


        if self.destination_object:
            if self.location == self.destination_object.location:
                self.destination_object.apply_drone(self)
                self.destination_object = None



    def move_random (self):
        points = self.location + self.block
        #print(points)
        drone_new_location = random.choice (points)
        #print('Drone-location:', drone_new_location)
        self.move_to_point(drone_new_location)

    def move_random_by_height (self):
        points = self.location + self.block
        #print(points)

        valid_points = []
        for point in points:
            if point[0] in range(self.actual_world.y_max) and point[1] in range(self.actual_world.x_max):
                if self.actual_world.map[tuple(point)] < self.drone_height:
                    valid_points.append(point)

        if len(valid_points):
            drone_new_location = random.choice (valid_points)
            #print('Drone-location:', drone_new_location)
            self.move_to_point(drone_new_location)

    def share_info(self):
        points = self.location + self.block
        share_points = []
        share_points_info = []

        for point in points:
            if point[0] in range(self.world.y_max) and point[1] in range(self.world.x_max):
                share_points.append(point)
                share_points_info.append(self.actual_world.map[tuple(point)])

        self.send(share_points, share_points_info)

    def update_drone_world (self):
        points = self.location + self.block
        for point in points:
            if point[0] in range(self.world.y_max) and point[1] in range(self.world.x_max):
                self.world.map[tuple(point)] = self.actual_world.map[tuple(point)]


    def move_to_point (self, point):
        #self.actual_world.map[tuple(self.location)] = self.under_drone_map_value
        #self.under_drone_map_value = self.actual_world.map[tuple(point)]

        #self.actual_world.map[tuple(point)] = self.drone_height
        if self.actual_world.map[tuple(point)] < self.drone_height:
            self.location = point
            return True
        return False

        #self.location_as_grid[tuple(self.location)] = 0
        #self.location_as_grid[tuple(point)] = self.drone_height

#    def move_to_point (self, point):
#        self.actual_world.map[tuple(self.location)] = self.under_drone_map_value
#        self.under_drone_map_value = self.actual_world.map[tuple(point)]
#
#        self.actual_world.map[tuple(point)] = self.drone_height
#        self.location = point
