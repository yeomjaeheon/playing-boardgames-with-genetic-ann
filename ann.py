import numpy as np

def crossover(a, b):
    pass

class ann:
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def softmax_simp(x):
        exp_x = np.exp(x)
        return exp_x

    def __init__(self, structure):
        self.structure = structure
        self.weights = []
        for i in range(0, len(self.structure) - 1):
            self.weights.append(np.random.normal(loc = 0.0, scale = (4 / (self.structure[i] + self.structure[i + 1])) ** 0.5, size = (self.structure[i], self.structure[i + 1])))
    
    def prop(self, input_data, bias = 0.1):
        input_data += bias
        for w in self.weights[:-1]:
            input_data = ann.sigmoid(np.dot(input_data, w))
        return ann.softmax_simp(np.dot(input_data, self.weights[-1]))

    def mut(self):
        pass