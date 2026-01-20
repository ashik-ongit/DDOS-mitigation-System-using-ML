from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np

scaler = StandardScaler()

# Simulated NORMAL traffic profile
normal = np.array([
 [3,2,0.6,0.3,0.01],
 [4,3,0.7,0.4,0.00],
 [2,1,0.8,0.5,0.02],
 [3,2,0.75,0.35,0.01],
 [4,2,0.65,0.30,0.00]
])

X = scaler.fit_transform(normal)

model = IsolationForest(
    contamination=0.15,
    n_estimators=120,
    max_samples='auto'
)

model.fit(X)


def is_attack(feature):

    f = scaler.transform([feature])
    score = model.decision_function(f)[0]

    # hybrid rule: ML + sanity
    if feature[0] > 25:        # extreme rps
        return True

    return model.predict(f)[0] == -1
