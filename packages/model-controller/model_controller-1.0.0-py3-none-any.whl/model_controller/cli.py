import sys
import click

from .upload_artifact import UploadArtifact


@click.group()
def cli():
    """Vumit - AI-powered Git analysis tool"""
    pass

@cli.command()
@click.option(
    "--model-name",
    required=True,
    help="Name of the model to register",
)
@click.option(
    "--artifact-path",
    required=True,
    help="Path to the directory containing the model artifacts",
)
@click.option(
    "--ckpt-ver",
    default="",
    help="Checkpoint version (optional)",
)
@click.option(
    "--alias",
    default="dev",
    help="Checkpoint version (optional)",
)

def upload(model_name, artifact_path, ckpt_ver, alias="dev"):
    """Upload artifact to MLFlow model registry.

    This command uploads model artifacts to MLflow and registers the model
    with a checksum tag.
    """
    click.echo(f"Uploading artifact from {artifact_path} to MLflow registry...")
    try:
        # Initialize uploader
        model_register = UploadArtifact(
            artifact_path=artifact_path, checkpoint_ver=ckpt_ver
        )

        # Register model
        model_version = model_register.register(model_name=model_name)

        # Set alias if registration was successful
        if model_version:
            model_register.set_registered_model_alias(
                model_name=model_name, alias=alias, version=model_version
            )
            click.secho(
                f"✅ Model version {model_version} registered successfully with alias {alias}.",
                fg="green"
            )
        else:
            click.secho("❌ Failed to register model version.", fg="red")
            sys.exit(1)

    except ValueError as e:
        click.secho(f"❌ Error: {str(e)}", fg="red")
        sys.exit(1)
    except Exception as e:
        click.secho(f"❌ Unexpected error: {str(e)}", fg="red")
        sys.exit(1)


def main():
    cli()

if __name__ == "__main__":
    main()