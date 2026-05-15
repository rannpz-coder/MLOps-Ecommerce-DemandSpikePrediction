import mlflow.pyfunc
import pandas as pd

# Load model dari Production
model = mlflow.pyfunc.load_model(
    "models:/demand_prediction_model/Production"
)

# Dummy input
data = pd.DataFrame([{
    "UnitPrice": 10.0,
    "hour": 12,
    "dayofweek": 2,
    "total_price": 100.0
}])

pred = model.predict(data)

print("Prediction:", pred)