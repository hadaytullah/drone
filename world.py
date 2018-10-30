import numpy as np
import math
import random
from objects import Resource, DropPoint, RechargePoint


class World:
    def __init__(self, x_max=50, y_max=50):
        self.MAX_OBJECT_HEIGHT = 1000 # cm, 3 story building
        self.MIN_OBJECT_HEIGHT = 300  # cm, a single story building

#        self.WORLD_HEIGHT = 50
#        self.WORLD_WIDTH = 50
        self.x_max = x_max
        self.y_max = y_max
        self.map = np.zeros((self.y_max, self.x_max))
        self.block = np.array([[-1,-1],[0,-1],[1,-1],[1,0],[0,0],[1,1],[0,1],[-1,1],[-1,0]])
        self.block_radius = 3


        self.resource_objects = {}
        self.drop_point_objects ={}
        self.recharge_point_objects ={}

        #self.drop_points = [[],[]]
        #self.resource_points = [[],[]]
        #self.recharge_points = [[],[]]
        self.clock = 0
        self.resource_timestamp = 0
        self.RESOURCE_INJECTION_PERIOD = 100

    def step(self):
        self.clock += 1

#        if(self.clock - self.resource_timestamp > self.RESOURCE_INJECTION_PERIOD):
#            self.resource_timestamp = self.clock
#            self.generate_resources()

    def campus(self):
        points = [ [math.floor(self.y_max*0.25), math.floor(self.x_max*0.25)], [math.floor(self.y_max*0.75), math.floor(self.x_max*0.25)], [math.floor(self.y_max*0.25), math.floor(self.x_max*0.75)],[math.floor(self.y_max*0.75), math.floor(self.x_max*0.75)]]

        #self.map[tuple(points[0])] = -1

        for point in points:
            self.map [tuple(point)] = random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT)

        #return world

    #--------------- Objects: Resource, Drop-point, Recharge-point ----------------
    def get_resource_points(self):
        return self.get_object_points(self.resource_objects)

    def get_drop_points(self):
        return self.get_object_points(self.drop_point_objects)

    def get_recharge_points(self):
        return self.get_object_points(self.recharge_point_objects)

    def get_object_points(self, obj_dict):
        y=[]
        x=[]
        for key, obj in obj_dict.items():
            y.append(obj.location[0])
            x.append(obj.location[1])
        return x, y

    def remove_object(self, the_object):
        if isinstance(the_object, Resource):
            self.resource_objects.pop(the_object.get_id_by_location())

        elif isinstance(the_object, DropPoint):
            self.drop_point_objects.pop(the_object.get_id_by_location())

        elif isinstance(the_object, RechargePoint):
            self.recharge_point_objects.pop(the_object.get_id_by_location())

    def generate_resources(self):
        for x in range(10):
            resource_location = [random.randint(0,self.y_max), random.randint(0,self.x_max)]
            #print('Resource location {}'.format(resource_location))
            resource = Resource(resource_location, self)
            self.resource_objects[resource.get_id_by_location()]= resource

        #self.resource_points = [random.sample(range(self.y_max), 10), random.sample(range(self.x_max), 10)]

    def generate_drop_points(self):
        for x in range(10):
            drop_point_location = [random.randint(0,self.y_max), random.randint(0,self.x_max)]
            #print('Resource location {}'.format(resource_location))
            drop_point = DropPoint(drop_point_location, self)
            self.drop_point_objects[drop_point.get_id_by_location()]= drop_point

    def generate_recharge_points(self):
        for x in range(10):
            location = [random.randint(0,self.y_max), random.randint(0,self.x_max)]
            #print('Resource location {}'.format(resource_location))
            recharge_point = RechargePoint(location, self)
            self.recharge_point_objects[recharge_point.get_id_by_location()]= recharge_point

    def generate(self, resource_points=False, drop_points=False, recharge_points=False):
        self.map = np.zeros((self.y_max, self.x_max)) #np.random.randint(2, size=(self.width,self.height))
        for i in range(math.floor(self.x_max)):
            x = random.randint(0,self.x_max-1)
            y = random.randint(0,self.y_max-1)
            self.draw_block(x,y, z=random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT), radius = random.randint(1,5))

        if drop_points:
            self.drop_points = [[5,10,20,40,45],[5,10,20,40,45]]

        if resource_points:
            self.generate_resources()

        if recharge_points:
            self.recharge_points = [random.sample(range(self.x_max), 10), random.sample(range(self.y_max), 10)]

    def generate_city(self, resource_points=False, drop_points=False, recharge_points=False):
        self.map = np.zeros((self.y_max, self.x_max)) #np.random.randint(2, size=(self.width,self.height))

        building_y = 0
        while building_y < self.y_max:
            building_x = 0
            while building_x < self.x_max:
                self.draw_block(building_x,building_y, z=random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT), radius = random.randint(1,5))
                building_x += int(0.10 * self.x_max)

            building_y += int(0.10 * self.y_max)


        #horizontal roads
        road_y = 0
        while road_y < self.y_max:
            self.map[road_y] = 0
            road_y += int((0.25)*self.y_max)

        #vertical roads
        road_x = 0
        while road_x < self.x_max:
            self.map[0:self.y_max, road_x] = 0
            road_x += int((0.25)*self.x_max)


        if drop_points:
            #self.drop_points = [[5,10,20,40,45],[5,10,20,40,45]]
            self.generate_drop_points()

        if resource_points:
            self.generate_resources()

        if recharge_points:
            self.generate_recharge_points()

            #self.recharge_points = [random.sample(range(self.x_max), 10), random.sample(range(self.y_max), 10)]

    def generate_with_roads(self, resource_points=False, drop_points=False, recharge_points=False):
        self.map = np.zeros((self.y_max, self.x_max)) #np.random.randint(2, size=(self.width,self.height))
        for i in range(math.floor(self.x_max)):
            x = random.randint(0,self.x_max-1)
            y = random.randint(0,self.y_max-1)
            self.draw_block(x,y, z=random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT), radius = random.randint(1,5))

        #horizontal roads
        road_y = 0
        while road_y < self.y_max:
            self.map[road_y] = 0
            road_y += int((0.25)*self.y_max)

        #vertical roads
        road_x = 0
        while road_x < self.x_max:
            self.map[0:self.y_max, road_x] = 0
            road_x += int((0.25)*self.x_max)


        if drop_points:
            self.drop_points = [[5,10,20,40,45],[5,10,20,40,45]]

        if resource_points:
            self.generate_resources()

        if recharge_points:
            self.recharge_points = [random.sample(range(self.x_max), 10), random.sample(range(self.y_max), 10)]


    def random (self):
        self.map = np.zeros((self.y_max, self.x_max)) #np.random.randint(2, size=(self.width,self.height))
        for i in range(math.floor(self.x_max/2)):
            x = random.randint(0,self.x_max-1)
            y = random.randint(0,self.y_max-1)
            self.draw_block(x,y, z=random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT))

    def draw_block(self, x, y, z, radius=1):
        left_top = [y - radius, x - radius]
        right_bottom = [y + radius, x + radius]

        for y in range(left_top[0], right_bottom[0]):
            for x in range(left_top[1], right_bottom[1]):
                if y in range(self.y_max) and x in range(self.x_max):
                    self.map[y,x] = z
        #return world

#    def stripes(self, w, h):
#        presence = np.zeros((h, w)) #np.random.randint(2, size=(self.width,self.height))
#        bulbs = np.zeros((h, w))
#        points = [[ math.floor(h*0.25), math.floor(w*0.25)], [math.floor(h*0.75), math.floor(w*0.25)], [math.floor(h*0.25), math.floor(w*0.75)],[math.floor(h*0.75), math.floor(w*0.75)]]
#
#        bulbs[points[0]] = -1
#
#        for point in points:
#            presence [point] = 1
#
#        return presence, bulbs
#
#    def corners(self, w, h):
#        presence = np.zeros((h, w)) #np.random.randint(2, size=(self.width,self.height))
#        bulbs = np.zeros((h, w))
#        points = [ [math.floor(h*0.25), math.floor(w*0.25)], [math.floor(h*0.75), math.floor(w*0.25)], [math.floor(h*0.25), math.floor(w*0.75)],[math.floor(h*0.75), math.floor(w*0.75)]]
#
#        bulbs[tuple(points[0])] = -1
#
#        for point in points:
#            presence [tuple(point)] = 1
#
#        return presence, bulbs
#
#    def corners2(self, w, h):
#        presence = np.zeros((h, w)) #np.random.randint(2, size=(self.width,self.height))
#        bulbs = np.zeros((h, w))
#        points = np.array([ [math.floor(h*0.25), math.floor(w*0.25)], [math.floor(h*0.75), math.floor(w*0.25)], [math.floor(h*0.25), math.floor(w*0.75)],[math.floor(h*0.75), math.floor(w*0.75)]])
#
#        #bulbs[tuple(points[0])] = -1
#
#        slash = np.array([[1,1],[0,0],[-1,-1]])
#        circle = np.array([[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]])*2
#        line = np.array([[-1,0],[0,0],[1,0]])
#        cross = np.array([[-1,-1],[0,-1],[1,-1],[0,0],[0,1]])
#
#        point = points[3]
#        for k in slash:
#            presence [tuple(point+k)] = 1
#            #bulbs[tuple(point+k)] = -1
#
#        point = points[1]
#        for k in circle:
#            presence [tuple(point+k)] = 1
#            bulbs[tuple(point+k)] = -1
#
#        point = points[2]
#        for k in line:
#            presence [tuple(point+k)] = 1
#            #bulbs[tuple(point+k)] = -1
#
#        point = points[0]
#        for k in cross:
#            presence [tuple(point+k)] = 1
#            bulbs[tuple(point+k)] = -1
#
#        return presence, bulbs
#
#
#
#    def extreme(self, w, h):
#        presence = np.zeros((h, w)) #np.random.randint(2, size=(self.width,self.height))
#        bulbs = np.zeros((h, w))
#
#        bulbs[2:5,2:w-2] = -1
#        bulbs[h-5:h-2,2:w-2] = -1
#        bulbs[5:8, int(w/2)-1:int(w/2)+2] = -1
#        bulbs[h-8:h-5, int(w/2)-1:int(w/2)+2] = -1
#
#        presence[3,4:w-4] = 1
#        presence[h-4,4:w-4] = 1
#        presence[5:7, int(w/2)] = 1
#        presence[h-7:h-5, int(w/2)] = 1
#
#        return presence, bulbs
