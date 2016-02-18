from sklearn import svm
import numpy as np

class PersonalityPredictor(object):
    def __init__(self):
        self.o_clf = svm.SVR()
        self.c_clf = svm.SVR()
        self.e_clf = svm.SVR()
        self.a_clf = svm.SVR()
        self.n_clf = svm.SVR()
        self.features = []
        self.o_value = []
        self.c_value = []
        self.e_value = []
        self.a_value = []
        self.n_value = []

    def register(self, data):
        for user_id in data:
            self.o_value.push(data[user_id]['o'])
            self.c_value.push(data[user_id]['c'])
            self.e_value.push(data[user_id]['e'])
            self.a_value.push(data[user_id]['a'])
            self.n_value.push(data[user_id]['n'])
            self.features.push(data[user_id]['f'])

    def train(self):
        features = np.array(self.features)
        o_value = np.array(self.o_value)
        c_value = np.array(self.c_value)
        e_value = np.array(self.e_value)
        a_value = np.array(self.a_value)
        n_value = np.array(self.n_value)
        self.o_clf.fit(features, o_value)
        self.c_clf.fit(features, c_value)
        self.e_clf.fit(features, e_value)
        self.a_clf.fit(features, a_value)
        self.n_clf.fit(features, n_value)

    def predict(self, features):
        features_np = np.array(features)
        o = self.o_clf.predict(features_np)
        c = self.c_clf.predict(features_np)
        e = self.e_clf.predict(features_np)
        a = self.a_clf.predict(features_np)
        n = self.n_clf.predict(features_np)
        return [o, c, e, a, n]
