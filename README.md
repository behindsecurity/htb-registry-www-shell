# HTB Registry shell as www-data

This Python script automates interactions with Registry's web application, focusing on authentication, configuration editing, file uploading, and remote command execution via a PHP webshell.

## Features

- **Login Automation:** Automates the login process with predefined credentials.
- **Configuration Editing:** Edits the application's configuration file through the web interface.
- **File Uploading:** Uploads a file to the server, typically for establishing a webshell.
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
python3 script.py
```

**Interactive Shell:** After successful execution, the script provides an interactive shell for executing commands on the target server.
