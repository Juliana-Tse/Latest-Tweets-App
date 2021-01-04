## This project retrieves the latest 10 tweets from an authorized user.

### Installation
1. Download python3.7
2. Download the project folder and go to the project root path
3. Copy `env_updated` file into the project root path and rename it as `.env`
4. Create a virtual environment
    ```
    python3 -m venv venv
    ```
5. Activate the virtual environment
    ```
    . venv/bin/activate
    ```
6. Install dependencies
    ```
    python3 -m pip install -r requirements.txt
    ```
7. Run the application on `http://127.0.0.1:5000/`
    ```
    flask run
    ```

Note: For Windows user, please refer to this [link](https://flask.palletsprojects.com/en/1.1.x/installation/#installation) for setting up virtual environment

### Testing
1. Run ```pytest -v```

