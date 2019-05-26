import pytest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from picknmix.picknmix import Layer

class TestLayer(object):
    def test_different_numbers_of_preprocessor_and_models(self):
        with pytest.raises(Exception):
            assert Layer([None],[LinearRegression(), LinearRegression()])

    def test_single_model_fit_without_preprocess(self):
        layer_model = Layer([None],[LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        result = layer_model.fit(X, y)
        assert result.shape == (4,1)
        assert np.allclose(result.flatten(), y)

    def test_single_model_fit_with_preprocess(self):
        layer_model = Layer([MinMaxScaler()],[LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        result = layer_model.fit(X, y)
        assert result.shape == (4,1)
        assert np.allclose(result.flatten(), y)

    def test_multiple_model_fit(self):
        layer_model = Layer([None, MinMaxScaler()],
                            [LinearRegression(), LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        result = layer_model.fit(X, y)
        assert result.shape == (4,2)
        assert np.allclose(result[:,0], y)
        assert np.allclose(result[:,1], y)

    def test_single_model_predict_without_preprocess(self):
        layer_model = Layer([None],[LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5],[3, 5]]))
        assert result.shape == (2,1)
        assert np.allclose(result, np.array([[16],[16]]))

    def test_single_model_predict_with_preprocess(self):
        layer_model = Layer([MinMaxScaler()],[LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5]]))
        assert result.shape == (1,1)
        assert np.allclose(result, np.array([[16]]))

    def test_multiple_model_predict(self):
        layer_model = Layer([None, MinMaxScaler()],
                            [LinearRegression(), LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5]]))
        assert result.shape == (1,2)
        assert np.allclose(result, np.array([[16, 16]]))
