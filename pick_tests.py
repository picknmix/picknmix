from picknmix import Layer, Stack

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn.model_selection import StratifiedKFold


if __name__ == "__main__":
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
