
import random
#from drone import Drone

class Resource:
    """Objects that agents are picking up.
    """
    def __init__(self, location, world):
        self.weight = random.randint(10,50) #grams
        self.area = random.randint(9,100) # m^2
        self.location = location
        self.drop_point = None

        self.world = world


    def get_id_by_location(self):
        return str(self.location[0])+'-'+str(self.location[1])

    def apply_drone(self, drone):
        #if isinstance(apply_obj, Drone):
        #drone = apply_obj
        self.world.remove_object(self)


    @staticmethod
    def location_to_id(self, location):
        return str(location[0])+'-'+str(location[1])

class RechargePoint:
    def __init__(self, uid, location):
        self.charge_available = random.randint(500,1000) #WATT ?
        self.location = location

class DropPoint:
    def __init__(self, uid, location):
        self.weight_capacity = random.randint(100,300) #grams
        self.area_capacity = random.randint(100,500)
        self.location = location

        self.weight_occupied = 0
        self.area_occupied = 0

        self.name = "DropPoint#{:0<3}".format(self.uid)

    def drop_resource(self, resource):
        if self.weight_occupied+resource.weight < self.weight_capacity and self.area_occupied+resource.area < self.area_capacity:
            self.weight_occupied += resource.weight
            self.area_occupied += resource.area
            return True # resource accepted

        return False # no more capacity bro!







