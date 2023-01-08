from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

class Model(object):

    def __init__(self):
        pass

    def fit(self, x, y):
        self.scaler = StandardScaler()
        self.lr = LogisticRegression()
        x = self.scaler.fit_transform(x)
        self.lr.fit(x, y)

    def predict(self, x):
        x = self.scaler.transform(x)
        return self.lr.predict(x)

    def predict_proba(self, x):
        x = self.scaler.transform(x)
        return self.lr.predict_proba(x)