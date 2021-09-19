import os
import sys
from flask import Flask
from .views.homepage import homepage
from pathlib import Path
from logging.config import dictConfig
import yaml
from env_vars import EnvironmentVariables


def configure_logging() -> None:
    log_conf_file: Path = Path(EnvironmentVariables.get(EnvironmentVariables.LOG_CONFIG_FILE))
    try:
        with open(log_conf_file, "r") as logging_conf_file:
            logging_conf: dict = yaml.safe_load(logging_conf_file)
            log_target_file: Path = Path(logging_conf["handlers"]["rotfile"]["filename"])
            if not log_target_file.parent.exists():
                print(f"Logging configuration specifies the logging path {log_target_file}, but it doesn't exist. "
                      f"Creating missing parent directories...")
                log_target_file.parent.mkdir(parents=True)
            dictConfig(logging_conf)
    except FileNotFoundError as e:
        sys.exit(f"Logging setup failed, stopping the server: {e}")
    except ValueError as e:
        sys.exit(f"Logging setup failed, stopping the server. "
                 f"Please check that the logging config file is well defined and all directories exist: {e}")
    except KeyError as e:
        sys.exit(f"Logging setup failed, stopping the server. "
                 f"Couldn't locate log filename from config dictionary: {e}")


def create_app(test: bool = False) -> Flask:
    """
    Creates and returns a Flask app from the config file described in an appropriate environment variable

    :param test: If set to True, instance specific secrets won't be loaded from instance/config.py,
    expecting test config file to load all necessary configurations
    :return: An instance of a Flask app
    """

    if os.environ["FLASK_ENV"] == "development":
        EnvironmentVariables.set_undefined_to_default()
    if not EnvironmentVariables.all_defined():
        sys.exit("Application could not be properly configured. "
                 "Missing environment variable definitions. Stopping the server...")

    configure_logging()

    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    default_config_file: str = 'config.default'
    instance_config_file: str = 'config.py'
    instance_config_file_path: Path = Path(app.instance_path).joinpath(instance_config_file)
    config_file_envvar: str = 'APP_CONFIG_FILE' if not test else 'TEST_CONFIG_FILE'
    # 1. Load the default configuration
    app.logger.info(f"Applying default settings for the application from {default_config_file} file")
    app.config.from_object(default_config_file)

    if not test:
        # 2. Load the environment related config file defined in the environment variable
        # Variables defined here will override those in the default configuration
        try:
            app.logger.info(f"Overriding default settings using the file defined in {config_file_envvar} env var")
            app.config.from_envvar(config_file_envvar)
        except RuntimeError:
            app.logger.warning(f"Could not find {config_file_envvar} environment variable. "
                               f"This means that the application configuration will use default settings "
                               f"defined in config/default.py file. "
                               f"If that is not intended, please make sure that this "
                               f"variable is set to the absolute path of the current application environment.")

        # 3. Load the configuration from the instance folder if we're not testing
        # This config file contains sensitive data and as such, isn't committed to version control
        if not instance_config_file_path.exists():
            app.logger.warning(f"Could not locate {instance_config_file_path} file, creating an empty one. "
                               f"This means that values from configuration file in {config_file_envvar} will be used."
                               f"If that is not intended, "
                               f"please populate the {instance_config_file_path} file with desired overrides. ")
            instance_config_file_path.touch()
        app.logger.info(f"Overriding sensitive environment settings using the {instance_config_file_path}")
        app.config.from_pyfile(instance_config_file)
    else:
        # If we're testing, load config file without exception handling.
        # Otherwise it won't be obvious why the tests fail.
        app.logger.debug(f"Loading test environment settings from {config_file_envvar}")
        app.config.from_envvar(config_file_envvar)

    app.logger.info("Registering application views")
    app.register_blueprint(homepage)
    return app
