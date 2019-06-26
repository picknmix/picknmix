=====
Usage
=====

Use Pick n Mix to create a regression model::

    from picknmix import Layer, Stack

    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Ridge

    first_layer = Layer([LinearRegression(), Ridge()])
    second_layer = Layer([LinearRegression()])
    model = Stack([first_layer, second_layer])

    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.dot(X, np.array([1, 2])) + 3
    model.fit(X, y)
    model.predict(np.array([[3, 5]]))

You can also use preprocessing in a Layer::

    from sklearn.linear_model import MinMaxScaler

    first_layer = Layer([LinearRegression(), Ridge()],
                        preprocessors = [MinMaxScaler(), None])

Classification task can also be done::

    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier

    first_layer = Layer([LogisticRegression(solver='liblinear'),
                         RandomForestClassifier()],
                         proba=True)
    second_layer = Layer([LogisticRegression(solver='liblinear')])
    model = Stack([first_layer, second_layer])

    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.array([1, 1, 0, 0])
    model.fit(X, y)
    model.predict(np.array([[1, 3]]))

You can also make use of cross-validation with one of the different scikit-learn options (e.g. Stratified K-Fold)::
    from sklearn import datasets
    from sklearn.model_selection import StratifiedKFold

    digits = datasets.load_digits()
    features = digits.images
    features = features.reshape(features.shape[0],
                                features.shape[1]*features.shape[2])
    targets = digits.target
    skf = StratifiedKFold(n_splits=2)
    skf.get_n_splits(features, targets)

    first_layer = Layer([LogisticRegression(solver='liblinear'),
                         RandomForestClassifier()],
                         proba=True)
    second_layer = Layer([LogisticRegression(solver='liblinear')])
    model = Stack([first_layer, second_layer], folds=skf)

    model.fit(features, targets)
