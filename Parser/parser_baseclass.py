from abc import ABCMeta, abstractmethod

class Parser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, path):
        pass