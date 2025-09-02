import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def train_rf(X, y, n_splits=5, **rf_kwargs):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    maes, rmses = [], []
    best_model = RandomForestRegressor(n_estimators=400, random_state=42, **rf_kwargs)
    best_model.fit(X, y)  # simple fit; opcional: CV y gridsearch
    # evaluación CV rápida
    for tr, te in tscv.split(X):
        m = RandomForestRegressor(n_estimators=400, random_state=42, **rf_kwargs)
        m.fit(X[tr], y[tr])
        p = m.predict(X[te])
        maes.append(mean_absolute_error(y[te], p))
        rmses.append(mean_squared_error(y[te], p, squared=False))
    return best_model, {"MAE": np.mean(maes), "RMSE": np.mean(rmses)}

def predict(model, X_last):
    return model.predict(X_last)
