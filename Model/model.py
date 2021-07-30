class Model:
    def __init__(self, data, chain):
        self.data = data
        self.chain = chain
    def run(self):
        for i in chain:
            data = i.run(self.data)