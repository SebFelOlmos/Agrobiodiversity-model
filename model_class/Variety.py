import random

class Variety:
    def __init__(self):
        self.vid = round(random.uniform(0, 1),3)
    def mutation(self):
        mutation_value = round(random.uniform(-0.1, 0.1), 3)
        self.vid += mutation_value