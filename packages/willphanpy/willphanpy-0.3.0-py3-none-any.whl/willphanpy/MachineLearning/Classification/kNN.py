import numpy as np
from collections import Counter

class kNN:
  '''
  k nearest neighbors
    @param k: k nearest neighbors
  '''
  
  def __init__(self, k=3):
    self.k = k

  def fit(self, X, y):
    '''
    @param X: training data - (instances, features)
    @param y: training label - (instances, 1)
    '''
    self._inputCheck(X, y)
    self.X_train = X
    self.y_train = y

  def _euclidean(self, x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

  def predict(self, X):
    '''
    predict method to output prediction
      @param X: test data - (instances, features)
      @return: predicted putput - (instances, 1)
    '''
    return np.array([self._predict(x) for x in X]).reshape(-1, 1)
  
  def _inputCheck(self, X, y):
    if (X.shape[0] != y.shape[0]):
      raise ValueError("X and y must have the same number of instances")

    if (y.shape[1] != 1):
      raise ValueError("y must be a column vector")

  def _predict(self, x):
    # calculate distances
    distances = [self._euclidean(x, x_train) for x_train in self.X_train]
    # get k nearest samples, labels
    k_nearest_index = np.argsort(distances)[:self.k]
    k_nearest_label = [self.y_train[i][0] for i in k_nearest_index]
    # Get most common label
    return Counter(k_nearest_label).most_common()[0][0]

  def accuracy(self, y_true, y_pred):
    '''
    Method to compute model accuracy
        @param y_pred: predicted values from the model
        @param y: target for testing
        @return: accuracy value
    '''
    return np.sum(y_true == y_pred) / len(y_true)