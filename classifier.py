# get_ipython().magic('matplotlib inline')
from sklearn.model_selection import KFold
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
import input_parser
import features as ft
import pandas as pd

def main():

    input_data, labels = input_parser.parse_input()
    X, Y = ft.get_features(input_data, labels)

    print("X.columns:")
    print(X.columns)

    folds = 5
    print("Selecting rows for " + str(folds) + "-fold validation")
    kf = KFold(n_splits=folds)
    kf.get_n_splits(X)

    summed_accuracy = 0

    fold_cnt = 1
    for train_index, test_index in kf.split(X):

        print('Fold: ' + str(fold_cnt))
        X_train, X_test = X.loc[train_index,], X.loc[test_index,]
        Y_train, Y_test = Y[train_index], Y[test_index]
        print(X_train)
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(X_train,Y_train)
        predictions = model.predict(X_test)

        summed_accuracy += accuracy_score(Y_test, predictions)
        print(confusion_matrix(Y_test,predictions))
        print(classification_report(Y_test,predictions))
        fold_cnt += 1

    print("Total accuracy: " + str(summed_accuracy / folds))

main()
