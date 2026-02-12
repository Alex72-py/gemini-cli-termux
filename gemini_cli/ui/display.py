"""
Display and formatting utilities using Rich library.
Provides beautiful terminal output for the CLI.
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
from typing import Optional


class Display:
    """Handles all terminal output and formatting."""
    
    def __init__(self, theme: str = "monokai"):
        """
        Initialize display handler.
        
        Args:
            theme: Syntax highlighting theme
        """
        self.console = Console()
        self.theme = theme
    
    def print(self, text: str, style: Optional[str] = None) -> None:
        """
        Print text with optional styling.
        
        Args:
            text: Text to print
            style: Rich style string
        """
        self.console.print(text, style=style)
    
    def print_markdown(self, text: str) -> None:
        """
        Print text as formatted markdown.
        
        Args:
            text: Markdown text
        """
        md = Markdown(text, code_theme=self.theme)
        self.console.print(md)
    
    def print_code(self, code: str, language: str = "python") -> None:
        """
        Print syntax-highlighted code.
        
        Args:
            code: Code to print
            language: Programming language
        """
        syntax = Syntax(code, language, theme=self.theme, line_numbers=True)
        self.console.print(syntax)
    
    def print_panel(
        self,
        text: str,
        title: Optional[str] = None,
        style: str = "cyan"
    ) -> None:
        """
        Print text in a panel/box.
        
        Args:
            text: Text to display
            title: Optional panel title
            style: Panel style
        """
        panel = Panel(text, title=title, border_style=style, box=box.ROUNDED)
        self.console.print(panel)
    
    def print_table(self, headers: list, rows: list) -> None:
        """
        Print a formatted table.
        
        Args:
            headers: List of column headers
            rows: List of row data
        """
        table = Table(box=box.ROUNDED)
        
        for header in headers:
            table.add_column(header, style="cyan")
        
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        
        self.console.print(table)
    
    def print_error(self, message: str) -> None:
        """
        Print an error message.
        
        Args:
            message: Error message
        """
        self.console.print(f"[bold red]✗ Error:[/bold red] {message}")
    
    def print_success(self, message: str) -> None:
        """
        Print a success message.
        
        Args:
            message: Success message
        """
        self.console.print(f"[bold green]✓ Success:[/bold green] {message}")
    
    def print_warning(self, message: str) -> None:
        """
        Print a warning message.
        
        Args:
            message: Warning message
        """
        self.console.print(f"[bold yellow]⚠ Warning:[/bold yellow] {message}")
    
    def print_info(self, message: str) -> None:
        """
        Print an info message.
        
        Args:
            message: Info message
        """
        self.console.print(f"[bold blue]ℹ Info:[/bold blue] {message}")
    
    def spinner(self, text: str = "Processing..."):
        """
        Create a spinner for long operations.
        
        Args:
            text: Spinner text
            
        Returns:
            Progress context manager
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        )
    
    def clear(self) -> None:
        """Clear the terminal screen."""
        self.console.clear()
    
    def rule(self, title: Optional[str] = None, style: str = "dim") -> None:
        """
        Print a horizontal rule.
        
        Args:
            title: Optional title for the rule
            style: Rule style
        """
        self.console.rule(title, style=style)
