import joblib
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')


class AAEMockModel:
    def __init__(self):
        self.model = None
        if os.path.exists(MODEL_PATH):
            self.load()

    def load(self):
        self.model = joblib.load(MODEL_PATH)

    def predict_confidence(self, features):
        # features: array-like
        if self.model is None:
            # default heuristic: higher amount -> lower confidence
            amt = features.get('amount', 0)
            conf = max(0.05, 1.0 - min(0.99, float(amt) / 10000.0))
            return conf
        # Build a feature vector with the same length/order the model was trained with.
        # If model exposes `n_features_in_`, use that and a deterministic ordering.
        try:
            n_in = int(self.model.n_features_in_)
        except Exception:
            n_in = None

        if n_in is None:
            X = np.array([[features.get(k, 0) for k in sorted(features.keys())]])
        else:
            # Use a stable feature ordering: prefer 'amount' first, then remaining numeric keys sorted
            keys = []
            if 'amount' in features:
                keys.append('amount')
            other_keys = [k for k in sorted(features.keys()) if k != 'amount']
            keys.extend(other_keys)
            # pad or truncate to n_in
            if len(keys) < n_in:
                # append filler keys not present
                while len(keys) < n_in:
                    keys.append('__pad_%d' % len(keys))
            keys = keys[:n_in]
            X = np.array([[features.get(k, 0) for k in keys]])
        proba = self.model.predict_proba(X)[0]
        # use max class probability as confidence
        return float(max(proba))

    @staticmethod
    def save_dummy_model():
        # train a trivial model to satisfy load() in demos
        X = [[100, 1], [5000, 0], [200, 1], [10000, 0]]
        y = [1, 0, 1, 0]
        clf = RandomForestClassifier(n_estimators=10, random_state=0)
        clf.fit(X, y)
        joblib.dump(clf, MODEL_PATH)
