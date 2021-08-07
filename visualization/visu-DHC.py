import setup
import matplotlib.pyplot as plt
import random

import numpy as np
import pandas as pd

#from scipy.cluster.hierarchy import dendogram # ImportError: cannot import name 'dendogram' from 'scipy.cluster.hierarchy'
from scipy.spatial import ConvexHull

from Model.divisive_clustering import Group
from Model.divisive_clustering import DHC

"""Module was created to simplify work on models locally so there is no need to create unit tests for it"""

class Labels:
    """Implements motion_notify_event"""

    def __init__(self, fig, ax, annot, points, lines, polygons, **kwargs):
        """
        Parameters:
        --------
        fig: Figure
        ax: axes.Axes
        annot: Annotation
        points: list of Path objects
        lines: list of Line2D objects
        polygons: list of Polygon objects
        """

        self.fig = fig
        self.ax = ax
        self.annot = annot

        self.points = points
        self.lines = lines
        self.polygons = polygons

        # with kwargs it is easy to swap update_{point,line,polygon}_annot functions
        # but this feature will be developed later
        # now it is impossible
        for k, v in kwargs.items():
            setattr(self, k, v)

    def update_point_annot(self, point, coords):
        """
        Updates point annotation
        """

        x, y = coords
        self.annot.xy = (x,y)
        self.annot.set_text(point.get_label())

    def update_line_annot(self, line, coords):
        """
        Updates line annotation
        """
        x, y = coords
        self.annot.xy = (x,y)
        self.annot.set_text(line.get_label())

    def update_polygon_annot(self, polygon, coords):
        """
        Updates polygon annotation
        """

        x, y = coords
        self.annot.xy = (x,y)
        self.annot.set_text(polygon.get_label())

    def __call__(self, event):
        """
        Function searches for objects (Path, Line2D, Polygon) which contain current event.
        Order is important because Path objects(ordinary points) are on the top of the plot 
        and Polygon objects are on the bottom of the plot.
        """
        vis = self.annot.get_visible()

        if event.inaxes == self.ax:

            # filters objects from set of points(plt.scatter) that contains current event
                objects = list(filter(lambda x: x.contains(event)[0], self.points))

                if len(objects) > 0: # points
                    point = objects[-1]
                    self.update_point_annot(point, (event.xdata, event.ydata))

                    self.annot.set_visible(True)
                    self.fig.canvas.draw_idle()
                else:
                    # filters object from set of lines(plt.plot) that contains current event
                    objects = list(filter(lambda x: x.contains(event)[0], self.lines))

                    if len(objects) > 0: # lines
                        line = objects[-1]
                        self.update_line_annot(line, (event.xdata, event.ydata))

                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                    else:
                        # filters object from set of polygons(plt.fill) that contains current event
                        objects = list(filter(lambda x: x.contains(event)[0], self.polygons))

                        if len(objects) > 0: # polygons
                            polygon = objects[-1]
                            self.update_polygon_annot(polygon, (event.xdata, event.ydata))

                            self.annot.set_visible(True)
                            self.fig.canvas.draw_idle()
                        else:
                            if vis:
                                self.annot.set_visible(False)
                                self.fig.canvas.draw_idle()

class PolygonHighlight:
    """
    Implements button_press_event and button_release_event
    Polygons are on the bottom of the plot so highlighting makes it easy to see the whole group
    """

    def __init__(self, fig, ax, annot, polygons, **kwargs):
        """
        Parameters:
        --------
        fig: Figure
        ax: axes.Axes
        annot: Annotation
        polygons: list of Polygon objects
        """
        self.fig = fig
        self.ax = ax
        self.annot = annot
        
        self.polygons = polygons

        for k, v in kwargs.items():
            setattr(self, k, v)

        self.plotted_convex = None

    def on_press(self, event):
        """Draw convex hull for polygon that belongs to current event"""
        
        if event.inaxes == self.ax:
            objects = list(filter(lambda x: x.contains(event)[0], self.polygons))
            
            if len(objects) > 0:
                polygon = objects[-1]
                path = polygon.get_xy()
                self.plotted_convex,  = self.ax.plot(path[..., 0], path[..., 1], color='red')

    def on_release(self, event):
        """Removes last convex hull"""
        if self.plotted_convex:
            self.plotted_convex.remove()
            self.plotted_convex = None


class VisuDHCHulls:
    def __init__(self, data):
        self.data = data    #dataset
        self.model = DHC()  #model
        self.groups = []    #stores leaves of tree
        self.group_data = [] #list of tuples (group_level, group_size)
    
    def visualize(self, levels=2):
        self.main_group = self.model.run(self.data, levels)  #model returns main group that has nodes to all subgroups
        self.get_groups(self.main_group)

        # matplotlib and scipy use numpy 
        self.groups = np.array([np.array(group, dtype=object) for group in self.groups], dtype=object)
        self.data = np.array([np.array(point, dtype=object) for point in self.data], dtype=object)

        fig, ax = plt.subplots()
        annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        points = []
        lines = []
        polygons = []

        # what's important: ax.plot and ax.fill return Line2D list and Polygon list 
        # but in our case those lists are singletons so main lists of lines and polygons can be extended with those returned
        # by mentioned functions
        for group, label in zip(self.groups, self.group_data):
            group_label = 'level=' + str(label[0]) + '\nsize=' + str(label[1])

            if len(group) > 2:
                hull = ConvexHull(group)
                polygons_ = ax.fill(group[hull.vertices,0], group[hull.vertices,1],
                     alpha=0.3, label=group_label) # make polygon
                polygons.extend(polygons_)
            elif len(group) == 2:
                lines_ = ax.plot(group[...,0], group[...,1], lw=2, label=group_label) # make line
                lines.extend(lines_)
            else:
                point = ax.scatter(group[...,0], group[...,1], zorder=3, marker='o', color='black',
                 label=group_label) # make single point
                points.append(point)

        onhover = Labels(fig, ax, annot, points, lines, polygons)
        highlights = PolygonHighlight(fig, ax, annot, polygons)

        fig.canvas.mpl_connect('motion_notify_event', onhover)
        fig.canvas.mpl_connect('button_press_event', highlights.on_press)
        fig.canvas.mpl_connect('button_release_event', highlights.on_release)
        plt.show()


    def get_groups(self, group, level=0):
        if level == 0:
            self.groups = []    #if level is 0 clear list
            self.group_data = []

        self.groups.append(group.values)
        self.group_data.append((level,len(group.values)))

        if group.subL:
            self.get_groups(group.subL, level+1)

        if group.subR:
            self.get_groups(group.subR, level+1)

#Visualizes hierarchical clustering by dendogram
class VisuDHCDendogram:
    def __init__(self, data):
        self.data = data
        self.model = DHC()

    #Converts to scipy linkage matrix format
    def to_linkage_matrix(G):
        #WIP
        pass

    def visualize(self, depth):
        G = self.model.run(self.data, depth)   #Run model -> it returns tree-like hierarchical group structure 
        Z = self.to_linkage_matrix(G)          #Converts to scipy-compatible linkage matrix

        plt.figure()
        d = dendogram(Z)
        plt.show()


def convex_hull_visualization(data=None, depth=1):


    if not data:
        center1 = (50, 60)
        center2 = (80, 20)
        distance = 20


        group1 = np.random.uniform(center1[0], center1[0] + distance, size=(100,2))
        group2 = np.random.uniform(center2[0], center2[0] + distance, size=(100,2))
        data = np.concatenate((group1, group2)).tolist() # DHC does not support numpy arrays
    

    v = VisuDHCHulls(data)
    v.visualize(depth)



data = [[1,1], [2,2], [1,2], [2,1], [3,1], [-1,-2], [-3,-1], [-1,-1], [-2,-2], [0,1], [1,0], [-2,-1], [3,2], [2,3]]
convex_hull_visualization(None, 2)
