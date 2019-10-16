import pytest
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.exceptions import NotFittedError
from picknmix import Layer, Stack

layer_width2_reg = Layer([LinearRegression(), LinearRegression()],
                         preprocessors = [None, MinMaxScaler()])
layer_width2_clf = Layer([LogisticRegression(solver='liblinear'),
                          LogisticRegression(solver='liblinear')],
                        proba=[True,False])
layer_width1_reg = Layer([LinearRegression()])
layer_width1_clf = Layer([LogisticRegression(solver='liblinear')])

class TestStack:

    def test_fit_predict_1_layer_reg(self):
        model = Stack([layer_width1_reg])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model.fit(X, y)
        result = model.predict(np.array([[3, 5],[3, 5]]))
        assert result.shape == (2,)
        assert np.allclose(result, np.array([16, 16]))

    def test_fit_predict_1_layer_clf(self):
        model = Stack([layer_width1_clf])
        X = np.array([[1, 1], [1, 1], [0, 0], [0, 0]])
        y = np.array([1, 1, 0, 0])
        model.fit(X, y)
        result = model.predict(np.array([[1, 1]]))
        assert result.shape == (1,)
        assert np.allclose(result, np.array([1]))

    def test_fit_predict_2_layers_reg(self):
        model = Stack([layer_width2_reg, layer_width1_reg])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model.fit(X, y)
        result = model.predict(np.array([[3, 5],[3, 5]]))
        assert result.shape == (2,)
        assert np.allclose(result, np.array([16, 16]))

    def test_fit_predict_2_layers_clf(self):
        model = Stack([layer_width2_clf, layer_width1_clf])
        X = np.array([[1, 1], [1, 1], [0, 0], [0, 0]])
        y = np.array([1, 1, 0, 0])
        model.fit(X, y)
        result = model.predict(np.array([[1, 1]]))
        assert result.shape == (1,)
        assert np.allclose(result, np.array([1]))

    def test_initialize_stack_with_sklearn_different_num_folds(self):
        with pytest.warns(Warning) as record:
            model = Stack([layer_width2_clf, layer_width1_clf],
                          folds = KFold(5))
            assert record
            assert model.splitter.n_splits == 2

    def test_initialize_stack_with_sklearn_same_num_folds(self):
        model = Stack([layer_width2_clf, layer_width1_clf],
                      folds = KFold(2))
        assert model.splitter.n_splits == 2

    def test_initialize_stack_with_custom_different_num_folds(self):
        with pytest.raises(AssertionError) as record:
            model = Stack([layer_width2_clf, layer_width1_clf],
                          folds = [[0,1,2]])
            assert record

    def test_initialize_stack_with_custom_same_num_folds(self):
        model = Stack([layer_width2_clf, layer_width1_clf],
                      folds = [[0,1,2],[3,4,5]])
        assert len(model.folds) == 2

    def test_fit_predict_stack_with_sklearn_folds(self):
        model = Stack([layer_width2_reg, layer_width1_reg],
                      folds = KFold(2))
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3],
                      [1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model.fit(X, y)
        result = model.predict(np.array([[3, 5],[3, 5]]))
        assert result.shape == (2,)
        assert np.allclose(result, np.array([16, 16]))

    def test_fit_predict_stack_with_custom_folds(self):
        model = Stack([layer_width2_reg, layer_width1_reg],
                      folds = [[0, 1, 2, 3],[4, 5, 6, 7]])
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3],
                      [1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model.fit(X, y)
        result = model.predict(np.array([[3, 5],[3, 5]]))
        assert result.shape == (2,)
        assert np.allclose(result, np.array([16, 16]))

    def test_stack_copy_function_only_model(self):
        first_layer = Layer([LinearRegression(), Ridge()])
        second_layer = Layer([LinearRegression()])
        model = Stack([first_layer, second_layer])

        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model.fit(X, y)
        model2 = model.copy()
        gotError = False
        try:
            model2.predict([1, 2])
        except(NotFittedError):
            gotError = True

        assert gotError, "Model failed the copy Test: When copying, a deep copy was produced"

    def test_stack_copy_function_model_and_preprocessor(self):
        first_layer = Layer(models=[LogisticRegression(), Ridge()], preprocessors=[MinMaxScaler(), None])
        second_layer = Layer([LinearRegression()], preprocessors=[MinMaxScaler()])
        model = Stack([first_layer, second_layer])

        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model.fit(X, y)
        model2 = model.copy()
        gotError = False
        try:
            model2.predict([1,2])
        except(NotFittedError):
            gotError = True

        assert gotError, "Model failed the copy Test: When copying, a deep copy was produced"