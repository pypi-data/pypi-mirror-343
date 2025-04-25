import os
from textwrap import dedent

from .base_validator import BaseValidator
from ..utils import msg_wrapper


class VersionValidator(BaseValidator):
    COMMON_PATH = "/usr/local/Ascend"
    VERSION_FILE = "version.info"

    def get_func_name(self):
        return "version_validator"

    def generate_func_body(self):
        """
        Generates a shell function that validates the existence of version files
        and prints their content if found.
        """
        TOOLKIT_PATH = os.path.join(self.COMMON_PATH, "ascend-toolkit", "latest", "compiler", self.VERSION_FILE)
        ATB_PATH = os.path.join(self.COMMON_PATH, "nnal", "atb", "latest", self.VERSION_FILE)
        MODELS_PATH = os.path.join(self.COMMON_PATH, "atb-models", self.VERSION_FILE)

        path_mapping = [
            ("toolkit_version", TOOLKIT_PATH),
            ("atb_version", ATB_PATH),
            ("mindie_version", TOOLKIT_PATH),
            ("atb_models_version", MODELS_PATH),
        ]

        cmd = dedent("""\
        function version_validator() {
        """)
        for key, path in path_mapping:
            cmd += dedent(f"""\
                if [ ! -f {path} ]; then
                    echo "ERROR - {path} not found" >&2
                else
                    echo {msg_wrapper(key)}
                    cat {path}
                fi
            """)

        cmd += "\n}"
        return cmd