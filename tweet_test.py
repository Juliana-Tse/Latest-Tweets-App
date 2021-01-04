from tweet import create_app
from dotenv import load_dotenv
import pytest
import os

@pytest.fixture()
def mock_env(monkeypatch):
    load_dotenv()
    monkeypatch.setenv('CONSUMER_API_KEY', os.environ["CONSUMER_API_KEY"])
    monkeypatch.setenv('CONSUMER_API_SECRET_KEY', os.environ["CONSUMER_API_SECRET_KEY"])
    monkeypatch.setenv('ACCESS_TOKEN', os.environ["ACCESS_TOKEN"])
    monkeypatch.setenv('ACCESS_TOKEN_SECRET', os.environ["ACCESS_TOKEN_SECRET"])

@pytest.fixture()
def mock_wrong_env(monkeypatch):
    monkeypatch.setenv('CONSUMER_API_KEY', "")
    monkeypatch.setenv('CONSUMER_API_SECRET_KEY', "")
    monkeypatch.setenv('ACCESS_TOKEN', "")
    monkeypatch.setenv('ACCESS_TOKEN_SECRET', "")
    
@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.mark.usefixtures("mock_env")
def test_success_latest_tweets(client):
    username = "dan_abramov"
    rv = client.post("/", data={"username": username})
    assert b"Not authorized." not in rv.data
    assert b"Sorry, that page does not exist." not in rv.data

def test_unauthorized_user_latest_tweets(client):
    username = "tse_juliana"
    rv = client.post("/", data={"username": username})
    assert b"Not authorized." in rv.data

def test_unexist_user_latest_tweets(client):
    username = "qqwwabc"
    rv = client.post("/", data={"username": username})
    assert b"Sorry, that page does not exist." in rv.data

def test_main_route_status_code(client) -> None:
    rv = client.get("/")
    assert rv.status_code == 200

@pytest.mark.usefixtures("mock_wrong_env")
def test_incorrect_oauth_credentials(client):
    username = "dan_abramov"
    rv = client.post("/", data={"username": username})
    assert b"Bad Authentication data." in rv.data