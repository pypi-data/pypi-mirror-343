"""
Module for creating a Discord webhook logger using Python's logging module and urllib.

This module provides a custom logging handler (`DiscordHandler`) that sends log messages to a Discord webhook URL.
It includes functionality to validate the webhook URL and send messages via HTTP POST requests using urllib.

Usage example:
    ```python
    logger = SetupDiscordLogger("https://discord.com/api/webhooks/123/abc")
    logger.info("Hello, Discord!")
    ```
"""

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import override


class DiscordHandler(logging.Handler):
    """
    A custom logging handler that sends log messages to a Discord webhook.

    Attributes:
        webhook_url (str): The Discord webhook URL to send messages to.
    """

    def __init__(self, webhook_url: str):
        """
        Initialize the DiscordHandler with a webhook URL.

        Args:
            webhook_url (str): The Discord webhook URL to send log messages to.

        Raises:
            ValueError: If the provided webhook_url is invalid (missing scheme or netloc).

        Example:
            ```python
            handler = DiscordHandler("https://discord.com/api/webhooks/123/abc")
            ```
        """
        super().__init__()
        parsed_url = urllib.parse.urlparse(webhook_url)
        if not (parsed_url.scheme in ("http", "https") and parsed_url.netloc):
            raise ValueError("Invalid webhook URL")
        self.webhook_url = webhook_url

    @override
    def emit(self, record):
        """
        Emit a log record by sending it to the Discord webhook.

        Args:
            record: The log record to be sent.

        Raises:
            None: Errors during the HTTP request are caught and logged to the default logger.

        Example:
            ```python
            handler = DiscordHandler("https://discord.com/api/webhooks/123/abc")
            record = logging.LogRecord(name="test", level=20, pathname="", lineno=0,
                                     msg="Test message", args=(), exc_info=None)
            handler.emit(record)
            ```
        """
        message = self.format(record)
        data = json.dumps({"content": message}).encode("utf-8")
        req = urllib.request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        try:
            urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            logging.getLogger().error(f"Failed to send Discord webhook: {e}")


def SetupDiscordLogger(
    webhook_url: str, name: str = "discord_logger"
) -> logging.Logger:
    """
    Set up a logger that sends messages to a Discord webhook.

    Args:
        webhook_url (str): The Discord webhook URL to send log messages to.
        name (str, optional): The name of the logger. Defaults to "discord_logger".

    Returns:
        logging.Logger: A configured logger with a DiscordHandler.

    Raises:
        ValueError: If the webhook_url is invalid (missing scheme or netloc).

    Example:
        ```python
        logger = SetupDiscordLogger("https://discord.com/api/webhooks/123/abc")
        logger.info("This is a test message!")
        ```
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = DiscordHandler(webhook_url)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
