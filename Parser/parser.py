from abc import ABC, abstractmethod

class Parser(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self, path):
        pass