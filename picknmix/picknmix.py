# -*- coding: utf-8 -*-

"""Pick N Mix is a simple stacking tool for stacking Sci-Kit learn models of your picks.
It provided 2 classes: Layer and Stack. Layer is a parallel combination of models,
while Stack combine Layers to create a stacking model"""

from copy import deepcopy
import numpy as np

class Layer:
    def __init__(self, preprocessors, models):
        """Initialize Layer, create a parallel combination of Sci-Kit learn models
        with preprocessors, the number of preprocessors and models must match

        Parameters
        ==========
        preprocessors : a list of picks from sklearn.preprocessing,
                        if not using preprocessing, None need to be put in place
        models : a list of picks from sklearn models

        Returns
        =======
        None
        """

        assert len(preprocessors) == len(models), \
         f"Number of preprocessors and models does not match, got {len(preprocessors)} processors but {len(models)} models."

        self.width = len(models) #number of models
        self.preprocessors = deepcopy(preprocessors)
        self.models = deepcopy(models)

    def fit(self, X, y):
        """Fit each preprocessors and models in Layer with (X, y) and return
        predictions in an array of shape (n_samples, n_models) for the next Layer

        Parameters
        ==========
        X : array-like or sparse matrix, shape (n_samples, n_features)
            Training data
        y : array_like, shape (n_samples, n_targets)
            Target values.

        Returns
        =======
        C : array, shape (n_samples, n_models)
            Returns predicted values for the next layer.
        """
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
        """With put fiting any preprocessors and models in Layer, return predictions
        of X in an array of shape (n_samples, n_models) for the next Layer

        Parameters
        ==========
        X : array-like or sparse matrix, shape (n_samples, n_features)
            Samples

        Returns
        =======
        C : array, shape (n_samples, n_models)
            Returns predicted values for the next layer.
        """
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
