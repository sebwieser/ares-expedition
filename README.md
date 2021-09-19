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
    EXPORT FLASK_APP=aresexpedition
    EXPORT FLASK_ENV=development
    EXPORT APP_CONFIG_FILE=<config_absolute_path>
    EXPORT TEST_CONFIG_FILE=<test_config_absolute_path>
    flask run

#### Windows:
    pip install -r requirements.txt
    SET FLASK_APP=aresexpedition
    SET FLASK_ENV=development
    SET APP_CONFIG_FILE=<config_absolute_path>
    SET TEST_CONFIG_FILE=<test_config_absolute_path>
    flask run

Make sure to:
* replace the `<config_absolute_path>` with absolute path to `ares-expedition\config\development.py`.
* replace the `<test_config_absolute_path>` with absolute path to `ares-expedition\config\test.py`.

And that's it, you're all set!

### Testing
To execute the test battery, run: `python -m pytest`

Additional info:
Test application context does not use instance relative config (sensitive data in separate file).
This means that all test configuration parameters should be defined in an environment config file (i.e. `config\test.py`).
Reminder; don't forget to set `TEST_CONFIG_FILE` environment variable pointing to that file, before you run the tests.

### LICENSE
GPLv3