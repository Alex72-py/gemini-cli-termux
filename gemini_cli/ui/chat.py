"""
Interactive chat interface using prompt_toolkit.
Provides a rich terminal-based chat experience.
"""

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from gemini_cli.ui.display import Display
from gemini_cli.core.client import GeminiClient
from gemini_cli.utils.clipboard import Clipboard
from gemini_cli.utils.memory import ConversationMemory


class ChatInterface:
    """Interactive chat interface for Gemini."""
    
    # Chat commands
    COMMANDS = {
        "/exit": "Exit chat",
        "/quit": "Exit chat",
        "/clear": "Clear conversation history",
        "/history": "Show conversation history",
        "/copy": "Copy last response to clipboard",
        "/save": "Save conversation to file",
        "/model": "Switch model (e.g., /model 1.5-pro)",
        "/help": "Show this help message",
    }
    
    def __init__(
        self,
        client: GeminiClient,
        display: Display,
        clipboard: Clipboard,
        memory: ConversationMemory,
        history_file: Optional[Path] = None
    ):
        """
        Initialize chat interface.
        
        Args:
            client: Gemini client
            display: Display handler
            clipboard: Clipboard handler
            memory: Conversation memory
            history_file: Optional file for command history
        """
        self.client = client
        self.display = display
        self.clipboard = clipboard
        self.memory = memory
        
        # Setup prompt session with history
        if history_file is None:
            history_file = Path.home() / ".local" / "share" / "gemini-cli" / "prompt_history"
            history_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Command completer
        completer = WordCompleter(list(self.COMMANDS.keys()), ignore_case=True)
        
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            enable_history_search=True
        )
        
        self.last_response = ""
        self.running = False
    
    def start(self, stream: bool = True, show_timestamps: bool = True) -> None:
        """
        Start the interactive chat session.
        
        Args:
            stream: Whether to stream responses
            show_timestamps: Whether to show message timestamps
        """
        self.running = True
        
        # Welcome message
        self.display.print_panel(
            "🤖 Gemini Chat Interface\n"
            "Type your message and press Enter\n"
            "Type /help for available commands",
            title="Welcome",
            style="green"
        )
        
        # Start chat session
        self.client.start_chat(history=self.memory.get_context_for_api())
        
        # Main loop
        while self.running:
            try:
                # Get user input
                user_input = self.session.prompt("\n[You] ❯ ")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    self._handle_command(user_input)
                    continue
                
                # Show timestamp if enabled
                if show_timestamps:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.display.print(f"[dim]({timestamp})[/dim]")
                
                # Add to memory
                self.memory.add_message("user", user_input)
                
                # Get response
                self.display.print("\n[Gemini] ", style="bold cyan", end="")
                
                if stream:
                    # Streaming response
                    self.last_response = ""
                    for chunk in self.client.send_message(user_input, stream=True):
                        self.display.console.print(chunk, end="")
                        self.last_response += chunk
                    self.display.console.print()  # New line
                else:
                    # Non-streaming response
                    with self.display.spinner("Thinking..."):
                        self.last_response = self.client.send_message(user_input, stream=False)
                    self.display.print_markdown(self.last_response)
                
                # Add response to memory
                self.memory.add_message("model", self.last_response)
                
                # Auto-save history
                self.memory.save()
                
            except KeyboardInterrupt:
                self.display.print("\n\n[yellow]Use /exit to quit[/yellow]")
                continue
            except EOFError:
                break
            except Exception as e:
                self.display.print_error(f"An error occurred: {str(e)}")
                continue
        
        self.display.print("\n[green]Goodbye! 👋[/green]")
    
    def _handle_command(self, command: str) -> None:
        """
        Handle chat commands.
        
        Args:
            command: Command string
        """
        cmd_parts = command.split(maxsplit=1)
        cmd = cmd_parts[0].lower()
        args = cmd_parts[1] if len(cmd_parts) > 1 else ""
        
        if cmd in ["/exit", "/quit"]:
            self.running = False
        
        elif cmd == "/clear":
            self.memory.clear()
            self.client.clear_history()
            self.display.clear()
            self.display.print_success("Conversation cleared")
        
        elif cmd == "/history":
            self._show_history()
        
        elif cmd == "/copy":
            self._copy_last_response()
        
        elif cmd == "/save":
            self._save_conversation()
        
        elif cmd == "/model":
            self._switch_model(args)
        
        elif cmd == "/help":
            self._show_help()
        
        else:
            self.display.print_error(f"Unknown command: {cmd}")
            self.display.print_info("Type /help for available commands")
    
    def _show_history(self) -> None:
        """Display conversation history."""
        history = self.memory.get_history(limit=20)
        
        if not history:
            self.display.print_warning("No conversation history")
            return
        
        self.display.rule("Recent Conversation History")
        
        for msg in history:
            role = "You" if msg["role"] == "user" else "Gemini"
            timestamp = msg.get("timestamp", "")
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            
            style = "green" if msg["role"] == "user" else "cyan"
            self.display.print(f"\n[bold {style}]{role}[/bold {style}]", end="")
            if timestamp:
                self.display.print(f" [dim]({timestamp})[/dim]", end="")
            self.display.print(f"\n{content}")
        
        self.display.rule()
    
    def _copy_last_response(self) -> None:
        """Copy last response to clipboard."""
        if not self.last_response:
            self.display.print_warning("No response to copy")
            return
        
        success = self.clipboard.copy(self.last_response)
        
        if success:
            self.display.print_success("Response copied to clipboard")
        else:
            fallback_file = self.clipboard.fallback_file
            self.display.print_warning(f"Saved to {fallback_file} (copy manually)")
    
    def _save_conversation(self) -> None:
        """Save conversation to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path.home() / f"gemini_conversation_{timestamp}.md"
        
        if self.memory.export_to_file(output_file):
            self.display.print_success(f"Conversation saved to {output_file}")
        else:
            self.display.print_error("Failed to save conversation")
    
    def _switch_model(self, model_arg: str) -> None:
        """
        Switch to a different model.
        
        Args:
            model_arg: Model name or number
        """
        if not model_arg:
            self._show_models()
            return
        
        # Try to find model
        models = GeminiClient.MODELS
        
        # By number
        if model_arg.isdigit():
            idx = int(model_arg) - 1
            if 0 <= idx < len(models):
                model = models[idx]
            else:
                self.display.print_error(f"Invalid model number: {model_arg}")
                return
        else:
            # By partial name
            matching = [m for m in models if model_arg.lower() in m.lower()]
            if len(matching) == 1:
                model = matching[0]
            elif len(matching) > 1:
                self.display.print_error(f"Ambiguous model: {matching}")
                return
            else:
                self.display.print_error(f"Unknown model: {model_arg}")
                return
        
        try:
            self.client.set_model(model)
            self.display.print_success(f"Switched to model: {model}")
        except Exception as e:
            self.display.print_error(f"Failed to switch model: {e}")
    
    def _show_models(self) -> None:
        """Show available models."""
        self.display.rule("Available Models")
        
        rows = []
        for i, model in enumerate(GeminiClient.MODELS, 1):
            current = "✓" if model == self.client.model_name else ""
            rows.append([str(i), model, current])
        
        self.display.print_table(["#", "Model", "Current"], rows)
        self.display.print_info("Use /model <number> or /model <name> to switch")
    
    def _show_help(self) -> None:
        """Show help message with available commands."""
        self.display.rule("Available Commands")
        
        rows = [[cmd, desc] for cmd, desc in self.COMMANDS.items()]
        self.display.print_table(["Command", "Description"], rows)
