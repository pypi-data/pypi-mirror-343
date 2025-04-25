import os
import argparse
from .validation_manager import ValidationManager
from .validators import VersionValidator, ServiceProfilerValidator


def check_output_path(path: str) -> str:
    path = os.path.realpath(path)
    if os.path.exists(path) and not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Path {path} exists and is not a directory.")
    os.makedirs(path, exist_ok=True)
    return path


def parse_args():
    parser = argparse.ArgumentParser(description="Run MindStudio Validators.")
    parser.add_argument("--image-name", "-i", required=True, help="Docker image name")
    parser.add_argument("--output-path", "-o", required=True, type=check_output_path, help="Output directory")
    return parser.parse_args()


def main():
    args = parse_args()
    manager = ValidationManager(args.image_name, args.output_path)
    manager.add(VersionValidator())
    manager.add(ServiceProfilerValidator())
    manager.run()


if __name__ == "__main__":
    main()