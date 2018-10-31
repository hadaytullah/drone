
import random
#from drone import Drone

class MapObject:
    """Objects that agents are picking up.
    """
    def __init__(self, location, world):
        self.location = location
        self.world = world


    def get_id_by_location(self):
        return str(self.location[0])+'-'+str(self.location[1])

    def apply_drone(self, drone):
        #if isinstance(apply_obj, Drone):
        #drone = apply_obj
        #if drone.pick(self):
        self.world.remove_object(self)


    @staticmethod
    def location_to_id(self, location):
        return str(location[0])+'-'+str(location[1])

class Resource (MapObject):
    """Objects that agents are picking up.
    """
    def __init__(self, location, world):
        super().__init__(location, world)
        self.weight = 10 #random.randint(10,50) #grams
        self.area = 10 # random.randint(9,100) # m^2


class RechargePoint(MapObject):
    def __init__(self, location, world):
        super().__init__(location, world)
        self.charge_available = random.randint(500,3000) #WATT ?

class DropPoint(MapObject):
    def __init__(self, location, world):
        super().__init__(location, world)
        self.weight_capacity = random.randint(100,300) #grams
        self.area_capacity = random.randint(100,500)

        self.weight_occupied = 0
        self.area_occupied = 0

        #self.name = "DropPoint#{:0<3}".format(self.uid)

#    def drop_resource(self, resource):
#        if self.weight_occupied+resource.weight < self.weight_capacity and self.area_occupied+resource.area < self.area_capacity:
#            self.weight_occupied += resource.weight
#            self.area_occupied += resource.area
#            return True # resource accepted
#
#        return False # no more capacity bro!





