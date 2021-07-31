from abc import ABCMeta, abstractmethod

class Model(metaclass=ABCMeta):
    
    @abstractmethod
    def run(self):
        pass