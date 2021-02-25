from sklearn.svm import SVC
import pandas as pd
import math

data = pd.read_csv("D:\codingan\Phyton\MachineLearn Scikit\zoo.csv")
data.head(2)

def preprocess(data):
    X = data.iloc[:, 1:17]  # all rows, all the features and no labels
    y = data.iloc[:, 17]  # all rows, label only
    return X, y

from sklearn.model_selection import train_test_split
all_X, all_y = preprocess(data)
X_train, X_test, y_train, y_test = train_test_split(all_X, all_y)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

clf = SVC(gamma='auto')
clf.fit(X_train, y_train)  
clf.score(X_test, y_test)
clf.predict(X_test[10:13])

# Show what the correct answer is
y_test[10:13]
print(y_test[10:13])