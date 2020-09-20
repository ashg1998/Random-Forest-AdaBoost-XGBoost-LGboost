# -*- coding: utf-8 -*-
"""Tree_classifier_Ensembling_technique

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pl-kKmyGQvxnKi5f9XQt1FCgKnKp_V09
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from sklearn.model_selection import train_test_split

df  = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Movie_classification.csv')

df['Time_taken'].fillna(value = df['Time_taken'].mean(),inplace = True)

df = pd.get_dummies(df,columns = ["3D_available","Genre"],drop_first = True)

X = df.loc[:,df.columns!="Start_Tech_Oscar"]
type(X)

y = df["Start_Tech_Oscar"]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.30,random_state=33)

from sklearn import tree
clf  = tree.DecisionTreeClassifier(max_depth = 3)
clf.fit(X_train,y_train)

y_pred = clf.predict(X_test)

from sklearn.metrics import accuracy_score,confusion_matrix

confusion_matrix(y_test,y_pred)

accuracy_score(y_test,y_pred)

"""Plotting Decision Tree"""

dot_data = tree.export_graphviz(clf, out_file = None,feature_names = X_train.columns, filled = True)

pip  install pydotplus

from IPython.display import Image
import pydotplus

graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())

"""Controlling Tree Growth"""

clftree2 = tree.DecisionTreeClassifier(min_samples_leaf= 20,max_depth = 4)
clftree2.fit(X_train,y_train)
dot_data = tree.export_graphviz(clftree2, out_file = None,feature_names = X_train.columns,filled = True)
graph2 = pydotplus.graph_from_dot_data(dot_data)
Image(graph2.create_png())

regtree3 = tree.DecisionTreeRegressor(min_samples_leaf= 25)

regtree3.fit(X_train,y_train)
dot_data = tree.export_graphviz(regtree3,out_file = None,feature_names = X_train.columns,filled =True)
graph3 = pydotplus.graph_from_dot_data(dot_data)
Image(graph3.create_png())

"""Bagging"""

from sklearn import tree
clf = tree.DecisionTreeClassifier()

from sklearn.ensemble import BaggingClassifier

bag_clf = BaggingClassifier(base_estimator = clf,n_estimators  = 1000, bootstrap = True, n_jobs = -1, random_state = 42)

bag_clf.fit(X_train,y_train)

confusion_matrix(y_test,bag_clf.predict(X_test))

accuracy_score(y_test,bag_clf.predict(X_test))

from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(n_estimators = 1000,n_jobs = -1, random_state = 42)

rf_clf.fit(X_train,y_train)

confusion_matrix(y_test,rf_clf.predict(X_test))

accuracy_score(y_test,rf_clf.predict(X_test))

from  sklearn.model_selection import GridSearchCV

rf_clf = RandomForestClassifier(n_estimators=250,random_state = 42)

import numpy as np
# Number of trees in random forest
n_estimators = [10,20,100,200]
# Number of features to consider at every split
max_features = ['auto', 'sqrt','log2']
# Maximum number of levels in tree
max_depth = [100,200,300]
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10,14]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4,6,8]
# Create the random grid
param = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
              'criterion':['entropy','gini']}

grid_search = GridSearchCV(rf_clf,param,n_jobs = -1,cv = 3, scoring = 'accuracy', verbose = 3 )

grid_search.fit(X_train,y_train)

grid_search.best_params_

print(grid_search)

cvrf_clf  = grid_search

accuracy_score(y_test,cvrf_clf.predict(X_test))

"""this is the case of overfitting"""

params_grid = {"max_features":[4,5,6,7,8,9,10],"min_samples_split":[2,3,10]}

rf_clf1 = RandomForestClassifier(n_estimators=250, random_state = 42)

grid_search = GridSearchCV(rf_clf1,params_grid,n_jobs = -1, cv =5 ,scoring = 'accuracy')

grid_search.fit(X_train,y_train)

grid_search.best_params_

cvrf_clf = grid_search.best_estimator_

accuracy_score(y_test,cvrf_clf.predict(X_test))

confusion_matrix(y_test,cvrf_clf.predict(X_test))

