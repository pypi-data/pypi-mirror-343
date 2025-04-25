import numpy as np
from willphanpy.MachineLearning.Regression.LinearRegression import Linear_Regression
from ..ActivationFunction.Sigmoid import Sigmoid

class Logistic_Regression(Linear_Regression):
    def __init__(self, function = Sigmoid, threshold = 0.5, method = 'normal', epochs = 1000, lr = 0.001):
        super().__init__(method, iterations=epochs, learning_rate=lr)
        self._function = function
        self._threshold = threshold
    
    def predict(self, X):
        '''
        predict method to predict the output of the model based on selected activation function
        @param X: data to predict - (instances, features)
        @return: predicted output - (instances, 1)
        '''
        y_pred = super().predict(X)
        activated = self._function.activate(y_pred)
        return np.array([1 if x > self._threshold else 0 for x in activated]).reshape(-1 ,1)
    
    def accuracy(self, y_pred, y):
        '''
        Method to compute model accuracy
            @param y_pred: predicted values from the model
            @param y: target for testing
            @return: accuracy value
        '''
        return np.sum(y == y_pred) / len(y)


