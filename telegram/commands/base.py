"""Base command class for all bot commands."""

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from environs import Env
from telethon import TelegramClient, events


class CommandRegistry:
    """Registry for automatic command registration."""

    _commands: ClassVar[dict[str, type["BaseCommand"]]] = {}

    @classmethod
    def register(cls, command_name: str) -> Any:
        """Decorator to register a command class.

        Args:
            command_name: The name of the command (e.g., 'start', 'help')

        Returns
        -------
            The decorator function
        """

        def decorator(command_class: type["BaseCommand"]) -> type["BaseCommand"]:
            cls._commands[command_name] = command_class
            return command_class

        return decorator

    @classmethod
    def get_all_commands(cls) -> dict[str, type["BaseCommand"]]:
        """Get all registered commands.

        Returns
        -------
            Dictionary mapping command names to command classes
        """
        return cls._commands.copy()

    @classmethod
    def get_command(cls, command_name: str) -> type["BaseCommand"] | None:
        """Get a specific command class.

        Args:
            command_name: The name of the command

        Returns
        -------
            The command class or None if not found
        """
        return cls._commands.get(command_name)


class BaseCommand(ABC):
    """Abstract base class for all bot commands.

    This class provides common functionality for all commands and eliminates
    duplicate code across command implementations.
    """

    def __init__(self, env: Env) -> None:
        """Initialize the command with environment configuration.

        Args:
            env: Environment configuration object
        """
        self.env = env

    @abstractmethod
    def get_pattern(self) -> str:
        """Return the regex pattern for this command.

        Returns
        -------
            Regex pattern string
        """

    @abstractmethod
    async def handle(self, event: events.NewMessage.Event) -> None:
        """Handle the command event.

        Args:
            event: The Telegram message event
        """

    @abstractmethod
    def get_usage(self) -> str:
        """Return the usage documentation for this command.

        Returns
        -------
            Usage documentation string
        """

    def add_handler(self, client: TelegramClient) -> None:
        """Add this command's event handler to the client.

        Args:
            client: The Telegram client instance
        """
        # Create a wrapper that applies the pattern decorator
        handler = events.register(events.NewMessage(pattern=self.get_pattern()))(self.handle)
        client.add_event_handler(handler)
