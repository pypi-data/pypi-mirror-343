import numpy as np

class Linear_Regression:
  def __init__(self, method = 'normal', iterations = 1000, learning_rate = 0.001):
    '''
    Linear Regression model
        @param method: 'normal' for normal equation, 'gradient' for gradient descent
        @param iterations: number of iterations for gradient descent
        @param learning_rate: learning rate for gradient descent
    '''
    
    self.__X = None # training data
    self.__y = None # training label
    self.__w = None # weight vector -> the output of the model
    self.__learning_rate = learning_rate # learning rate
    self.__iterations = iterations # number of iterations
    self.__method = method # method to use

  def cost(self):
    '''
    Use mean square error as cost function
      @return: mean square cost
    '''
    m = np.size(self.__y)
    error = (self.__X @ self.__w - self.__y)**2
    return (1/(m))*np.sum((error))
  
  def _normalize(self, X):
    '''
    Method to normalize the data so it prevents overflow
      @param X: training data
      @return: normalized version of data
    '''
    return ( X - X.mean(axis = 0) ) / X.std(axis = 0)

  def fit(self, X, y):
    '''
    fit method to train the model
      @param X: training data - (instances, features)
      @param y: training label - (instances, 1)
    '''
    self.__X = self._normalize(X)
    self.__y = y
    if self.__method == 'normal':
      self.__w = np.linalg.inv(X.T @ X) @ X.T @ y # proven by using derivatives
      print("Model cost using normal equation: " + str(self.cost()))
      return

    if self.__method == 'gradient':
      rows, cols = self.__X.shape
      self.__w = np.full((cols,1), 0, dtype="float") # initialize an array 9x1 filled with 0 for all 9 weights

      prev_mse = self.cost() # previous mean square error
      for i in range(self.__iterations):
          self.__w = self.__w - self.__learning_rate * (1 / rows) * self.__X.T @ (self.__X @ self.__w - self.__y)

          cur_mse = self.cost() # current mean square error

          # define a condition where if the gap between mean square errors is less than a certain amount, then break the loop
          if(abs(cur_mse - prev_mse) <= 10e-10):
              break

          prev_mse = cur_mse # set current mean square error to the previous mean square error
      print("Model cost using gradient descent: " + str(self.cost()))

      return

  def predict(self, X):
    '''
    predict method to predict the output of the model
      @param X: data to predict - (instances, features)
      @return: predicted output - (instances, 1)
    '''
    return X @ self.__w