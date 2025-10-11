"""Reply to messages."""

import sys

from environs import Env
from loguru import logger
from telethon import TelegramClient

# Import command modules to trigger registration
# These imports trigger the @CommandRegistry.register decorators
import telegram.commands.help
import telegram.commands.start  # noqa: F401
from telegram.commands.base import CommandRegistry
from telegram.utils import CustomMarkdown


class Telegram(object):
    """A class representing a Telegram bot."""

    def __init__(self, session_file: str, env: Env) -> None:
        """Create a new Telegram object and connect to the Telegram API using the given session file.

        Args:
            session_file: The path to the session file to use for connecting to the Telegram API.
            env: Environment configuration object.
        """
        self.env = env

        # Create a new TelegramClient instance with the given session file and API credentials
        self.client: TelegramClient = TelegramClient(
            session_file,
            env.int("API_ID"),
            env.str("API_HASH"),
            sequential_updates=True,
        )
        # Connect to the Telegram API using bot authentication
        logger.debug("Trying to connect using bot token")
        self.client.start(bot_token=env.str("BOT_TOKEN"))
        # Check if the connection was successful
        if self.client.is_connected():
            self.client.parse_mode = CustomMarkdown()
            logger.info("Connected to Telegram")
            logger.info("Using bot authentication. Only bot messages are recognized.")
        else:
            logger.info("Unable to connect with Telegram exiting.")
            sys.exit(1)

    def bot_listener(self) -> None:
        """Listen for incoming bot messages and handle them based on the command."""
        # Automatically register all commands from the registry
        commands = CommandRegistry.get_all_commands()
        logger.info(f"Registering {len(commands)} commands: {list(commands.keys())}")

        for command_name, command_class in commands.items():
            # Instantiate each command with env and register its handler
            command_instance = command_class(self.env)
            command_instance.add_handler(self.client)
            logger.debug(f"Registered handler for /{command_name}")

        # Start listening for incoming bot messages
        self.client.run_until_disconnected()

        # Log a message when the bot stops running
        logger.info("Stopped!")
