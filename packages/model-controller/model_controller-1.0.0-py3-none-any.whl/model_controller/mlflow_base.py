"""
This module handles the registration of models in MLflow.
"""

import os
import uuid

import mlflow
import mlflow.pyfunc
import pkg_resources
from loguru import logger
from mlflow.exceptions import MlflowException, RestException
from mlflow.store.artifact.artifact_repository_registry import \
    get_artifact_repository
from mlflow.tracking import MlflowClient


# List all packaged that installed
def list_installed_packages():
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(
        ["%s==%s" % (i.key, i.version) for i in installed_packages]
    )
    return installed_packages_list


# Define a simple PyFunc model
class SimpleModel(mlflow.pyfunc.PythonModel):
    def predict(self, _, model_input):
        return model_input.sum(axis=1)


class MLFlowRegistryBase:
    """
    Class to handle model registry operations
    """

    def __init__(self):
        self.client = MlflowClient()
        self.exp_id = self.setup_mlflow()

    @staticmethod
    def setup_mlflow():
        mlflow_uri = os.environ.get("MLFLOW_TRACKING_URI")
        assert mlflow_uri, "Please set MLFLOW_TRACKING_URI in environment variable."

        exp_name = os.environ.get("MLFLOW_EXPERIMENT_NAME")
        assert mlflow_uri, "Please set MLFLOW_EXPERIMENT_NAME in environment variable."

        mlflow.set_tracking_uri(mlflow_uri)
        exp = mlflow.get_experiment_by_name(name=exp_name)

        if exp:
            exp_id = exp.experiment_id
        else:
            exp_id = mlflow.create_experiment(name=exp_name)
        return exp_id

    def log_models_and_artifact(self, artifact_path, model_name):
        """
        Log the model and artifact to MLflow
        """
        # Start an MLflow run
        with mlflow.start_run(experiment_id=self.exp_id) as run:
            # Set the run name
            mlflow.set_tag("mlflow.runName", f"{model_name}-{uuid.uuid4().hex}")
            # Log the dummy models to use model registry, focusing on log artifacts only
            mlflow.pyfunc.log_model(
                artifact_path=f"dummy_model/{model_name}",
                python_model=SimpleModel(),
                pip_requirements=list_installed_packages(),
                registered_model_name=model_name,
            )

            mlflow.log_artifact(artifact_path)

        return run.info.run_id

    def get_model_version_by_run_id(self, model_name, run_id):
        """
        Get model version by run_id
        """
        # List all versions of the registered model
        model_versions = self.client.search_model_versions(f"name='{model_name}'")
        # Filter the versions to find the one with the given run_id
        for version in model_versions:
            if version.run_id == run_id:
                return version.version
        return None

    def set_registered_model_alias(self, model_name, alias, version):
        """
        Set alias for the registered model
        """
        self.client.set_registered_model_alias(model_name, alias, version)

    def get_latest_version_model_name(self, model_name):
        """
        Get the latest version of the registered model
        """
        return self.client.get_latest_versions(model_name)

    def get_all_versions_model_name(self, model_name):
        """
        Get all versions of the registered model
        """
        return self.client.search_model_versions(f"name='{model_name}'")

    def get_model_info_by_alias(self, model_name, alias):
        """
        Get model version by alias
        """
        return self.client.get_model_version_by_alias(model_name, alias)

    def get_model_info_by_version(self, model_name, version):
        """
        Get model version by alias
        """
        return self.client.get_model_version(model_name, version)

    @staticmethod
    def delete_artifact_by_uri(artifact_uri, artifact_path):
        """
        Delete the artifact from the given artifact URI.
        """
        try:
            repository = get_artifact_repository(artifact_uri=artifact_uri)
            repository.delete_artifacts(artifact_path=artifact_path)
        except RestException as e:
            logger.error(f"Failed to delete artifacts at {artifact_uri}: {e}")
        else:
            logger.info(f"Successfully deleted artifacts at {artifact_uri}")

    def delete_model_version(self, model_name, version):
        """
        Delete the model version with the given alias.
        """
        try:
            self.client.delete_model_version(name=model_name, version=version)
        except MlflowException as e:
            logger.error(
                f"Failed to delete model version {model_name}:{version} with error: {e}"
            )
        else:
            logger.info(f"Successfully deleted model version {model_name}:{version}")

    def set_model_version_tag(self, model_name, version, info: dict):
        """
        Set tag for the model version
        """
        for key, value in info.items():
            self.client.set_model_version_tag(model_name, version, key, value)
        logger.info(
            f"Set tag for model version {model_name}:{version} with info {info}"
        )
