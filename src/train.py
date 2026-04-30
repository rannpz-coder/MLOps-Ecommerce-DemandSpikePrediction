import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Ecommerce Demand Prediction")

df = pd.read_csv("data/processed/clean_week_03.csv")
df = df.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice", "StockCode"])

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate"])

df["hour"] = df["InvoiceDate"].dt.hour
df["dayofweek"] = df["InvoiceDate"].dt.dayofweek
df["total_price"] = df["Quantity"] * df["UnitPrice"]

product_demand = df.groupby("StockCode")["Quantity"].sum()
threshold = product_demand.median()

df["target"] = df["StockCode"].map(
    lambda x: 1 if product_demand[x] > threshold else 0
)

X = df[["UnitPrice", "hour", "dayofweek", "total_price"]]
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

experiments = [
    {"n_estimators": 20, "max_depth": 3},
    {"n_estimators": 60, "max_depth": 5},
    {"n_estimators": 120, "max_depth": 7},
]

for params in experiments:
    with mlflow.start_run(
        run_name=f"rf_{params['n_estimators']}_{params['max_depth']}"
    ):
        model = RandomForestClassifier(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            random_state=42
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_param("n_estimators", params["n_estimators"])
        mlflow.log_param("max_depth", params["max_depth"])
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(model, name="model")

        print(f"Run selesai: {params}")
        print(f"Accuracy: {acc:.4f}, F1 Score: {f1:.4f}")
        print("-" * 40)
