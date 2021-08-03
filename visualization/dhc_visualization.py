import setup

from Model.divisive_clustering import DHC
from Model.divisive_clustering import Group
from Model.divisive_clustering import naive_split

import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull #Gonna use it later
import numpy as np
import pandas as pd

import random

"""Module was created to simplify work on models locally so there is no need to create unit tests for it"""


class DHCVisualizer:
    def __init__(self,data):
        self.data = data # dataset
        self.model = DHC() # model
        self.leaves = [] # stores leaves of tree
    
    def visualize(self,levels=2):
        self.main_group = self.model.run(self.data,levels) # model returns main group that has nodes to all subgroups
        self.get_leaves(self.main_group)
        self.table = pd.DataFrame(columns=['x','y','category']) # pandas table

        for category, leaf in enumerate(self.leaves):
            for coords in leaf: # for each coords in leaf append them to pandas table with their category
                self.table = self.table.append({'x':coords[0], 'y':coords[1], 'category':'category ' + str(category)}, ignore_index=True)

        groups = self.table.groupby('category') # group table by categories

        for name, group in groups:
            plt.plot(group['x'], group['y'], marker='o', linestyle="", label=name)
        plt.legend()
        plt.show()


    def get_leaves(self, group, level=0):
        if level == 0:
            self.leaves = [] # if level is 0 clear list

        if group.subL:
            self.get_leaves(group.subL, level+1)

        if group.subR:
            self.get_leaves(group.subR, level+1)

        if group.subL == None and group.subR == None:
            self.leaves.append(group.values)

data = []

for i in range(30):
    data.append([random.uniform(0,1), random.uniform(0,1)]) # generate random data on [0,1]x[0,1] plane

#print(data)

visualizer = DHCVisualizer(data) # init visualizer
visualizer.visualize(5) # visualise result of DHC