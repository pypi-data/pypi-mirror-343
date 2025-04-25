import numpy as np

class Time_Series():
  '''
  Time series model
    @param window_size: size of the sliding window
    @param method: model to use
  '''
  def __init__(self, window_size, method):
    self._window_size = window_size
    self._method = method()

  def _inputCheck(self, X, y):
    '''
    Validate input data
      @param X: training data
      @param y: training label
    '''
    if (X.shape[0] != y.shape[0]):
      raise ValueError("X and y must have the same number of instances")

    if (y.shape[1] != 1):
      raise ValueError("y must be a column vector")

  def sliding_window(self, X):
    '''
    This method is to extract training data and training label from the original dataset using sliding window technique
      @param X: original dataset
      @return: training data and training label
    '''
    X_train = []
    y_train = []
    for i in range(len(X) - self._window_size):
      X_train.append(X[i:i+self._window_size])
      y_train.append(X[i+self._window_size])
    return np.array(X_train), np.array(y_train)


  def fit(self, X, y):
    '''
    Fit method to train the model
      @param X: training data
      @param y: training label
    '''
    self._inputCheck(X, y)
    self._method.fit(X, y)

  def predict(self, X, k):
    '''
    Predict or forecast the next k days
      @param X: training data
      @param d: number of days to predict
      @return: predicted output
    '''
    predictions = [] # predicted output

    start = X[-1].tolist() # start at the last sample

    # Use for loop to predict the next k days
    for i in range(k):
      predict = self._method.predict(np.array(start).reshape(1,-1))
      predictions.append(predict.item())

      start.pop(0) # remove the first value
      start.append(predict.item()) # add the predicted value to the end

    return np.array(predictions).reshape(-1, 1)