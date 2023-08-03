"""Handle help command."""

# Import necessary libraries and modules
from telethon import TelegramClient, events

from telegram.strings import command_not_found, docs_not_found

# Import some helper functions
from telegram.utils import SupportedCommands, command_help

help_message = """
Hey there,Welcome to the Help Center

Here's a list of supported commands:

1. `/start`: Start using the bot (usage: `/start`).

For more information on each command, type `/help <command>`.

If you have any questions or need assistance, feel free to ask. Happy botting!
"""


def add_help_handlers(client: TelegramClient) -> None:
    """Add /help command Event Handler."""
    client.add_event_handler(handle_help_message)


def help_usage() -> str:
    """Return the usage of add command."""
    usage = "Really bro🥸."
    return usage


# Register the function to handle the /help command
@events.register(events.NewMessage(pattern=f"^{SupportedCommands.HELP.value}(.*)"))  # type: ignore
async def handle_help_message(event: events.NewMessage.Event) -> None:
    """Handle /help command.

    Args:
        event (events.NewMessage.Event): A new message event.

    Returns:
        None: This function doesn't return anything.
    """
    data = event.pattern_match.group(1).strip()
    if not data:
        await event.reply(help_message)
    else:
        if f"/{data}" not in SupportedCommands.get_values():
            await event.reply(command_not_found)
        else:
            try:
                usage = command_help(data)
                await event.reply(usage)
            except KeyError:
                await event.reply(docs_not_found)
