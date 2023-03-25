import ast
import numpy as np

class LLMInterface:
    def __init__(self):
        self.design_space = ["a","v", "c","d","E","f","G","h","Z"]
        self.data_list = {}

    def initialize(self, n):
        try:
            n = int(n)
            print(f"\nStarting optimization with {n} experiments. \n")
            return np.random.choice(self.design_space, size=n, replace=False)
        except:
            return "Error. Please check your input, it should be a single number."

    def optimize_step(self, d:dict):
        parse_d = ast.literal_eval(d)
        self.data_list.update(parse_d)
        return np.random.choice(self.design_space)
