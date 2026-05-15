import os
import mlflow
from fastapi import FastAPI
import uvicorn

app = FastAPI()

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

@app.get("/")
def home():
    return {
        "message": "Inference API is running",
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI
    }

@app.get("/model-status")
def model_status():
    client = mlflow.tracking.MlflowClient()

    try:
        model = client.get_registered_model("demand_prediction_model")
        versions = client.search_model_versions("name='demand_prediction_model'")

        return {
            "status": "success",
            "connected_to_mlflow": True,
            "model_name": model.name,
            "versions": [
                {
                    "version": v.version,
                    "stage": v.current_stage,
                    "run_id": v.run_id
                }
                for v in versions
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "connected_to_mlflow": False,
            "message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)