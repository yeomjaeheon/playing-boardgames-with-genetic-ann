import numpy as np

def crossover(parent1, parent2):
    child = ann(parent1.structure)
    for i in range(0, len(parent1.structure) - 1):
        if np.random.randint(2) == 0:
            child.weights[i] = parent1.weights[i].copy()
        else:
            child.weights[i] = parent2.weights[i].copy()
    return child

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
        input_data = np.array(input_data) + bias
        for w in self.weights[:-1]:
            input_data = ann.sigmoid(np.dot(input_data, w))
        return np.dot(input_data, self.weights[-1])

    def mut(self, mut_rate = 0.03, mut_scale = 0.03):
        for i in range(0, len(self.weights)):
            if np.random.random() <= mut_rate:
                self.weights[i] += np.random.normal(loc = 0.0, scale = mut_scale, size = (self.structure[i], self.structure[i + 1]))