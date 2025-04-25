import random
import questionary
from rich.console import Console

from pyros_cli.services.commands.base_command import BaseCommand, CommandResult
from pyros_cli.models.prompt_vars import load_prompt_vars
from flock.cli.utils import print_subheader

console = Console()

class ListVarsCommand(BaseCommand):
    """Command to list prompt variables"""
    
    name = "/list-vars"
    help_text = "List all available prompt variables"
    
    def __init__(self, command_registry=None):
        self.command_registry = command_registry
    
    async def execute(self, args: str) -> CommandResult:
        """List all available prompt variables"""
        prompt_vars = load_prompt_vars()
        
        if not prompt_vars:
            console.print("No prompt variables found.", style="yellow")
            return CommandResult(is_command=True, should_generate=False)
            
        choices = [
            f"{var.prompt_id} - {var.description[:50] + '...' if var.description and len(var.description) > 50 else var.description or 'No description'}\n"
            for var in prompt_vars.values()
        ]
        
        selected = await questionary.select(
            "Select a prompt variable to view:",
            choices=choices
        ).ask_async()
        
        if not selected:
            return CommandResult(is_command=True, should_generate=False)
            
        # Extract the prompt_id from the selection
        prompt_id = selected.split(" - ")[0]
        
        if prompt_id in prompt_vars:
            var = prompt_vars[prompt_id]
            print_subheader(f"[bold cyan]Prompt Variable:[/] {var.prompt_id}")

            console.line()
            
            if var.description:
                console.print(f"[bold cyan]Description:[/] {var.description}")
                
            console.print(f"[bold cyan]File Path:[/] {var.file_path}")
            
            console.line()
            if var.values:
                # Show only 5 random values if there are more than 5
                sample_size = min(5, len(var.values))
                # Get 5 random indices from the values list
                sample_indices = random.sample(range(len(var.values)), sample_size)
                # Sort the indices to show them in order
                sample_indices.sort()
                
                console.print(f"[bold cyan]Values[/] (showing {sample_size} of {len(var.values)}):")
                for idx in sample_indices:
                    console.print(f"  {idx}. {var.values[idx]}")
            else:
                console.print("[yellow]No values found.[/]")
                
        return CommandResult(is_command=True, should_generate=False) 