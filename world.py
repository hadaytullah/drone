import numpy as np
import math
import random

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

    def campus(self):
        points = [ [math.floor(self.y_max*0.25), math.floor(self.x_max*0.25)], [math.floor(self.y_max*0.75), math.floor(self.x_max*0.25)], [math.floor(self.y_max*0.25), math.floor(self.x_max*0.75)],[math.floor(self.y_max*0.75), math.floor(self.x_max*0.75)]]

        #self.map[tuple(points[0])] = -1

        for point in points:
            self.map [tuple(point)] = random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT)

        #return world
    def generate(self):
        self.map = np.zeros((self.y_max, self.x_max)) #np.random.randint(2, size=(self.width,self.height))
        for i in range(math.floor(self.x_max)):
            x = random.randint(0,self.x_max-1)
            y = random.randint(0,self.y_max-1)
            self.draw_block(x,y, z=random.randint(self.MIN_OBJECT_HEIGHT, self.MAX_OBJECT_HEIGHT), radius = random.randint(1,5))

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
