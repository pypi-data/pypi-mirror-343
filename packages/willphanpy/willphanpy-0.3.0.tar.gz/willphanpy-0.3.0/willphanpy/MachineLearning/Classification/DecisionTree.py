import numpy as np

class Node:
  def __init__(self, feature_idx = None, threshold = None, info_gain = None, left = None, right = None, value = None, depth = 0): # depth = 0 -> root node
    self.feature_idx = feature_idx
    self.threshold = threshold
    self.info_gain = info_gain
    self.left = left
    self.right = right
    self.value = value
    self.depth = depth

class Decision_Tree:
  '''
  Classification. Decision Tree Model
      @param max_depth: maximum depth the tree can go down
      @param min-sample: minimum number of samples in a table that the tree can be made from
      @method fit
      @method predit
      @method print_tree
      @method accuracy
  '''
  def __init__(self, max_depth = 10, min_sample = 1):
    self.root = None
    self.max_depth = max_depth
    self.min_samples = min_sample

  def _build_tree(self, data, depth = 0):
    X, y = data[:, :-1], data[:, -1]
    num_samples, num_features = X.shape

    if depth >= self.max_depth and num_samples <= self.min_samples:
      return Node(value = self._most_common_label(y), depth=depth)

    best_split = self._best_split(data)

    if best_split['info_gain'] <= 0:
      return Node(value = self._most_common_label(y), depth=depth)

    left_subtree = self._build_tree(best_split['left_data'], depth + 1)
    right_subtree = self._build_tree(best_split['right_data'], depth + 1)

    return Node(feature_idx = best_split['feature_idx'], threshold = best_split['threshold'], info_gain = best_split['info_gain'], left = left_subtree, right = right_subtree, depth = depth)

  def _best_split(self, data):
    best_split_result = {}
    best_split_result['info_gain'] = -float('inf')

    X, y = data[:, :-1], data[:, -1]
    num_samples, num_features = X.shape

    for feature_idx in range(num_features):
      thresholds = np.unique(X[:, feature_idx])
      for threshold in thresholds:
        y_left = y[X[:, feature_idx] <= threshold]
        y_right = y[X[:, feature_idx] > threshold]
        y = data[:, -1]

        info_gain = self._compute_info_gain(y, y_left, y_right)

        if info_gain > best_split_result['info_gain']:
          best_split_result['info_gain'] = info_gain
          best_split_result['feature_idx'] = feature_idx
          best_split_result['threshold'] = threshold
          best_split_result['left_data'] = data[X[:, feature_idx] <= threshold]
          best_split_result['right_data'] = data[X[:, feature_idx] > threshold]

    return best_split_result

  def _compute_info_gain(self, y, y_left, y_right, method = 'entropy'):
    w_left = len(y_left) / len(y)
    w_right = len(y_right) / len(y)

    def entropy(y):
      entropy = 0
      labels = np.unique(y)
      for label in labels:
        p = len(y[y == label]) / len(y)
        entropy += - p * np.log2(p)

      return entropy

    def gini_index(y):
      gini = 0
      labels = np.unique(y)
      for label in labels:
        p = len(y[y == label]) / len(y)
        gini += p ** 2

      return 1 - gini

    if (method == 'entropy'):
      return entropy(y) - w_left * entropy(y_left) - w_right * entropy(y_right)

    if (method == 'gini'):
      return gini_index(y) - w_left * gini_index(y_left) - w_right * gini_index(y_right)

  def _most_common_label(self, y):
    labels, counts = np.unique(y, return_counts = True)
    return labels[np.argmax(counts)]

  def fit(self, X, y):
    '''
    This method is to fit the data into the tree instance and automatically build the tree from there
      @param X: training data - (instances, features)
      @param y: target data - (instances, 1)
    '''
    self._inputCheck(X, y)
    self.root = self._build_tree(np.concatenate((X, y), axis = 1))

  def _inputCheck(self, X, y):
    if (X.shape[0] != y.shape[0]):
      raise ValueError("X and y must have the same number of samples")
    if (y.shape[1] != 1):
      raise ValueError("y must be a column vector")

  def predict(self, X):
    '''
    Method to predic result
      @param X: testing data - (instances, features)
      @return: numpy array of results (instances, 1)
    '''
    def helper(node, x):
      if node is not None:
        if node.feature_idx is not None:
          if x[node.feature_idx] <= node.threshold:
            return helper(node.left, x)
          return helper(node.right, x)

        return node.value

    return np.array([helper(self.root, x) for x in X]).reshape(-1, 1)

  def accuracy(self, y_pred, y):
    '''
    Method to compute model accuracy
      @param y_pred: predicted results (instances, 1)
      @param y: target for testing (instances, 1)
    '''
    return np.sum(y_pred == y) / len(y)

  def print_tree(self, feature_names):
    '''
    Method to visualize the decision tree
      @param feature_names: list of feature names
    '''
    def helper(node, depth, prefix="Root: "):
      if node is not None:
        space = " " * (4 * depth)
        if node.feature_idx is not None:
          print(f"{space} {prefix} Depth: {node.depth}, Feature: {feature_names[node.feature_idx]}, Threshold: {node.threshold}, Info Gain: {node.info_gain}")
        else:
          print(f"{space} {prefix} Value: {node.value}")
        helper(node.left, depth + 1, "L--- ")
        helper(node.right, depth + 1, "R--- ")

    helper(self.root, 0)