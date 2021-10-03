`ares-expedition/instance` directory should contain only `config.py` file, apart from these instructions.

The `instance/config.py` file is used to store sensitive configuration data, such as database credentials, API secrets, etc.

Thus, it __should not__ be committed to version control.

For development purposes, each contributor should create their own `config.py` in this directory and enter the required values.

For production, `config.py` should be created in a secure way (orchestration scripts, or manually on the server).
