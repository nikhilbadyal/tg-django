"""Utility functions."""

from enum import Enum
from typing import Any

from loguru import logger
from telethon import events, types
from telethon.extensions import markdown
from telethon.tl.types import User as TelegramUser

from sqlitedb.models import User

# Number of records per page
PAGE_SIZE = 10


class CustomMarkdown:
    """Custom Markdown parser."""

    @staticmethod
    def parse(text: str) -> Any:
        """Parse."""
        text, entities = markdown.parse(text)
        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == "spoiler":
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith("emoji/"):
                    entities[i] = types.MessageEntityCustomEmoji(
                        e.offset,
                        e.length,
                        int(e.url.split("/")[1]),
                    )
        return text, entities

    @staticmethod
    def unparse(text: str, entities: Any) -> Any:
        """Unparse."""
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(
                    e.offset,
                    e.length,
                    f"emoji/{e.document_id}",
                )
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(e.offset, e.length, "spoiler")
        return markdown.unparse(text, entities)


# Define a list of supported commands
class SupportedCommands(Enum):
    """Enum for supported commands."""

    START = "/start"
    HELP = "/help"

    @classmethod
    def get_values(cls) -> list[str]:
        """Returns a list of all the values of the SupportedCommands enum.

        Returns
        -------
            list: A list of all the values of the SupportedCommands enum.
        """
        return [command.value for command in cls]

    def __str__(self) -> str:
        """Returns the string representation of the enum value.

        Returns
        -------
            str: The string representation of the enum value.
        """
        return self.value


async def get_telegram_user(event: events.NewMessage.Event) -> TelegramUser:
    """Get the user associated with a message event in Telegram.

    Args:
        event (events.NewMessage.Event): The message event.

    Returns
    -------
        User: The User entity associated with the message event.
    """
    try:
        # Get the user entity from the peer ID of the message event, Uses cache
        user: TelegramUser = await event.client.get_entity(event.peer_id)
    except (ValueError, AttributeError):
        logger.debug("Couldn't get user from cache. Invalid Peer ID")
        user = await event.get_sender()
    return user


def get_regex() -> str:
    """Generate a regex pattern that matches any message that is not a supported command.

    Returns
    -------
        str: A regex pattern as a string.
    """
    # Exclude any message that starts with one of the supported commands using negative lookahead
    return r"^(?!({}))[/].*".format("|".join(SupportedCommands.get_values()))


class UserSettings(Enum):
    """User Settings."""

    PAGE_SIZE = "page_size", "The number of records displayed per page."

    def __new__(cls, *args: Any, **_: Any) -> "UserSettings":
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: str, description: str | None = None) -> None:
        self._description_ = description

    def __str__(self) -> str:
        return str(self.value)

    @property
    def description(self) -> str | None:
        """Returns the description of the setting.

        Returns
        -------
            Optional[str]: The description of the setting.
        """
        return self._description_


async def get_user(event: events.NewMessage.Event) -> User:
    """Get out user from telegram user."""
    telegram_user: TelegramUser = await get_telegram_user(event)
    return await User.objects.get_user(telegram_user=telegram_user)
