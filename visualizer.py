import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import cv2

class orientation_plotter:
    def __init__(self):
        self.fig_ori = plt.figure()
        self.ax_ori = self.fig_ori.add_subplot(projection='3d')
        self.ax_ori.view_init(45, -80) # ax2.view_init(90, -90)  # x-y perspective

        self.ax_ori.plot([0, 1], [0, 0], [0, 0],"--",color="black", label="Global Reference Plane")
        self.ax_ori.plot([0, 0], [0, 1], [0, 0],"--",color="black")
        self.ax_ori.plot([0, 0], [0, 0], [0, 1],"--",color="black")

    def plot_axis(self, R, main_label = "Axis"):
        x_axis = R[:,0]
        y_axis = R[:,1]
        z_axis = R[:,2]
        self.ax_ori.plot([0, x_axis[0]], [0, x_axis[1]], [0, x_axis[2]],color="red",   label = "x " + main_label , linewidth=5)
        self.ax_ori.plot([0, y_axis[0]], [0, y_axis[1]], [0, y_axis[2]],color="blue",  label = "y " + main_label, linewidth=5)
        self.ax_ori.plot([0, z_axis[0]], [0, z_axis[1]], [0, z_axis[2]],color="green", label = "z " + main_label, linewidth=5)


    def plot_axis2(self, R, main_label = "Axis"):
        x_axis = R[:,0] * 1.5
        y_axis = R[:,1] * 1.5
        z_axis = R[:,2] * 1.5
        self.ax_ori.plot([0, x_axis[0]], [0, x_axis[1]], [0, x_axis[2]],"--",color="red",   label = "x " + main_label , linewidth=3)
        self.ax_ori.plot([0, y_axis[0]], [0, y_axis[1]], [0, y_axis[2]],"--",color="blue",  label = "y " + main_label, linewidth=3)
        self.ax_ori.plot([0, z_axis[0]], [0, z_axis[1]], [0, z_axis[2]],"--",color="green", label = "z " + main_label, linewidth=3)
        
    def reset(self):
        self.ax_ori.cla()
        self.ax_ori.plot([0, 1], [0, 0], [0, 0],"--",color="black", label="Global Reference Plane")
        self.ax_ori.plot([0, 0], [0, 1], [0, 0],"--",color="black")
        self.ax_ori.plot([0, 0], [0, 0], [0, 1],"--",color="black")
        
    def get_plot(self,title):
        bound = 1.2
        self.ax_ori.set_xlim([-bound,bound])
        self.ax_ori.set_ylim([-bound,bound])
        self.ax_ori.set_zlim([-bound,bound])

        self.ax_ori.set_xlabel('Global X')
        self.ax_ori.set_ylabel('Global Y')
        self.ax_ori.set_zlabel('Global Z')

        self.ax_ori.set_title(title)
        self.ax_ori.legend(loc='upper left')

        self.fig_ori.canvas.draw()
        image_ori = np.frombuffer(self.fig_ori.canvas.tostring_rgb(), dtype=np.uint8)
        image_ori = image_ori.reshape(self.fig_ori.canvas.get_width_height()[::-1] + (3,))
        image_ori = cv2.cvtColor(image_ori, cv2.COLOR_RGB2BGR)
        return image_ori
    

class velocity_plotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots(3,figsize=(6,6))
        self.size_gt = 20
        self.size_es = 15
        self.col_gt = "green"
        self.col_es = "red"

    def add_gt_point(self, time, vel):
        self.ax[0].scatter(time, vel[0],s=self.size_gt, c=self.col_gt)
        self.ax[1].scatter(time, vel[1],s=self.size_gt, c=self.col_gt)
        self.ax[2].scatter(time, vel[2],s=self.size_gt, c=self.col_gt)

    def add_es_point(self, time, vel):
        self.ax[0].scatter(time, vel[0],s=self.size_es, c=self.col_es)
        self.ax[1].scatter(time, vel[1],s=self.size_es, c=self.col_es)
        self.ax[2].scatter(time, vel[2],s=self.size_es, c=self.col_es)


    def reset(self):
        self.ax[0].cla()
        self.ax[1].cla()
        self.ax[2].cla()
        
    def get_plot(self):
        self.ax[0].set_ylabel('NORTH')
        self.ax[1].set_ylabel('EAST')
        self.ax[2].set_ylabel('DOWN')
        self.ax[0].set_title('Velocity versus Time')
                
        self.fig.canvas.draw()
        image_from_plot = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        image_from_plot = image_from_plot.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        image_from_plot = cv2.cvtColor(image_from_plot, cv2.COLOR_RGB2BGR)

        return image_from_plot
    


class location_plotter:
    def __init__(self,location,time):
        self.fig, self.ax = plt.subplots(1,2,figsize=(8,4))
        self.bound = 1.2
        self.col = "red"

        self.ax[0].plot(location[:,1], location[:,0],"--",color="blue",linewidth=0.5)
        #ax.set_box_aspect([1,1,1]) # IMPORTANT - this is the new, key line
        self.ax[0].set_xlabel('NORTH')
        self.ax[0].set_ylabel('EAST')
        self.ax[0].set_title('NORT-EAST Trajectory')
        
        # self.ax[0].set_xlim([-400,400])
        # self.ax[0].set_ylim([-600,200])

        self.ax[1].plot(time, location[:,2],"--",color="blue",linewidth=0.5)
        #ax.set_box_aspect([1,1,1]) # IMPORTANT - this is the new, key line
        self.ax[1].set_xlabel('time(sec)')
        self.ax[1].set_ylabel('DOWN')
        self.ax[1].set_title('DOWN versus Time')
        # self.ax[1].set_ylim([-40,20])

    def add_point(self, curr_loc, curr_time):
        self.ax[0].scatter(curr_loc[0], curr_loc[1],s=3,c=self.col)
        self.ax[1].scatter(curr_time,curr_loc[2],s=3,c=self.col)

    def get_plot(self):
        self.fig.canvas.draw()
        image_from_plot = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        image_from_plot = image_from_plot.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        image_from_plot = cv2.cvtColor(image_from_plot, cv2.COLOR_RGB2BGR)

        return image_from_plot