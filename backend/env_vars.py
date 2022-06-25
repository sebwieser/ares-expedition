from enum import Enum
import os
from pathlib import Path


class FlaskEnvironmentVariables(Enum):
    """
    Defines important environment variables for Flask configuration.
    """
    FLASK_APP = 1
    FLASK_ENV = 2

    def get(self):
        """
        Returns env variable value from the system
        """
        return os.environ.get(self.name)


class AresEnvironmentVariables(Enum):
    """
    Defines important environment variables for application configuration.
    Use this to check if variables are defined, or set the undefined ones to default values.
    """
    # Format: ENVIRONMENT VARIABLE = DEFAULT
    APP_CONFIG_FILE = Path(__file__).parent.resolve().joinpath("config/development.py")
    TEST_CONFIG_FILE = Path(__file__).parent.resolve().joinpath("config/test.py")
    LOG_CONFIG_FILE = Path(__file__).parent.resolve().joinpath("config/logging.yaml")

    def get(self):
        """
        Returns env variable value from the system
        """
        return os.environ.get(self.name)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @staticmethod
    def set_undefined_to_default() -> None:
        """
        Sets the undefined env variables to their configured default values
        """
        for env_var in AresEnvironmentVariables:
            e = os.environ.get(env_var.name)
            if e is None:
                print(f"Environment variable {env_var} is undefined. "
                      f"Setting it to default value: {str(Path(env_var.value).resolve())}")
                os.environ[env_var.name] = str(Path(env_var.value).resolve())

    @staticmethod
    def all_defined() -> bool:
        """
        Verifies if all listed Environment variables are defined on the system

        :return: True if yes, False otherwise
        """
        all_defined: bool = True
        for env_var in AresEnvironmentVariables:
            e = os.environ.get(env_var.name)
            if e is None:
                print(f"ERROR: Environment variable {env_var.name} is not defined.")
                all_defined = False
        return all_defined
