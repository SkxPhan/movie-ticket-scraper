import requests
import logging


def send_slack_message(webhook_url: str, message: str) -> None:
    """Sends a message to a Slack channel using a webhook.

    Args:
        webhook_url (str): The Webhook URL of the Slack channel.
        message (str): The message to send in the Slack channel.

    Raises:
        requests.exceptions.RequestException: If there is an error sending the message.
            This could include network issues, timeouts, or invalid webhook URLs.
    """
    try:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logging.info("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")
