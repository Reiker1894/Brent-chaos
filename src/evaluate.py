from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mape = (abs((y_true - y_pred) / (y_true+1e-12))).mean()*100
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}
