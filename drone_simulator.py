import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from route_planner import RoutePlanner
from world import World
from drone import Drone



class DroneSimulator:
    def __init__(self):
        self.x_max = 50
        self.y_max = 50
        self.world = World(self.x_max, self.y_max)
        #self.world.random()
        self.world.generate()

        self.drones = [Drone(self.world), Drone(self.world), Drone(self.world)]
        self.drone_world_plots = []


        #self.fig = plt.figure(figsize=(1, 2))#, dpi=80, facecolor='w', edgecolor='k')
        self.init_figures()


    def create_plot(self, location, title, data, plot_cmap='gray_r', plot_interpolation='nearest', plot_vmin=0, plot_vmax=1, plot_animated=False):
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
        image = plt.imshow(data, cmap=plot_cmap, interpolation=plot_interpolation, vmin=plot_vmin, vmax=plot_vmax, animated=plot_animated)
        #plt.grid()
        return image

    def init_figures(self):
        self.fig_rows = 1
        self.fig_images = len(self.drones)+1
        self.fig = plt.figure(figsize=(self.fig_rows, self.fig_images))#, dpi=80, facecolor='w', edgecolor='k')

        #self.fig.set_size_inches(200,200)
        plot_location = int(str(self.fig_rows)+str(self.fig_images)+ str(1))
        self.world_plot = self.create_plot(location=plot_location, title='World', data=self.world.map, plot_cmap='Blues', plot_interpolation='nearest', plot_vmin=self.world.MIN_OBJECT_HEIGHT, plot_vmax=self.world.MAX_OBJECT_HEIGHT)

        #self.fig_drone_0 = plt.figure(figsize=(1, 2))#, dpi=80, facecolor='w', edgecolor='k')
        #self.fig.set_size_inches(200,200)
        for i,drone in enumerate(self.drones):
            plot_location = int(str(self.fig_rows)+str(self.fig_images)+ str(i+2))
            print(plot_location)
            drone_world_plot = self.create_plot(location=plot_location, title='Drone World', data=self.drones[0].world.map, plot_cmap='Blues', plot_interpolation='nearest', plot_vmin=self.drones[0].world.MIN_OBJECT_HEIGHT, plot_vmax=self.drones[0].world.MAX_OBJECT_HEIGHT)
            self.drone_world_plots.append(drone_world_plot)


    def update(self, args):
        #print('update--')

        for i,drone in enumerate(self.drones):
            drone.move()
            self.drone_world_plots[i].set_data(drone.world.map)

        #for drone_world_plot in self.drone_world_plots
        #    self.drone_world_plot_0.set_data(self.drones[0].world.map)

        self.world_plot.set_data(self.world.map)

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
        return self.world_plot,

    def run(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=50, blit=True)
        #self.update([])
        plt.show()
