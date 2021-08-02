import matplotlib.pyplot as plt
import setup
from Model.divisive_clustering import DHC, Group

#data = [[0.3, 0.4], [1.0, 0.2], [0.1, 0.5], [0.0, 0.9], [0.8, 0.7], [0.3, 0.2], [0.5, 0.7], [0.8, 0.6], [0.2, 0.4], [0.1, 0.3]]

#plt.scatter(*zip(*data))
#plt.show()

M = DHC()
print(M.run(data, 4))