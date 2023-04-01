import random

class RandomNumber:
    @classmethod
    def generate(cls):
        return random.randint(1, 1000)
