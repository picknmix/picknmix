# -*- coding: utf-8 -*-

"""Pick N Mix is a simple stacking tool for stacking Sci-Kit learn models of your picks.
It provided 2 classes: Layer and Stack. Layer is a parallel combination of models,
while Stack combine Layers to create a stacking model"""

from copy import deepcopy
import numpy as np

class Layer:
    def __init__(self, models, preprocessors=None, proba=False):
        """Initialize Layer, create a parallel combination of Sci-Kit learn models
        with preprocessors,

        Parameters
        ==========
        preprocessors : a list of picks from sklearn.preprocessing,
                        if not None, the number of preprocessors and models must match.
                        If not using preprocessing for a model, None need to be put in place
        models : a list of picks from sklearn models
        proba : bool or a list of bool to show if predict_proba should be use instaed of predict,
                useful for classifiers not in the final Layer. If is a list,
                the length must match the number models.

        Returns
        =======
        None
        """
        if preprocessors is not None:
            assert len(preprocessors) == len(models), \
             f"Number of preprocessors and models does not match, got {len(preprocessors)} processors but {len(models)} models."

        if type(proba) != bool:
            assert len(proba) == len(models), \
             f"Length of proba and number of models does not match, got {len(proba)} processors but {len(models)} models."

        self.width = len(models) #number of models

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
                temp_result = self.models[idx].predict_proba(X_new)
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
                temp_result = self.models[idx].predict_proba(X_new)
            else:
                temp_result = self.models[idx].predict(X_new)
                temp_result = np.expand_dims(temp_result, axis=1)

            if result is None:
                result = temp_result
            else:
                result = np.concatenate((result, temp_result), axis=1)
        return result
