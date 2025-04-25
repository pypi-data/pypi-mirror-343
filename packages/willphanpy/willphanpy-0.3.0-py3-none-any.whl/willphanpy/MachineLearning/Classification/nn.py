import numpy as np

class Layer:
    def __init__(self, n_inputs, n_neurons):
        np.random.seed(42)
        self.weights = np.random.randn(n_inputs, n_neurons) # Gaussian distribution bounded around 0
        self.biases = np.zeros((1, n_neurons)) # biases

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases # z = IW + b

# Define Relu class
class Relu:
    def activate(self, x):
        self.output = np.maximum(0, x)
        self.derivative = self.grad()

    def grad(self):
        return np.diag(np.where(self.output > 0, 1, 0).flatten())

# Define Softmax class
class Softmax:
    def f(self, list):
        return np.exp(list) / np.sum(np.exp(list))

    def activate(self, list):
        self.output = self.f(list)
        self.derivative = self.grad(list)

    def grad(self, list):
        grad = [] # derivative output
        d = 0.0001 # small value for derivative calculation using numerical method

        for i in range(len(list)):
          for j in range(len(list[0])):
            list_plus = list[i].copy()
            list_plus[j] += d
            list_minus = list[i].copy()
            list_minus[j] -= d
            grad.append((self.f(list_plus) - self.f(list_minus)) / (2 * d))

        return np.array(grad)

# Define feedforward neural networks
class nn:
    '''
    Classification. Neural Networks Model
    '''
    def __init__(self, num_features, num_classes):
        self.layer1 = Layer(num_features, 4) # Define layer 1
        self.relu = Relu() # use relu activation for layer 1

        self.layer2 = Layer(4, num_classes) # Define layer 2
        self.softmax = Softmax() # use softmax activation for layer 2

        self.X = None # Training data
        self.y = None # Training label

        self.r = 0.001 # learning rate
        self.n = 100 # number of iterations

        self.lossList = [] # Loss list to hold loss value over training

    # Define loss function using Cross Entropy
    def loss(self, y_pred, y_target):
        targetPos = np.argmax(y_target)
        return np.log(y_pred.flatten()[targetPos] ** (-1)), - y_target / y_pred


    def fit(self, X, y):
        self.X = X
        self.y = y

    def createTargetClass(self, y):
        ini = [0,0,0]
        ini[y] = 1
        return np.array(ini)

    # Feed forward
    def feedforward(self, X):
        self.layer1.forward(X) # forward input to layer 1
        self.relu.activate(self.layer1.output) # activate layer 1 output using Relu activation

        self.layer2.forward(self.relu.output) # forward output from relu to layer 2
        self.softmax.activate(self.layer2.output) # activate layer 2 output using softmax activation

    def backpropagation(self):
        y_target_class = self.createTargetClass(self.y) # create target class array. If target is 0, return [1,0,0], target is 1, return [0,1,0], target is 2, return [0,0,1]
        loss, lossDerivative = self.loss(self.softmax.output, y_target_class) # calculate loss
        self.lossList.append(loss) # save loss to loss list

        # print(lossDerivative)

        dLdb2 = lossDerivative @ self.softmax.derivative # Calculate change of loss with respect to biases of layer 2
        self.layer2.biases = self.layer2.biases - self.r * dLdb2 # Update layer 2 biases
        self.layer2.weights = self.layer2.weights - self.r * self.relu.output.T @ dLdb2 # Update layer 2 weights

        dLdb1 = dLdb2 @ self.layer2.weights.T @ self.relu.derivative # Calculate change of loss with respect to biases of layer 1
        self.layer1.biases = self.layer1.biases - self.r * dLdb1 # update layer 1 biases
        self.layer1.weights = self.layer1.weights - self.r * self.X.T @ dLdb1 # update layer 1 weights

    def training(self):
        for i in range(self.n):
            self.feedforward(self.X) # perform feed forward

            self.backpropagation() # perform back propagation

    def predit(self, x_test, y_test):
        self.x_test = x_test
        self.y_test = y_test.flatten()
        self.output = []
        for i in range(len(x_test)):
            self.feedforward(x_test[i])
            target_pred = np.argmax(self.softmax.output.flatten()) # Get the index of maximum probability
            self.output.append(target_pred)
        
        return np.array(self.output).reshape(-1,1)

    def accuracy(self):
        return np.mean(self.output == self.y_test)


