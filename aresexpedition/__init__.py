from flask import Flask
from .views.homepage import homepage
from pathlib import Path


def create_app(test: bool = False) -> Flask:
    """
    Creates and returns a Flask app from the config file described in an appropriate environment variable

    :param test: If set to True, instance specific secrets won't be loaded from instance/config.py,
    expecting test config file to load all necessary configurations
    :return: An instance of a Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    default_config_file: str = 'config.default'
    instance_config_file: str = 'config.py'
    instance_config_file_path: Path = Path(app.instance_path).joinpath(instance_config_file)
    config_file_envvar: str = 'APP_CONFIG_FILE' if not test else 'TEST_CONFIG_FILE'

    # 1. Load the default configuration
    app.config.from_object(default_config_file)

    if not test:
        # 2. Load the environment related config file defined in the environment variable
        # Variables defined here will override those in the default configuration
        try:
            app.config.from_envvar(config_file_envvar)
        except RuntimeError:
            # TODO: instead of printing it, log the warning if the APP_CONFIG_FILE variable is not found
            print(f"WARNING: Could not find {config_file_envvar} environment variable. "
                  f"This means that the application configuration will use default settings "
                  f"defined in config/default.py file. If that is not intended, please make sure that this "
                  f"variable is set to the absolute path of the current application environment.")

        # 3. Load the configuration from the instance folder if we're not testing
        # This config file contains sensitive data and as such, isn't committed to version control
        if not instance_config_file_path.exists():
            print(f"WARNING: Could not locate {instance_config_file_path} file, creating an empty one. "
                  f"This means that values from configuration file in {config_file_envvar} will be used."
                  f"If that is not intended, "
                  f"please populate the {instance_config_file_path} file with desired overrides. ")
            instance_config_file_path.touch()
        app.config.from_pyfile(instance_config_file)
    else:
        # If we're testing, load config file without exception handling,
        # otherwise it won't be obvious why the tests fail
        app.config.from_envvar(config_file_envvar)

    # Register views
    app.register_blueprint(homepage)
    return app
