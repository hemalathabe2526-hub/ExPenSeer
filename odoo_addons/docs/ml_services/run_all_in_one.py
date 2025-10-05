"""Single-file AAE demo: trains a dummy model, predicts confidence, and prints suggested chain.

This script is self-contained and avoids running a FastAPI server. It demonstrates the
AAE logic and can be executed directly with `python run_all_in_one.py`.
"""
import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')


class AAEMockModel:
    def __init__(self):
        self.model = None
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception:
                self.model = None

    def save_dummy_model(self):
        X = [[100, 1], [5000, 0], [200, 1], [10000, 0]]
        y = [1, 0, 1, 0]
        clf = RandomForestClassifier(n_estimators=10, random_state=0)
        clf.fit(X, y)
        joblib.dump(clf, MODEL_PATH)
        self.model = clf

    def predict_confidence(self, features):
        # If no trained model is present, use a simple heuristic
        if self.model is None:
            amt = features.get('amount', 0)
            return max(0.05, 1.0 - min(0.99, float(amt) / 10000.0))

        # Build a feature vector compatible with the trained model
        try:
            n_in = int(self.model.n_features_in_)
        except Exception:
            n_in = None

        if n_in is None:
            X = np.array([[features.get(k, 0) for k in sorted(features.keys())]])
        else:
            keys = []
            if 'amount' in features:
                keys.append('amount')
            other_keys = [k for k in sorted(features.keys()) if k != 'amount']
            keys.extend(other_keys)
            if len(keys) < n_in:
                while len(keys) < n_in:
                    keys.append('__pad_%d' % len(keys))
            keys = keys[:n_in]
            X = np.array([[features.get(k, 0) for k in keys]])

        proba = self.model.predict_proba(X)[0]
        return float(max(proba))


def suggest_chain_logic(amount):
    if amount < 1000:
        return ['manager', 'finance']
    return ['manager', 'director', 'finance']


def main():
    print('AAE single-file demo starting...')
    model = AAEMockModel()
    if model.model is None:
        print('No model found — training dummy model...')
        model.save_dummy_model()
        print('Model trained and saved to', MODEL_PATH)

    # Sample claims to demo different behaviors
    samples = [
        {'claim_id': 1, 'employee_id': 10, 'amount': 50.0, 'currency': 'USD', 'category': 'meal', 'merchant': 'Cafe'},
        {'claim_id': 2, 'employee_id': 11, 'amount': 2500.0, 'currency': 'USD', 'category': 'travel', 'merchant': 'AirCo'},
    ]

    for s in samples:
        amt = float(s.get('amount', 0))
        features = {'amount': amt}
        conf = model.predict_confidence(features)
        chain = suggest_chain_logic(amt)
        print('\nClaim', s['claim_id'])
        print('  Amount:', amt)
        print('  Suggested chain:', chain)
        print('  Confidence:', conf)
        if conf >= 0.85:
            print('  -> Auto-approve (confidence >= 0.85)')
        else:
            print('  -> No auto-approve (below threshold)')


if __name__ == '__main__':
    main()
