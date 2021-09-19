from enum import Enum
import os
from pathlib import Path


class EnvironmentVariables(Enum):
    """
    Defines important environment variables for Flask configuration.
    Use this check if variables are defined, or set the undefined ones to default values.
    """
    APP_CONFIG_FILE = "config/development.py"
    TEST_CONFIG_FILE = "config/test.py"
    LOG_CONFIG_FILE = "config/logging.yaml"

    def get(self) -> str:
        """
        Returns env variable value
        """
        return os.environ[self.name]

    @staticmethod
    def set_undefined_to_default() -> None:
        """
        Sets the undefined env variables to their configured default values
        """
        for env_var in EnvironmentVariables:
            try:
                os.environ[env_var.name]
            except KeyError:
                print(f"Environment variable {env_var.name} is undefined. "
                      f"Setting it to default value: {str(Path(env_var.value).resolve())}")
                os.environ[env_var.name] = str(Path(env_var.value).resolve())

    @staticmethod
    def all_defined() -> bool:
        """
        Verifies if all listed Environment variables are defined on the system

        :return: True if yes, False otherwise
        """
        all_defined: bool = True
        for env_var in EnvironmentVariables:
            try:
                os.environ[env_var.name]
            except KeyError as e:
                print(f"ERROR: Environment variable {env_var.name} is not defined.")
                all_defined = False
        return all_defined
