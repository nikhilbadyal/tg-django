"""Handle help command."""

from telethon import events

from telegram.commands.base import BaseCommand, CommandRegistry
from telegram.strings import command_not_found, docs_not_found
from telegram.utils import SupportedCommands


@CommandRegistry.register("help")
class HelpCommand(BaseCommand):
    """Handle /help command."""

    def get_pattern(self) -> str:
        """Return the regex pattern for /help command.

        Returns
        -------
            Regex pattern string
        """
        return f"^{SupportedCommands.HELP.value}(.*)"

    def get_usage(self) -> str:
        """Return the usage documentation for /help command.

        Returns
        -------
            Usage documentation string
        """
        return "Really bro🥸."

    def _get_help_message(self) -> str:
        """Generate the main help message dynamically from registered commands.

        Returns
        -------
            Formatted help message string
        """
        commands = CommandRegistry.get_all_commands()
        command_list = []

        for idx, (cmd_name, _) in enumerate(commands.items(), start=1):
            command_list.append(f"{idx}. `/{cmd_name}`: Start using the bot (usage: `/{cmd_name}`).")

        command_lines = "\n".join(command_list)

        return f"""
Hey there, Welcome to the Help Center

Here's a list of supported commands:

{command_lines}

For more information on each command, type `/help <command>`.

If you have any questions or need assistance, feel free to ask. Happy botting!
"""

    def _get_command_usage(self, command_name: str) -> str:
        """Get usage documentation for a specific command.

        Args:
            command_name: Name of the command (without the '/' prefix)

        Returns
        -------
            Usage documentation string

        Raises
        ------
            KeyError: If command is not found in registry
        """
        command_class = CommandRegistry.get_command(command_name)
        if command_class is None:
            msg = f"Command '{command_name}' not found in registry"
            raise KeyError(msg)

        # Instantiate the command with env (needed for get_usage)
        command_instance = command_class(self.env)
        return command_instance.get_usage()

    async def handle(self, event: events.NewMessage.Event) -> None:
        """Handle /help command.

        Args:
            event: A new message event.
        """
        data = event.pattern_match.group(1).strip()

        if not data:
            # Show general help message
            await event.reply(self._get_help_message())
        elif f"/{data}" not in SupportedCommands.get_values():
            # Command not supported
            await event.reply(command_not_found)
        else:
            # Show specific command usage
            try:
                usage = self._get_command_usage(data)
                await event.reply(usage)
            except KeyError:
                await event.reply(docs_not_found)
