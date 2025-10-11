"""Handle start command."""

from telethon import events

from telegram.commands.base import BaseCommand, CommandRegistry
from telegram.utils import SupportedCommands, get_user


@CommandRegistry.register("start")
class StartCommand(BaseCommand):
    """Handle /start command."""

    def get_pattern(self) -> str:
        """Return the regex pattern for /start command.

        Returns
        -------
            Regex pattern string
        """
        return f"^{SupportedCommands.START.value}$"

    def get_usage(self) -> str:
        """Return the usage documentation for /start command.

        Returns
        -------
            Usage documentation string
        """
        return "It can be used to check if bot is alive or dead.\n"

    async def handle(self, event: events.NewMessage.Event) -> None:
        """Handle /start command.

        Args:
            event: A new message event.
        """
        # Get the user associated with the message
        user = await get_user(event)
        result = f"Hii👋, {user.name} {user.telegram_id}"
        await event.reply(result)
