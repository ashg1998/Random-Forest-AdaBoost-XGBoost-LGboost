# -*- coding: utf-8 -*-
"""Boosting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CGtWuZyeVc44vAL22J_Eks5dJ_Dz20W4
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

df  = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Movie_classification.csv')

df['Time_taken'].fillna(value = df['Time_taken'].mean(),inplace = True)

df = pd.get_dummies(df,columns = ["3D_available","Genre"],drop_first = True)

X = df.loc[:,df.columns!="Start_Tech_Oscar"]
type(X)

y = df["Start_Tech_Oscar"]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.30,random_state=33)

from sklearn.ensemble import GradientBoostingClassifier

gbc_clf = GradientBoostingClassifier(learning_rate=0.0212,n_estimators=1000,max_depth=1)
gbc_clf.fit(X_train,y_train)

from sklearn.metrics import accuracy_score,confusion_matrix
accuracy_score(y_test,gbc_clf.predict(X_test))

l1 = np.linspace(0.01,0.1,10)

print(l1)

for x in l1:
  gbc_clf = GradientBoostingClassifier(learning_rate=x,n_estimators=1000,max_depth=1)
  gbc_clf.fit(X_train,y_train)
  print(accuracy_score(y_test,gbc_clf.predict(X_test)))

from sklearn.ensemble import AdaBoostClassifier

ada_clf = AdaBoostClassifier(learning_rate=0.02,n_estimators=5000)

ada_clf.fit(X_train,y_train)

accuracy_score(y_test,ada_clf.predict(X_test))

ada_clf = AdaBoostClassifier(learning_rate=0.02,n_estimators=500)
ada_clf.fit(X_train,y_train)
accuracy_score(y_test,ada_clf.predict(X_test))

from sklearn.ensemble import RandomForestClassifier
rlf_cls = RandomForestClassifier(n_estimators = 1000,n_jobs = -1, random_state = 42)
ada_clf = AdaBoostClassifier(rlf_cls,learning_rate=0.02,n_estimators=500)
ada_clf.fit(X_train,y_train)
accuracy_score(y_test,ada_clf.predict(X_test))

for x in l1:
  ada_clf = AdaBoostClassifier(learning_rate=x,n_estimators=500)
  ada_clf.fit(X_train,y_train)
  print(x,"=",accuracy_score(y_test,ada_clf.predict(X_test)))

for x in l1:
  ada_clf = AdaBoostClassifier(rlf_cls,learning_rate=x,n_estimators=500)
  ada_clf.fit(X_train,y_train)
  print(x,"=",accuracy_score(y_test,ada_clf.predict(X_test)))

import xgboost as xgb

xgb_clf = xgb.XGBClassifier(max_depth = 5, n_estimators = 1000,learning_rate = 0.3,
                            n_jobs = -1)

xgb_clf.fit(X_train,y_train)

accuracy_score(y_test,xgb_clf.predict(X_test))

xgb.plot_importance(xgb_clf)

for x in l1:
  xgb_clf = xgb.XGBClassifier(max_depth = 5, n_estimators = 1000,learning_rate = x,
                            n_jobs = -1)
  xgb_clf.fit(X_train,y_train)
 
  print(x,"=",accuracy_score(y_test,xgb_clf.predict(X_test)))

xgb_clf = xgb.XGBClassifier(n_estimators = 250,learning_rate = 0.1,
                            n_jobs = -1,random_state = 42)

param_test1 = {
    'max_depth':range(3,10,2),
    'gamma': [0.1,0.2,0.3],
    'subsample':[0.8,0.9],
    'colsample_bytree':[0.8,0.9],
    'reg_alpha':[1e-2,0.1,1]
}

from  sklearn.model_selection import GridSearchCV
grid_search = GridSearchCV(xgb_clf,param_test1,n_jobs = -1, cv =5 ,scoring = 'accuracy')

grid_search.fit(X_train,y_train)

cvxgb_clf = grid_search.best_estimator_

accuracy_score(y_test,cvxgb_clf.predict(X_test))

