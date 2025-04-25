from rich.console import Console
from rich.table import Table

from pyros_cli.services.commands.base_command import BaseCommand, CommandResult

console = Console()

class HelpCommand(BaseCommand):
    """Help command to display available commands"""
    
    name = "/help"
    help_text = "Display available commands"
    
    def __init__(self, command_registry=None):
        self.command_registry = command_registry
    
    async def execute(self, args: str) -> CommandResult:
        """Display help for available commands"""
        table = Table(title="Available Commands")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="green")
        
        if self.command_registry:
            for cmd_name, cmd_instance in sorted(self.command_registry.items()):
                table.add_row(cmd_name, cmd_instance.help_text)
                
        console.print(table)
        return CommandResult(is_command=True, should_generate=False) 