"""
Main CLI entry point for Gemini Termux.
Handles command-line interface and argument parsing.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

from gemini_cli import __version__
from gemini_cli.core import Auth, Config, GeminiClient
from gemini_cli.ui import Display, ChatInterface
from gemini_cli.utils import Clipboard, FileHandler, ConversationMemory


def setup_command(args, config: Config, auth: Auth, display: Display) -> int:
    """
    Run initial setup wizard.
    
    Args:
        args: Command arguments
        config: Config manager
        auth: Auth manager
        display: Display handler
        
    Returns:
        Exit code
    """
    display.print_panel(
        "🚀 Welcome to Gemini CLI for Termux!\n\n"
        "Let's get you set up in a few steps.",
        title="Setup Wizard",
        style="green"
    )
    
    # Check for existing API key
    existing_key = auth.get_api_key()
    if existing_key:
        display.print_warning("API key already configured")
        response = input("Do you want to replace it? (y/N): ").strip().lower()
        if response != "y":
            display.print_info("Setup cancelled")
            return 0
    
    # Get API key
    display.print("\n[bold]Step 1: API Key[/bold]")
    display.print("Get your API key from: https://aistudio.google.com/app/apikey")
    
    while True:
        api_key = input("\nEnter your API key: ").strip()
        
        if not api_key:
            display.print_error("API key cannot be empty")
            continue
        
        if not auth.validate_api_key(api_key):
            display.print_error("Invalid API key format")
            retry = input("Try again? (Y/n): ").strip().lower()
            if retry == "n":
                return 1
            continue
        
        # Save API key
        if auth.save_api_key(api_key):
            display.print_success("API key saved securely")
            break
        else:
            display.print_error("Failed to save API key")
            return 1
    
    # Configure model
    display.print("\n[bold]Step 2: Default Model[/bold]")
    display.print("Available models:")
    for i, model in enumerate(GeminiClient.MODELS, 1):
        display.print(f"  {i}. {model}")
    
    model_choice = input("\nChoose model (default: 1): ").strip() or "1"
    try:
        model_idx = int(model_choice) - 1
        if 0 <= model_idx < len(GeminiClient.MODELS):
            model = GeminiClient.MODELS[model_idx]
            config.set("api", "model", model)
            display.print_success(f"Model set to: {model}")
        else:
            display.print_warning("Invalid choice, using default")
    except ValueError:
        display.print_warning("Invalid input, using default")
    
    # Streaming preference
    display.print("\n[bold]Step 3: Streaming Responses[/bold]")
    streaming = input("Enable streaming responses? (Y/n): ").strip().lower() != "n"
    config.set("ui", "streaming", streaming)
    
    # Save configuration
    if config.save():
        display.print_success("Configuration saved")
    else:
        display.print_error("Failed to save configuration")
        return 1
    
    # Done!
    display.print_panel(
        "✅ Setup complete!\n\n"
        "Try these commands:\n"
        "  • gemini-termux chat         - Start interactive chat\n"
        "  • gemini-termux ask \"...\"  - Quick question\n"
        "  • gemini-termux --help       - Show all commands",
        title="All Set!",
        style="green"
    )
    
    return 0


def chat_command(args, client: GeminiClient, config: Config, display: Display) -> int:
    """
    Start interactive chat session.
    
    Args:
        args: Command arguments
        client: Gemini client
        config: Config manager
        display: Display handler
        
    Returns:
        Exit code
    """
    # Initialize components
    clipboard = Clipboard(use_termux_api=config.clipboard.use_termux_api)
    memory = ConversationMemory(
        data_dir=config.data_dir,
        max_entries=config.history.max_entries
    )
    
    # Create chat interface
    chat = ChatInterface(client, display, clipboard, memory)
    
    # Handle file inputs
    if args.image or args.file:
        files = []
        if args.image:
            files.extend([Path(f) for f in args.image])
        if args.file:
            files.extend([Path(f) for f in args.file])
        
        # Validate files
        valid_files = []
        for file_path in files:
            if not FileHandler.validate_file(file_path):
                display.print_error(f"Invalid or unsupported file: {file_path}")
                continue
            valid_files.append(file_path)
        
        if valid_files:
            display.print_info(f"Loaded {len(valid_files)} file(s)")
            # TODO: Add files to first message
    
    # Start chat
    try:
        chat.start(
            stream=config.ui.streaming,
            show_timestamps=config.ui.show_timestamps
        )
        return 0
    except KeyboardInterrupt:
        display.print("\n[yellow]Chat interrupted[/yellow]")
        return 130
    except Exception as e:
        display.print_error(f"Chat error: {e}")
        return 1


def ask_command(args, client: GeminiClient, config: Config, display: Display) -> int:
    """
    Ask a single question.
    
    Args:
        args: Command arguments
        client: Gemini client
        config: Config manager
        display: Display handler
        
    Returns:
        Exit code
    """
    question = args.question
    
    # Handle file inputs
    files = []
    if args.image:
        files.extend([Path(f) for f in args.image])
    if args.file:
        files.extend([Path(f) for f in args.file])
    
    # Validate files
    valid_files = []
    for file_path in files:
        if not FileHandler.validate_file(file_path):
            display.print_error(f"Invalid or unsupported file: {file_path}")
            continue
        valid_files.append(file_path)
    
    try:
        if valid_files:
            # With files
            if args.stream:
                for chunk in client.send_message_with_files(question, valid_files, stream=True):
                    display.console.print(chunk, end="")
                display.console.print()
            else:
                response = client.send_message_with_files(question, valid_files, stream=False)
                display.print_markdown(response)
        else:
            # Text only
            if args.stream:
                for chunk in client.generate_content(question, stream=True):
                    display.console.print(chunk, end="")
                display.console.print()
            else:
                response = client.generate_content(question, stream=False)
                display.print_markdown(response)
        
        return 0
    except Exception as e:
        display.print_error(f"Error: {e}")
        return 1


def config_command(args, config: Config, display: Display) -> int:
    """
    Manage configuration.
    
    Args:
        args: Command arguments
        config: Config manager
        display: Display handler
        
    Returns:
        Exit code
    """
    if args.config_action == "show":
        # Show current config
        display.print_panel(
            f"Configuration file: {config.config_file}\n\n"
            f"Model: {config.api.model}\n"
            f"Streaming: {config.ui.streaming}\n"
            f"History: {config.history.enabled}\n"
            f"Clipboard: {config.clipboard.use_termux_api}",
            title="Current Configuration"
        )
        return 0
    
    elif args.config_action == "set":
        if not args.key or not args.value:
            display.print_error("Usage: config set <section.key> <value>")
            return 1
        
        try:
            section, key = args.key.split(".", 1)
            config.set(section, key, args.value)
            config.save()
            display.print_success(f"Set {args.key} = {args.value}")
            return 0
        except ValueError:
            display.print_error("Invalid key format. Use: section.key")
            return 1
    
    elif args.config_action == "reset":
        config.reset()
        display.print_success("Configuration reset to defaults")
        return 0
    
    return 0


def doctor_command(args, config: Config, auth: Auth, display: Display) -> int:
    """
    Run diagnostics to check installation.
    
    Args:
        args: Command arguments
        config: Config manager
        auth: Auth manager
        display: Display handler
        
    Returns:
        Exit code
    """
    display.print_panel("🔍 Running Diagnostics...", style="cyan")
    
    issues = []
    
    # Check API key
    display.print("\n[bold]1. API Key[/bold]")
    if auth.is_authenticated():
        display.print_success("API key found")
    else:
        display.print_error("No API key configured")
        issues.append("Run 'gemini-termux setup' to configure API key")
    
    # Check config
    display.print("\n[bold]2. Configuration[/bold]")
    if config.config_file.exists():
        display.print_success(f"Config file: {config.config_file}")
    else:
        display.print_warning("No config file (using defaults)")
    
    # Check Termux-API
    display.print("\n[bold]3. Termux-API[/bold]")
    clipboard = Clipboard()
    if clipboard.has_termux_api:
        display.print_success("Termux-API available")
    else:
        display.print_warning("Termux-API not installed")
        issues.append("Install with: pkg install termux-api")
    
    # Check directories
    display.print("\n[bold]4. Directories[/bold]")
    for name, path in [
        ("Config", config.config_dir),
        ("Cache", config.cache_dir),
        ("Data", config.data_dir),
    ]:
        if path.exists():
            display.print_success(f"{name}: {path}")
        else:
            display.print_warning(f"{name}: {path} (will be created)")
    
    # Summary
    if issues:
        display.print("\n[bold yellow]⚠ Issues Found:[/bold yellow]")
        for issue in issues:
            display.print(f"  • {issue}")
        return 1
    else:
        display.print("\n[bold green]✅ All checks passed![/bold green]")
        return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="gemini-termux",
        description="Native Gemini AI CLI for Termux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  gemini-termux setup                    # Run initial setup
  gemini-termux chat                     # Start interactive chat
  gemini-termux ask "What is Termux?"    # Quick question
  gemini-termux chat --image photo.jpg   # Chat with image
        """
    )
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    subparsers.add_parser("setup", help="Run initial setup wizard")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start interactive chat")
    chat_parser.add_argument("--image", "-i", action="append", help="Image file to analyze")
    chat_parser.add_argument("--file", "-f", action="append", help="File to include")
    
    # Ask command
    ask_parser = subparsers.add_parser("ask", help="Ask a single question")
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument("--image", "-i", action="append", help="Image file to analyze")
    ask_parser.add_argument("--file", "-f", action="append", help="File to include")
    ask_parser.add_argument("--stream", "-s", action="store_true", help="Stream response")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("config_action", choices=["show", "set", "reset"],
                              help="Configuration action")
    config_parser.add_argument("key", nargs="?", help="Config key (section.key)")
    config_parser.add_argument("value", nargs="?", help="Config value")
    
    # Doctor command
    subparsers.add_parser("doctor", help="Run diagnostics")
    
    args = parser.parse_args()
    
    # Initialize core components
    config = Config()
    auth = Auth(config.config_dir)
    display = Display(theme=config.ui.theme if hasattr(config.ui, "theme") else "monokai")
    
    # Handle commands
    if args.command == "setup":
        return setup_command(args, config, auth, display)
    
    elif args.command == "doctor":
        return doctor_command(args, config, auth, display)
    
    elif args.command == "config":
        return config_command(args, config, display)
    
    # Commands that require API key
    elif args.command in ["chat", "ask"]:
        api_key = auth.get_api_key()
        if not api_key:
            display.print_error("API key not configured")
            display.print_info("Run 'gemini-termux setup' to get started")
            return 1
        
        # Initialize client
        try:
            client = GeminiClient(
                api_key=api_key,
                model=config.api.model,
                temperature=config.generation.temperature,
                top_p=config.generation.top_p,
                top_k=config.generation.top_k,
                max_output_tokens=config.generation.max_output_tokens,
            )
        except Exception as e:
            display.print_error(f"Failed to initialize client: {e}")
            return 1
        
        if args.command == "chat":
            return chat_command(args, client, config, display)
        elif args.command == "ask":
            return ask_command(args, client, config, display)
    
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(130)
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        sys.exit(1)
