import setup
import matplotlib.pyplot as plt
import random

import numpy as np
import pandas as np

from scipy.cluster.hierarchy import dendogram # ImportError: cannot import name 'dendogram' from 'scipy.cluster.hierarchy'
from scipy.spatial import ConvexHull

from Model.divisive_clustering import Group
from Model.divisive_clustering import DHC

"""Module was created to simplify work on models locally so there is no need to create unit tests for it"""

class VisuDHCHulls:
    def __init__(self, data):
        self.data = data    #dataset
        self.model = DHC()  #model
        self.groups = []    #stores leaves of tree
        self.group_data = [] #gonna use it later as labels
    
    def visualize(self, levels=2):
        self.main_group = self.model.run(self.data, levels)  #model returns main group that has nodes to all subgroups
        self.get_groups(self.main_group)

        # matplotlib and scipy use numpy 
        self.groups = np.array([np.array(group) for group in self.groups])
        self.data = np.array([np.array(point) for point in self.data])

        for group in self.groups:
            if len(group) > 2:
                hull = ConvexHull(group)
                plt.fill(group[hull.vertices,0], group[hull.vertices,1], alpha=0.3) # make polygon
            elif len(group) == 2:
                plt.plot(group[...,0], group[...,1], lw=2) # make line
            else:
                plt.scatter(group[...,0], group[...,1], zorder=3, marker='o') # make single point

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
        center1 = (0.5, 0.3)
        center2 = (-0.5, 1.0)

        group1 = np.random.uniform(center1[0], center1[1], size=(10,2))
        group2 = np.random.uniform(center2[0], center2[1], size=(10,2))

        data = np.concatenate((group1, group2)).tolist() # DHC does not support numpy arrays
    

    v = VisuDHCHulls(data)
    v.visualize(depth)



data = [[1,1], [2,2], [1,2], [2,1], [3,1], [-1,-2], [-3,-1], [-1,-1], [-2,-2], [0,1], [1,0], [-2,-1], [3,2], [2,3]]
convex_hull_visualization(data, 2)
