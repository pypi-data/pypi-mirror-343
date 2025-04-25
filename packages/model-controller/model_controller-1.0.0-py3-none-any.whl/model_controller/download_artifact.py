import argparse
import json
import os
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List

import mlflow
from loguru import logger
from mlflow.exceptions import MlflowException, RestException

from configs.pipeline_config import internvl_model_config
from model_controller.mlflow_base import MLFlowRegistryBase


class MlflowDownloader(MLFlowRegistryBase):
    def __init__(
        self,
        models: List[str],
        max_workers=1,
    ):
        super().__init__()
        self.max_workers = max_workers

        self.artifact_path = internvl_model_config.INTERNVL_MODEL_DIR
        self.models = self.get_valid_models_to_download(
            models=models,
        )
        self._run_id_path = Path(self.artifact_path).joinpath("run_id.json")
        self._local_run_ids = self._load_run_id()

        self._lock = threading.Lock()

    def _load_run_id(self):
        if self._run_id_path.exists():
            with open(self._run_id_path, "r") as file:
                return json.load(file)
        else:
            return {}

    def _save_run_id(self, run_ids):
        with open(self._run_id_path, "w") as file:
            json.dump(run_ids, file, indent=4)

    def _download_artifact(self, model_name, run_id, artifact_path):
        try:
            logger.info(f"Downloading artifacts module: {model_name}...")

            dst_model_path = os.path.join(self.artifact_path, model_name)
            os.makedirs(dst_model_path, exist_ok=True)

            temp_path = os.path.join(self.artifact_path, "temp")
            os.makedirs(temp_path, exist_ok=True)

            # Handle temporary files and directories, auto clean up if no longer needed
            with tempfile.TemporaryDirectory(dir=temp_path) as tmp_dir:
                # Download all artifacts to the temporary directory
                mlflow.artifacts.download_artifacts(
                    run_id=run_id, artifact_path=artifact_path, dst_path=tmp_dir
                )
                # Walk through the temp directory and replace files in the destination
                for root, dirs, files in os.walk(tmp_dir):
                    # Calculate relative path from tmp_dir
                    relative_path = os.path.relpath(root, tmp_dir)
                    # Create corresponding directory in destination if it doesn't exist
                    dst_dir_path = os.path.join(self.artifact_path, relative_path)
                    os.makedirs(dst_dir_path, exist_ok=True)

                    for file_name in files:
                        src_file_path = os.path.join(root, file_name)
                        dst_file_path = os.path.join(dst_dir_path, file_name)

                        # Replace the file in the destination
                        os.replace(src_file_path, dst_file_path)
            logger.info(f"Successfully downloaded artifacts module: {model_name}!")
            return run_id

        except MlflowException as e:
            logger.error(f"Failed to download artifact module {model_name}: {e}")
            raise

    def _process_download_artifacts(self, model_name, alias):
        alias = alias.replace(".", "-")
        try:
            remote_run_id = self.get_model_info_by_alias(model_name, alias).run_id
        except RestException:
            logger.error(f"Failed to get alias module name {model_name} !!!")
            raise
        local_run_id = self._local_run_ids.get(model_name, "")
        if remote_run_id != local_run_id:
            run_id = self._download_artifact(
                model_name=model_name,
                run_id=remote_run_id,
                artifact_path=model_name,
            )
            with self._lock:
                self._local_run_ids[model_name] = run_id
                self._save_run_id(self._local_run_ids)
        else:
            logger.info(f"Model {model_name} is up-to-date, skip download.")

    def download_artifacts_multithreading(self, alias):
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(
                    self._process_download_artifacts,
                    model_name=model_name,
                    alias=alias,
                )
                for model_name in self.models
            ]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"Error downloading artifact: {e}")
                    raise
        logger.info("Completed downloading artifacts!")

    def get_valid_models_to_download(self, models: List[str]):
        try:
            registered_models = [
                model.name for model in self.client.search_registered_models()
            ]
            missing_models = list(set(models) - set(registered_models))
            if missing_models:
                logger.warning(
                    f"Models: {missing_models} is not registered ! "
                    f"Remove them from the list models."
                )
                models = list(set(models) - set(missing_models))
            else:
                logger.info("All models are registered!")
            return models
        except Exception as e:
            logger.error(f"Error checking registered models: {e}")
            raise


def load_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--models",
        type=str,
        nargs="+",
        default=None,
        help="List of models to download artifacts",
    )
    parser.add_argument("--image-version", type=str, required=True)
    return parser.parse_args()


def main(models: List[str], image_version: str):
    downloader = MlflowDownloader(
        models=models,
        max_workers=1,
    )
    start_time = time.time()
    downloader.download_artifacts_multithreading(
        alias=image_version,
    )
    logger.info(f"Total time to download artifacts: {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    args = load_args_parser()
    main(models=args.models, image_version=args.image_version)
