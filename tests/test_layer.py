import pytest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from picknmix import Layer

class TestLayer(object):
    def test_different_numbers_of_preprocessor_and_models(self):
        with pytest.raises(Exception):
            assert Layer([LinearRegression(), LinearRegression()],
                         [MinMaxScaler()])

    def test_fit_single_model_without_preprocess(self):
        layer_model = Layer([LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        # X and y are linearly related, predictions will be almost perfect
        result = layer_model.fit(X, y)
        assert result.shape == (4,1)
        assert np.allclose(result.flatten(), y)

    def test_fir_single_model_with_preprocess(self):
        layer_model = Layer([LinearRegression()],
                            [MinMaxScaler()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        # X and y are linearly related, predictions will be almost perfect
        result = layer_model.fit(X, y)
        assert result.shape == (4,1)
        assert np.allclose(result.flatten(), y)

    def test_fit_single_model_with_2_class_proba(self):
        layer_model = Layer([LogisticRegression(solver='liblinear')],
                            proba=True)
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([1, 1, 0, 0])
        result = layer_model.fit(X, y)
        assert result.shape == (4,2)

    def test_fit_single_model_with_multi_class_proba(self):
        layer_model = Layer([LogisticRegression(solver='lbfgs',
                                                multi_class='multinomial')],
                            proba=True)
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([1, 1, 0, 2])

        result = layer_model.fit(X, y)
        assert result.shape == (4,3)

    def test_fit_multiple_models(self):
        layer_model = Layer([LinearRegression(), LinearRegression()],
                            [None, MinMaxScaler()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        # X and y are linearly related, predictions will be almost perfect
        result = layer_model.fit(X, y)
        assert result.shape == (4,2)
        assert np.allclose(result[:,0], y)
        assert np.allclose(result[:,1], y)

    def test_fit_multiple_model_with_2_class_proba(self):
        layer_model = Layer([LogisticRegression(solver='liblinear'),
                             LogisticRegression(solver='liblinear')],
                            proba=[True,False])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([1, 1, 0, 0])
        result = layer_model.fit(X, y)
        assert result.shape == (4,3)

    def test_predict_single_model_without_preprocess(self):
        layer_model = Layer([LinearRegression()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5],[3, 5]]))
        assert result.shape == (2,1)
        assert np.allclose(result, np.array([[16],[16]]))

    def test_predict_single_model_with_preprocess(self):
        layer_model = Layer([LinearRegression()],
                            [MinMaxScaler()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5]]))
        assert result.shape == (1,1)
        assert np.allclose(result, np.array([[16]]))

    def test_predict_single_model_with_2_class_proba(self):
        layer_model = Layer([LogisticRegression(solver='liblinear')],
                            proba=True)
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([1, 1, 0, 0])

        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5]]))
        assert result.shape == (1,2)

    def test_predict_single_model_with_multi_class_proba(self):
        layer_model = Layer([LogisticRegression(solver='lbfgs',
                                                multi_class='multinomial')],
                            proba=True)
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([1, 1, 0, 2])
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5]]))
        assert result.shape == (1,3)

    def test_predict_multiple_model(self):
        layer_model = Layer([LinearRegression(), LinearRegression()],
                            [None, MinMaxScaler()])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5]]))
        assert result.shape == (1,2)
        assert np.allclose(result, np.array([[16, 16]]))

    def test_predict_multiple_model_with_2_class_proba(self):
        layer_model = Layer([LogisticRegression(solver='liblinear'),
                             LogisticRegression(solver='liblinear')],
                            proba=[True,False])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([1, 1, 0, 0])
        layer_model.fit(X, y)
        result = layer_model.predict(np.array([[3, 5], [2, 5]]))
        assert result.shape == (2,3)

    def test_using_proba_without_predict_proba_method(self):
        with pytest.warns(Warning) as record:
            layer_model = Layer([LinearRegression()],
                                proba=True)
            X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
            y = np.dot(X, np.array([1, 2])) + 3
            layer_model.fit(X, y)
            result = layer_model.predict(np.array([[3, 5],[3, 5]]))
            assert result.shape == (2,1)
            assert np.allclose(result, np.array([[16],[16]]))
            assert record
