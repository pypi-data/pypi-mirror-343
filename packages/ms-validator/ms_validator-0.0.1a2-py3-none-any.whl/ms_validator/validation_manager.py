import logging
import subprocess
from typing import List

from .validators import BaseValidator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationManager:
    def __init__(self, image_name: str, output_dir: str):
        """
        Initialize the ValidationManager with a Docker image name and output directory.
        """
        self.validators: List[BaseValidator] = []
        self.image_name = image_name
        self.output_dir = output_dir

    def add(self, validator: BaseValidator) -> None:
        """
        Add a validator to the list of validators.
        """
        if not isinstance(validator, BaseValidator):
            raise TypeError("Validator must be an instance of BaseValidator.")
        self.validators.append(validator)
        logger.info(f"Validator {validator} added.")

    def run(self) -> None:
        """
        Run all validators inside a Docker container in parallel.
        """
        if not self.validators:
            logger.error("No validators added. Ensure validators are added before running.")
            raise ValueError("No validators to execute.")

        # Generate commands
        script = "\n".join(
            f"{validator.generate_func_body()}\n{validator.get_func_name()}"
            for validator in self.validators
        )
        # script += "\nwait"  # Wait for all background processes to finish

        docker_args = [
            "docker", "run", "--rm",
            "--user", "root:root",
            "-v", f"{self.output_dir}:/host_output",
            self.image_name,
            "/bin/bash", "-c", script
        ]

        logger.info(f"Running Docker container with image: {self.image_name}")
        try:
            subprocess.run(docker_args, text=True, check=True)
            logger.info("Validation completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker command failed with error: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise
