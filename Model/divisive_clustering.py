from math import sqrt
from .model_baseclass import Model

def swap(a, b):
    return b, a

#Tree-like structure that output hierarchy is stored in
class Group:
    def __init__(self, values):
        self.values = values    #Points inside this group
        self.subL = None        #
        self.subR = None        #Subgroups

#Simple euclidean distance between two points in n-dimensinal space
def d_euclid(a, b):
    d = 0.0     #Resulting distance
    
    d_a = len(a)    #Number of a dimensions
    d_b = len(b)    #Number of b dimensions
    
    #Swap if needed
    if(d_b > d_a):
        a, b = swap(a, b)
        d_a, d_b = swap(d_a, d_b)

    #Calculate squares of differences in each dimension, if b has less assume 0 values in these dimensions
    for i in range(d_b):
        d = d+((a[i]-b[i])*(a[i]-b[i]))
        
    for i in range(d_a-d_b):
        d = d+(a[d_b+i]*a[d_b+i])

    return sqrt(d)

#Calculates centroid of given list of points
#C is in least-dimensional space of points from list
def centroid(v):
    c = [sum(x)/len(v) for x in zip(*v)]
    return c

#^Gonna use this two function only for equally-dimensioned spaces
#And better use them only in this case

#Splits group in O(n^2), O(n^3) beacuse of not using fucking sets
#- to be optimized, but it's the first test splitting function
#It seems reasonably good, isn't as simple as heuristics or overly complex
#Will improve function and think about moving to sets to represent groups ;) 
def naive_split(group, d=d_euclid):
    groupa = group.copy()  #Old group copy
    groupb = []            #Detached group

    #Finding furthest point from centroid
    cA = centroid(groupa)    #First group centroid
    maxd = 0.0           #Max distance from centroid
    maxp = groupa[0]     #Furthest point
    for p in groupa:
        cd = d(p, cA)
        if(maxd < cd):
            maxd = cd
            maxp = p

    #Create detached group
    cB = maxp           #Detached group centroid
    groupb.append(cB)
    groupa.remove(cB)

    #Move points to new group if they are closer to it than to old one
    while len(groupa) > 1:
        cA = centroid(groupa)
        cB = centroid(groupb)

        #Find nearest to B
        mind = maxd
        minp = groupa[0]
        for p in groupa:
            cd = d(p, cB)
            if(mind > cd):
                mind = cd
                minp = p

        #Check if it's closer to B than to A
        if(mind < d(minp, cA)):
            groupb.append(minp)
            groupa.remove(minp)
        else:
            break   #Stop
    
    return groupa, groupb

#Simple Divisive Hierarchical Clustering model for tests/learning
class DHC(Model):
    def __init__(self, split=naive_split):
        self.split = naive_split    #Group splitting method

    #Recursive funciton clusters data accordingly to parameters
    #O(n*split)
    def division(self, G, level):
        if(level < self.max_depth and len(G.values) > 1):
            vL, vR = self.split(G.values)  #Split
            G.subL = Group(vL)
            G.subR = Group(vR)
            self.division(G.subL, level+1)
            self.division(G.subR, level+1)
    
    def run(self, data, max_depth):
        self.data = data                #Data
        self.max_depth = max_depth      #Maximum depth
        G = Group(self.data)
        self.division(G, 0)
        return G

    