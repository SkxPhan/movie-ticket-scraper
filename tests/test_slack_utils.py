from pathlib import Path
import configparser
import pytest
from scraper.slack_utils import send_slack_message


@pytest.fixture(scope="module")
def test_webhook_url():
    # Get the path to the config.ini file
    config_file_path = Path(__file__).resolve().parent.parent / "scraper" / "config.ini"
    config = configparser.ConfigParser()
    config.read(config_file_path)
    test_webhook_url = config.get("Testing", "TEST_SLACK_WEBHOOK_URL")
    if not test_webhook_url:
        raise ValueError("Config file missing slack webhook url for testing.")
    return test_webhook_url


def test_send_slack_message(test_webhook_url):
    message = "This is a test message from pytest!"
    try:
        send_slack_message(test_webhook_url, message)
        # If no exceptions are raised, the test should pass
        assert True
    except Exception as e:
        # If any exception is raised, the test should fail
        pytest.fail(f"Failed to send message: {e}")
