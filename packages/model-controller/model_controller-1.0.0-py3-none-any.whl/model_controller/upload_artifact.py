import argparse
import os
from pathlib import Path
from typing import Optional

from model_controller.common import checksum_folder_alg
from model_controller.mlflow_base import MLFlowRegistryBase


class UploadArtifact(MLFlowRegistryBase):
    def __init__(self, artifact_path, checkpoint_ver: Optional[str] = ""):
        super().__init__()
        self.artifact_path = artifact_path
        self._validate_path(artifact_path=self.artifact_path)
        self.checkpoint_ver = checkpoint_ver

    def register(self, model_name: str) -> Optional[str]:
        """
        Registers the model artifact and sets a tag with the checksum.

        :param model_name: Name of the model to register.
        :return: Registered model version or None if an error occurs.
        """
        try:
            run_id = self.log_models_and_artifact(
                artifact_path=self.artifact_path, model_name=model_name
            )
            model_version = self.get_model_version_by_run_id(
                model_name=model_name, run_id=run_id
            )
            tags = {
                "checksum": self.checksum_artifact(artifact_path=self.artifact_path)
            }
            self.set_model_version_tag(
                model_name=model_name, version=model_version, info=tags
            )
        except Exception as e:
            print(f"Error when registering model: {e}")
            return None
        else:
            print(
                f"Model {model_name} registered successfully "
                f"with version {model_version}"
            )
            return model_version

    def checksum_artifact(self, artifact_path: str):
        """
        Computes and returns the checksum of the artifact.

        :return: The computed checksum or None if an error occurs.
        """
        try:
            file_paths = self.get_all_files_with_paths(folder_path=artifact_path)
            checksum = checksum_folder_alg(
                dir_name=Path(artifact_path), algorithm="md5", file_paths=file_paths
            )
            final_checksum = (
                f"{self.checkpoint_ver}-{checksum}" if self.checkpoint_ver else checksum
            )

            return final_checksum
        except Exception as e:
            print(f"Error when computing checksum: {e}")
            return None

    @property
    def checksum(self):
        return self.checksum_artifact(artifact_path=self.artifact_path)

    @staticmethod
    def get_all_files_with_paths(folder_path: str):
        folder = Path(folder_path)
        return [str(file) for file in folder.rglob("*") if file.is_file()]

    @staticmethod
    def _validate_path(artifact_path: str):
        """
        Validates the existence of the artifact path.

        :param artifact_path: Path to the artifact directory.
        :raises ValueError: If the path does not exist or is not a directory.
        """
        if not os.path.exists(artifact_path):
            raise ValueError(f"Artifact path does not exist: {artifact_path}")
        if not os.path.isdir(artifact_path):
            raise ValueError(f"Artifact path is not a directory: {artifact_path}")


def parse_args():
    parser = argparse.ArgumentParser("Upload artifact to MLFlow model registry")
    parser.add_argument(
        "--model-name",
        type=str,
        required=True,
        help="Name of the model to register",
    )
    parser.add_argument(
        "--artifact-path",
        type=str,
        required=True,
        help="Path to the directory containing the model artifacts",
    )
    parser.add_argument(
        "--ckpt-ver",
        type=str,
        required=True,
        help="Checkpoint version",
    )
    args = parser.parse_args()

    return args


def main(args):
    model_register = UploadArtifact(
        artifact_path=args.artifact_path, checkpoint_ver=args.ckpt_ver
    )
    model_version = model_register.register(model_name=args.model_name)
    if model_version:
        model_register.set_registered_model_alias(
            model_name=args.model_name, alias="dev", version=model_version
        )
        print(f"Model version {model_version} registered successfully with alias dev.")
    else:
        print("Failed to register model version.")


if __name__ == "__main__":
    args = parse_args()
    main(args=args)
