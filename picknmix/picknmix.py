# -*- coding: utf-8 -*-

"""Main module."""

from copy import deepcopy
import numpy as np

class Layer:
    def __init__(self, preprocessors, models):

        assert len(preprocessors) == len(models), \
         f"Number of preprocessors and models does not match, got {len(preprocessors)} processors but {len(models)} models."

        self.width = len(models)
        self.preprocessors = deepcopy(preprocessors)
        self.models = deepcopy(models)

    def fit(self, X, y):
        result = None
        for idx in range(self.width):
            if self.preprocessors[idx] is not None:
                X_new = self.preprocessors[idx].fit_transform(X)
            else:
                X_new = X
            self.models[idx].fit(X_new,y)
            temp_result = self.models[idx].predict(X_new)
            temp_result = np.expand_dims(temp_result, axis=1)
            if result is None:
                result = temp_result
            else:
                result = np.concatenate((result, temp_result), axis=1)
        return result

    def predict(self, X):
        result = None
        for idx in range(self.width):
            if self.preprocessors[idx] is not None:
                X_new = self.preprocessors[idx].transform(X)
            else:
                X_new = X
            temp_result = self.models[idx].predict(X_new)
            temp_result = np.expand_dims(temp_result, axis=1)
            if result is None:
                result = temp_result
            else:
                result = np.concatenate((result, temp_result), axis=1)
        return result
