# HTB Registry shell as www-data

This Python script automates interactions with Registry's web application, focusing on authentication, configuration editing, file uploading, and remote command execution via a PHP webshell.

## Features

- **Login Automation:** Automates the login process with predefined credentials.
- **Configuration Editing:** Edits the application's configuration file through the web interface.
- **File Uploading:** Uploads a php script to the server in order to establish a webshell.
- **Command Execution:** Executes commands on the server through the uploaded PHP webshell.

## Requirements

- `requests` library
- `beautifulsoup4` library

Ensure you have the required Python libraries installed:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script with Python 3:

```bash
python3 main.py
```

**Interactive Shell:** After successful execution, the script provides a semi-interactive shell for executing commands on the target server.
