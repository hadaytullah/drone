import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from route_planner import RoutePlanner
from world import World
from drone import Drone
from message_dispatcher import MessageDispatcher



class DroneSimulator:
    def __init__(self):
        self.x_max = 50
        self.y_max = 50
        self.world = World(self.x_max, self.y_max)
        #self.world.random()
        #self.world.generate_with_roads(resource_points=True, drop_points = True, recharge_points=True)
        self.world.generate_city(resource_points=True, drop_points = True, recharge_points=True)

        # drones may have different charaterisics, battery size, max lift, max weight carrying capacity, turning abilities? some might make only right turns?
        self.drones = []
        self.drone_world_plots = []

        self.message_dispatcher = MessageDispatcher()
        self.drone_alpha = Drone('URBAN0X1', self.world,self.message_dispatcher, cooperate=True)
        self.drones.append(self.drone_alpha)

        self.drone_beta = Drone('URBAN0X2', self.world,self.message_dispatcher, cooperate=True)
        self.drones.append(self.drone_beta)

        #self.drone_gamma = Drone('URBAN0X3', self.world,self.message_dispatcher, cooperate=False)
        #self.drones.append(self.drone_gamma)



        #self.fig = plt.figure(figsize=(1, 2))#, dpi=80, facecolor='w', edgecolor='k')
        self.drop_point_marker = 'o'
        #self.world.drop_point_locations = [random.sample(range(self.world.x_max), 10), random.sample(range(self.world.y_max), 10)]
        self.drop_point_plot = None


        #reacharge point
        self.recharge_point_marker = 's' #square
        self.recharge_point_plot = None

        #resources
        #self.fig = plt.figure(figsize=(1, 2))#, dpi=80, facecolor='w', edgecolor='k')
        #self.world.resource_locations = [[5,10,20,40,45],[5,10,20,40,45]]
        self.resource_plot = None
        self.resource_marker = 'v'

        self.markers = ['|','+','x','*']
        self.colors = ['r','k','g','c','m','b']
        self.init_figures()

        #

#    def create_plot(self, location, title, data, plot_cmap='gray_r', plot_interpolation='nearest', plot_vmin=0, plot_vmax=1, plot_animated=False):
#        plot = self.fig.add_subplot(location)
#        plot.set_title(title, y=1.08)
#        plot.xaxis.tick_top()
#        #presence_plot_x, presence_plot_y = np.meshgrid(np.arange(self.width), np.arange(self.height))
#        plt.gca().invert_yaxis()
#        #presence_plot.scatter(presence_plot_x, presence_plot_y, c=self.presence, cmap='gray_r', marker='+')
#        #presence_plot.grid(color='g', linestyle='-', linewidth=1)
#        #presence_draw_array = np.where(self.presence<1, 1, 0)
#        plot.set_xticks(np.arange(self.x_max)+0.5)
#        plot.set_yticks(np.arange(self.y_max)+0.5)
#        plot.set_yticklabels([])
#        plot.set_xticklabels([])
#        image = plot.imshow(data, cmap=plot_cmap, interpolation=plot_interpolation, vmin=plot_vmin, vmax=plot_vmax, animated=plot_animated)
#        plot = plot.plot([0], [0], color=self.colors.pop(), linestyle='', marker=self.markers.pop(),
#     markerfacecolor='red', markersize=3)  # for lines
#        #plt.imshow(data, cmap=plot_cmap, interpolation=plot_interpolation, vmin=plot_vmin, vmax=plot_vmax, animated=plot_animated)
#        #plt.grid()
#        return image, plot[0]

    def init_plot(self, location, title):
        plot = self.fig.add_subplot(location)
        plot.set_title(title, y=1.08)
        plot.xaxis.tick_top()
        #presence_plot_x, presence_plot_y = np.meshgrid(np.arange(self.width), np.arange(self.height))
        plt.gca().invert_yaxis()
        #presence_plot.scatter(presence_plot_x, presence_plot_y, c=self.presence, cmap='gray_r', marker='+')
        #presence_plot.grid(color='g', linestyle='-', linewidth=1)
        #presence_draw_array = np.where(self.presence<1, 1, 0)
        plot.set_xticks(np.arange(self.x_max)+0.5)
        plot.set_yticks(np.arange(self.y_max)+0.5)
        plot.set_yticklabels([])
        plot.set_xticklabels([])
        return plot



    def init_figures(self):
        self.fig_rows = 1
        self.fig_images = len(self.drones)+1
        self.fig = plt.figure(figsize=(self.fig_rows, self.fig_images))#, dpi=80, facecolor='w', edgecolor='k')

        #Let there be light, the world begins
        #self.fig.set_size_inches(200,200)
        plot_location = int(str(self.fig_rows)+str(self.fig_images)+ str(1))
        self.world_plot = self.init_plot(location=plot_location, title='World')
        self.world_image = self.world_plot.imshow(self.world.map, cmap='Blues', interpolation='nearest', vmin=self.world.MIN_OBJECT_HEIGHT, vmax=self.world.MAX_OBJECT_HEIGHT, animated=False)



        #self.drop_point_plot = (self.world_plot.plot(self.world.drop_points[1], self.world.drop_points[0], color=self.colors.pop(), linestyle='', marker=self.drop_point_marker, markerfacecolor='white', markersize=3))[0]

        #Let there be resources
        resources_x, resources_y = self.world.get_resource_points()
        self.resource_plot = (self.world_plot.plot(resources_x, resources_y, color='red', linestyle='', marker=self.resource_marker, markerfacecolor='white', markersize=3))[0]
        #plt.gca().invert_yaxis()

        #Let there be drop points
        drop_points_x, drop_points_y = self.world.get_drop_points()
        self.drop_point_plot = (self.world_plot.plot(drop_points_x, drop_points_y, color='black', linestyle='', marker=self.drop_point_marker, markerfacecolor='white', markersize=3))[0]

        #Let there be recharge points
        #Let there be drop points
        recharge_points_x, recharge_points_y = self.world.get_recharge_points()
        self.recharge_point_plot = (self.world_plot.plot(recharge_points_x, recharge_points_y, color='magenta', linestyle='', marker=self.recharge_point_marker, markerfacecolor='white', markersize=3))[0]


        # Let there be drones
        #self.fig_drone_0 = plt.figure(figsize=(1, 2))#, dpi=80, facecolor='w', edgecolor='k')
        #self.fig.set_size_inches(200,200)
        for i,drone in enumerate(self.drones):
            drone.marker = self.markers.pop()
            plot_location = int(str(self.fig_rows) + str(self.fig_images)+ str(i+2))
            #print(plot_location)
            drone.world_plot = self.init_plot(location=plot_location, title='Drone '+drone.uid+ ' View:'+ drone.marker)
            drone.world_image = drone.world_plot.imshow(self.drones[0].world.map, cmap='Blues', interpolation='nearest', vmin=self.drones[0].world.MIN_OBJECT_HEIGHT, vmax=self.drones[0].world.MAX_OBJECT_HEIGHT, animated=True)
            #drone.location_plot = (drone.world_plot.plot([drone.location[1]], [drone.location[0]], color=self.colors.pop(), linestyle='', marker=self.markers.pop(), markerfacecolor='red', markersize=3))[0]
            drone.location_plot = (self.world_plot.plot([drone.location[1]], [drone.location[0]], color=self.colors.pop(), linestyle='', marker=drone.marker, markerfacecolor='red', markersize=3))[0]
            #print(drone.location_plot)
            #self.drone_world_plots.append(drone_world_plot)


    def update(self, args):
        #print('update--')

        #drone_locations_y = []
        #drone_locations_x = []
        self.world.step()
        for i,drone in enumerate(self.drones):
            drone.move()
            #print(drone.location_plot)
            drone.world_image.set_data(drone.world.map)
            drone.location_plot.set_data([drone.location[1]],[drone.location[0]])
            #drone_locations_y.append(drone.location[0])
            #drone_locations_x.append(drone.location[1])
            #self.drone_world_plots[i].set_data(drone.world.map)

            #self.drone_world_plots.gca().plot
            #self.world_plot.plot(drone.location[0], drone.location[1], marker='o', markersize=3, color="red")
        #for drone_world_plot in self.drone_world_plots
        #    self.drone_world_plot_0.set_data(self.drones[0].world.map)

        self.world_image.set_data(self.world.map)

        x, y = self.world.get_resource_points()
        self.resource_plot.set_data([x],[y])

        drop_point_x, drop_point_y = self.world.get_drop_points()
        self.drop_point_plot.set_data([drop_point_x],[drop_point_y])

        recharge_point_x, recharge_point_y = self.world.get_recharge_points()
        self.recharge_point_plot.set_data([recharge_point_x],[recharge_point_y])

        #self.world_drone_plot.set_data([drone_locations_x,drone_locations_y])
        #self.im.set_array(self.luminosity)
        #self.im.set_facecolors(self.luminosity)


        #self.luminosity_im.set_data(self.luminosity_extrapolate(self.luminosity))
        #im.set_cmap("gray")
        #im.update()
        #self.steps += 1
        #if self.steps > self.MAX_STEPS:
        #    self.ani.event_source.stop()
        #    plt.grid()
        #    plt.grid()
        return self.world_image,

    def run(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50, blit=True)
        #self.update([])
        plt.show()
