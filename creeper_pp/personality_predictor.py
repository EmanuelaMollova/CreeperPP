from sklearn import svm
import numpy as np
import re
from sklearn.preprocessing import normalize
from sklearn.neighbors import KNeighborsRegressor

class PersonalityPredictor(object):
    nn = 10

    def __init__(self):
        self.o_clf = KNeighborsRegressor(n_neighbors=self.nn)
        self.c_clf = KNeighborsRegressor(n_neighbors=self.nn)
        self.e_clf = KNeighborsRegressor(n_neighbors=self.nn)
        self.a_clf = KNeighborsRegressor(n_neighbors=self.nn)
        self.n_clf = KNeighborsRegressor(n_neighbors=self.nn)
        self.features = []
        self.o_value = []
        self.c_value = []
        self.e_value = []
        self.a_value = []
        self.n_value = []

    def register(self, data):
        for user_id in data:
            if 'f' in data[user_id]:
                self.o_value.append(self.make_float(data[user_id]['o']))
                self.c_value.append(self.make_float(data[user_id]['c']))
                self.e_value.append(self.make_float(data[user_id]['e']))
                self.a_value.append(self.make_float(data[user_id]['a']))
                self.n_value.append(self.make_float(data[user_id]['n']))
                self.features.append(data[user_id]['f'])
            else:
                break

    def make_float(self, value):
        if isinstance(value, basestring):
            return float(re.sub("[^0-9.]", "", value))
        else:
            return float(value)

    def train(self):
        self.features = normalize(self.features)
        self.o_clf.fit(self.features, self.o_value)
        self.c_clf.fit(self.features, self.c_value)
        self.e_clf.fit(self.features, self.e_value)
        self.a_clf.fit(self.features, self.a_value)
        self.n_clf.fit(self.features, self.n_value)

    def predict(self, features):
        o = self.o_clf.predict([features])
        c = self.c_clf.predict([features])
        e = self.e_clf.predict([features])
        a = self.a_clf.predict([features])
        n = self.n_clf.predict([features])
        return [o, c, e, a, n]
