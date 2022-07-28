# Terraforming Mars: Ares Expedition <img src="https://img.icons8.com/external-sbts2018-flat-sbts2018/58/000000/external-mars-space-sbts2018-flat-sbts2018.png"/> 

> This is an open-source online implementation of the board game [Terraforming Mars: Ares Expedition](https://boardgamegeek.com/boardgame/328871/terraforming-mars-ares-expedition). 
The project is not affiliated with [FryxGames](https://boardgamegeek.com/boardgamepublisher/18575/fryxgames) nor [Stronghold Games](https://boardgamegeek.com/boardgamepublisher/11652/stronghold-games) in any way.

## About The Game

This great card game is a 2021. [Kickstarter project](https://www.kickstarter.com/projects/strongholdgames/ares-expedition-the-terraforming-mars-card-game).

It is a more streamlined version (a spin-off, really) to the incredibly popular [Terraforming Mars](https://boardgamegeek.com/boardgame/167791/terraforming-mars) board game.

If you would like to learn the rules, [here](https://youtu.be/Nbrkfu_bVBM) is a good tutorial video to watch.

## Reporting Bugs Or Requesting Features
Please use the [issues tab](https://github.com/sebwieser/ares-expedition/issues/new) on this project.

## Setting Up Development Environment
### 1. Prerequisites
Before installing the project, you will need a few tools:
* `Python 3.9+` is required to start the project.
* `pip` is required to manage project requirements.
* Python virtual environment is advised. When creating it, make sure the name starts with `venv` as the exception is already added to `.gitignore`.
* Node.js virtual env is also advised. It will be automatically created and configured via `install` script

### 2. Installing
Clone the project, then `cd` into the repository root and run:
#### Windows
    install.bat
#### Linux/MacOS
    install.sh

### 3. Additional configuration
It's important to note that`FLASK_APP` and `FLASK_ENV` environment variables are mandatory 
to run the backend project in any Flask environment (`production` or `development`).

But, in `development` environment, it is not mandatory to set the 3 config file variables manually: `APP_CONFIG_FILE`, `TEST_CONFIG_FILE`, `LOG_CONFIG_FILE`.
If omitted, they will be set to their default project values.

If you wish to change those default locations, set the following env variables manually or append them to `backend/.env` file:

    APP_CONFIG_FILE=<config_absolute_path>
    TEST_CONFIG_FILE=<test_config_absolute_path>
    LOG_CONFIG_FILE=<log_config_absolute_path>

## Testing
To execute the backend test battery, run: `cd backend && python -m pytest`

## Running the project
#### Windows
    run.bat
#### Linux/MacOS
    run.sh

## License
GPLv3