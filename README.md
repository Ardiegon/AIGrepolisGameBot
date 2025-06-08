# AIGrepolisGameBot
Computer Vision based (simulating real user, hence not detectable) assistant for doing basic and boring stuff automatically in grepolis.

## Features

- Automates repetitive tasks in Grepolis using computer vision.
- Simulates real user interactions to avoid detection.
- Modular and extensible codebase for adding new automation features only by edditing yaml files.
- Configurable task scheduling and execution.
- Logs actions and errors.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/AIGrepolisGameBot.git
    cd AIGrepolisGameBot
    ```

2. **Install dependencies:**
    ```bash
    pip install -e .
    ```

3. **Configure settings:**
    - Edit `config.yaml` to set up your preferences and credentials.

## Usage

1. **Preparing Environment**
    - Turn off screen saver so the screen is always on
    - Turn on Grepolis in Google Chrome. (Your City view, or the screen with worlds to choose)

2. **Start the bot:**
    ```bash
    python grepobot
    ```

3. **Monitor logs:**
    - Check terminal (WILL BE CHANGED TO LOG FILE) to see what the bot is doing

## Configuration
    - Bot currently is able to log in, solve captcha, gather resources from all cottages, and reset.
    - To add more configurations edit config.yaml, and contribute to this repository.

## Adding new Actions and Events
    - See the congig.yaml to specify which actions to perform
    - Add new actions in grepobot/config/actions.yaml

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description.

## Disclaimer

This project is for educational purposes only. Use at your own risk. Automating online games may violate their terms of service.