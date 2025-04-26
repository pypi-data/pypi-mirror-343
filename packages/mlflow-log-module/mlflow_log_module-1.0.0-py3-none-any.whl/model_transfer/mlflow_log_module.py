import mlflow
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def validate_mlflow_inputs(experiment_name, params_map, metrics_map, artifact_paths):
    """
    Validates the input parameters for MLflow logging.
    Logs warnings and errors if any expected values are missing or invalid.
    """
    logging.info("Validating input parameters...")

    if not experiment_name:
        logging.error("'experiment_name' is empty.")
        return
    else:
        logging.info(f"Experiment name: {experiment_name}")

    if not isinstance(params_map, dict) or not params_map:
        logging.warning("'params_map' is empty or not a dictionary.")
    else:
        logging.info(f"Parameters to log: {list(params_map.keys())}")

    if not isinstance(metrics_map, dict) or not metrics_map:
        logging.warning("'metrics_map' is empty or not a dictionary.")
    else:
        logging.info(f"Metrics to log for epochs: {list(metrics_map.keys())}")

    if not isinstance(artifact_paths, list) or not artifact_paths:
        logging.warning("'artifact_paths' is empty or not a list.")
    else:
        logging.info(f"Artifact paths provided: {artifact_paths}")

def log_to_mlflow(
    experiment_name: str,
    params_map: dict,
    metrics_map: dict,
    artifact_paths: list
):
    """
    Logs parameters, metrics, and artifacts to an MLflow experiment.
    Automatically sets up tracking and handles errors with logging.
    """
    logging.info("Starting MLflow logging process...")

    # Generate a run name based on timestamp
    run_name = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logging.info(f"Generated run name: {run_name}")

    # Validate inputs before proceeding
    validate_mlflow_inputs(experiment_name, params_map, metrics_map, artifact_paths)

    # Get tracking URI from environment variable
    uri = os.environ.get("MLFLOW_TRACKING_URI")
    if not uri:
        logging.error("Environment variable 'MLFLOW_TRACKING_URI' is not set. Cannot proceed.")
        return
    logging.info(f"MLFLOW_TRACKING_URI: {uri}")

    try:
        # Set MLflow tracking URI and experiment
        mlflow.set_tracking_uri(uri)
        mlflow.set_experiment(experiment_name)

        # Start MLflow run
        with mlflow.start_run(run_name=run_name) as run:
            logging.info(f"MLflow run started with ID: {run.info.run_id}")

            # Log parameters
            for key, value in params_map.items():
                mlflow.log_param(key, value)

            # Log metrics
            for metric_key, metric_value in metrics_map.items():
                mlflow.log_metric(metric_key, float(metric_value))

            # Log artifacts
            for artifact_path in artifact_paths:
                if os.path.exists(artifact_path):
                    if os.path.isdir(artifact_path):
                        for root, _, files in os.walk(artifact_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                relative_path = os.path.relpath(file_path, artifact_path)
                                mlflow.log_artifact(file_path, artifact_path=os.path.dirname(relative_path))
                    else:
                        mlflow.log_artifact(artifact_path)
                else:
                    logging.warning(f"Artifact path '{artifact_path}' does not exist, skipping.")

            logging.info(f"Run logged successfully: {run.info.run_id}")

    except Exception as e:
        logging.error(f"An unexpected error occurred during MLflow logging: {e}")