# Terraforming Mars: Ares Expedition

This is an open-source online implementation of the board game [Terraforming Mars: Ares Expedition](https://boardgamegeek.com/boardgame/328871/terraforming-mars-ares-expedition). 
The project is not affiliated with [FryxGames](https://boardgamegeek.com/boardgamepublisher/18575/fryxgames) nor [Stronghold Games](https://boardgamegeek.com/boardgamepublisher/11652/stronghold-games) in any way.

### About The Game

This great card game is a 2021. [Kickstarter project](https://www.kickstarter.com/projects/strongholdgames/ares-expedition-the-terraforming-mars-card-game)
and is [soon hitting the retail in US](https://www.kickstarter.com/projects/strongholdgames/ares-expedition-the-terraforming-mars-card-game/posts/3224358).
Europe will be following soon after, undoubtedly.

If you would like to learn the rules, [here](https://youtu.be/Nbrkfu_bVBM) is a good tutorial video to watch.

### Reporting Bugs Or Requesting Features
Please use the [issues tab](https://github.com/sebwieser/ares-expedition/issues/new) on this project.

### Setting Up Development Environment
Prerequisites:
* `Python 3.9+` is required to start the project.
* `pip` is required to manage project requirements.
* virtual environment is advised. When creating it, make sure the name starts with `venv` as the exception is already added to `.gitignore`. 

Clone the project, then `cd` into the repository root and run:
#### Linux/MacOS:
    pip install -r requirements.txt
    export FLASK_APP=src/backend/aresexpedition
    export FLASK_ENV=development
    flask run

#### Windows:
    pip install -r requirements.txt
    SET FLASK_APP=src/backend/aresexpedition
    SET FLASK_ENV=development
    flask run

And that's it, you're all set!

##### _Special note: Overriding config file locations_
It's important to note that`FLASK_APP` and `FLASK_ENV` environment variables are mandatory 
to run the project in any Flask environment (`production` or `development`).

But, in `development` environment, it is not mandatory to set the 3 config file variables manually: `APP_CONFIG_FILE`, `TEST_CONFIG_FILE`, `LOG_CONFIG_FILE`.
If omitted, they will be set to their default project values if possible.

If you wish to change those default locations, follow these instructions:

###### Linux/MacOS
    export APP_CONFIG_FILE=<config_absolute_path>
    export TEST_CONFIG_FILE=<test_config_absolute_path>
    export LOG_CONFIG_FILE=<log_config_absolute_path>

###### Windows
    SET APP_CONFIG_FILE=<config_absolute_path>
    SET TEST_CONFIG_FILE=<test_config_absolute_path>
    SET LOG_CONFIG_FILE=<log_config_absolute_path>

Make sure to:
* replace the `<config_absolute_path>` with absolute path to the desired _existing_ location.
* replace the `<test_config_absolute_path>` with absolute path to the desired _existing_ location.
* replace the `<log_config_absolute_path>` with absolute path to the desired _existing_ location.

### Testing
To execute the test battery, run: `python -m pytest`

Additional info:
Test application context does not use instance relative config (sensitive data in separate file).
This means that all test configuration parameters should be defined in an environment config file (i.e. `config\test.py`).
Reminder; don't forget to set `TEST_CONFIG_FILE` environment variable pointing to that file, before you run the tests.

### LICENSE
GPLv3