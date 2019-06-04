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
    second_layer = Layer([LogisticRegression(solver='liblinear'])
    model = Stack([first_layer, second_layer])

    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
    y = np.array([1, 1, 0, 0])
    model.fit(X, y)
    model.predict(np.array([[1, 3]]))
