# -*- coding: utf-8 -*-

"""Pick n Mix is a simple stacking tool for stacking Sci-Kit learn models of your picks.
It provided 2 classes: Layer and Stack. Layer is a parallel combination of models,
while Stack combine Layers to create a stacking model"""

from copy import deepcopy
import numpy as np
import warnings

class Layer:
    def __init__(self, models, preprocessors=None, proba=False):
        """Initialize Layer, create a parallel combination of Sci-Kit learn models
        with or without preprocessors

        Parameters
        ==========
        preprocessors : a list of picks from sklearn.preprocessing,
                        if not None, the number of preprocessors and models must match.
                        If not using preprocessing for a model, None need to be put in place
        models : a list of picks from sklearn models
        proba : bool or a list of bool to show if predict_proba should be use instaed of predict,
                useful for classifiers not in the final Layer. If is a list,
                the length must match the number models.
        """
        if preprocessors is not None:
            assert len(preprocessors) == len(models), \
             "Number of preprocessors and models does not match, got {} processors but {} models.".format(len(preprocessors),len(models))

        if type(proba) != bool:
            assert len(proba) == len(models), \
             "Length of proba and number of models does not match, got {} processors but {} models.".format(len(proba),len(models))

        self.width = len(models) # number of models

        if preprocessors is None:
            self.preprocessors = [None] * self.width
        else:
            self.preprocessors = deepcopy(preprocessors)

        self.models = deepcopy(models)

        if type(proba) == bool:
            self.proba = [proba] * self.width
        else:
            self.proba = deepcopy(proba)

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

            if self.proba[idx]:
                if _method_checker(self.models[idx],'predict_proba'):
                    temp_result = self.models[idx].predict_proba(X_new)
                else:
                    warnings.warn("Warning: predict_proba not exist for {}, using predict instead".format(self.models[idx].__class__))
                    temp_result = self.models[idx].predict(X_new)
                    temp_result = np.expand_dims(temp_result, axis=1)
            else:
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

            if self.proba[idx]:
                if _method_checker(self.models[idx],'predict_proba'):
                    temp_result = self.models[idx].predict_proba(X_new)
                else:
                    warnings.warn("Warning: predict_proba not exist for {}, using predict instead".format(self.models[idx].__class__))
                    temp_result = self.models[idx].predict(X_new)
                    temp_result = np.expand_dims(temp_result, axis=1)
            else:
                temp_result = self.models[idx].predict(X_new)
                temp_result = np.expand_dims(temp_result, axis=1)

            if result is None:
                result = temp_result
            else:
                result = np.concatenate((result, temp_result), axis=1)
        return result


class Stack:
    def __init__(self, layers):
        """Initialize Stack, create a vertical stacking of Layers

        Parameters
        ==========
        layers : a list of Layers
        """
        self.depth = len(layers) # number of layers
        self.layers = deepcopy(layers)

    def fit(self, X, y):
        """Fit Layers with (X, y) and return the fitted Stack

        Parameters
        ==========
        X : array-like or sparse matrix, shape (n_samples, n_features)
            Training data
        y : array_like, shape (n_samples, n_targets)
            Target values.

        Returns
        =======
        self : obejct, the fitted Stack itself
        """
        X_new = X
        for idx in range(self.depth):
            X_new = self.layers[idx].fit(X_new, y)
        return self # follow convention of Sci-Kit learn and return self

    def predict(self, X):
        """With given X, predict the result with the Stack

        Parameters
        ==========
        X : array-like or sparse matrix, shape (n_samples, n_features)
            Samples.

        Returns
        =======
        C : array, shape (n_samples,)
            Returns predicted values from the Stack.
        """
        X_new = X
        for idx in range(self.depth):
            X_new = self.layers[idx].predict(X_new)
        # flatten result if only a number for each X
        if X_new.shape[1] == 1:
            X_new = X_new.flatten()
        return X_new # this is the final result

def _method_checker(obj,method_name):
    return method_name in dir(obj)
