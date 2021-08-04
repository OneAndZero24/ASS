import setup
import random

from Model.divisive_clustering import Group
from Model.divisive_clustering import DHC

def parse(G, level=0):
    print(level, G.values)
    if G.subL:
        parse(G.subL, level+1)
    if G.subR:
        parse(G.subR, level+1)

data = []

#Random points on [0,1]x[0,1] plane
for i in range(10):
    data.append([round(random.uniform(0,1), 2), round(random.uniform(0,1), 2)])

print(data)

M = DHC()
G = M.run(data, 4)

parse(G)