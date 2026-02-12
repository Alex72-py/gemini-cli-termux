# Project Structure

## Overview

**Gemini CLI for Termux** - A production-ready, native Python CLI for Google's Gemini AI, specifically built for Termux on Android.

- **Total Python Code**: ~1,891 lines
- **Files**: 24 files
- **License**: MIT
- **Author**: Alex72-py

## Directory Structure

```
gemini-cli-termux/
├── gemini_cli/                  # Main package
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # CLI entry point (450+ lines)
│   │
│   ├── core/                   # Core functionality
│   │   ├── __init__.py
│   │   ├── auth.py             # API key authentication
│   │   ├── client.py           # Gemini API client
│   │   └── config.py           # Configuration management
│   │
│   ├── ui/                     # User interface
│   │   ├── __init__.py
│   │   ├── chat.py             # Interactive chat interface
│   │   └── display.py          # Terminal output formatting
│   │
│   ├── utils/                  # Utilities
│   │   ├── __init__.py
│   │   ├── clipboard.py        # Termux clipboard integration
│   │   ├── files.py            # File handling
│   │   └── memory.py           # Conversation history
│   │
│   └── tools/                  # Tools & integrations
│       └── __init__.py         # (Reserved for future MCP support)
│
├── tests/                      # Test suite
│   ├── __init__.py
│   └── test_basic.py          # Basic unit tests
│
├── docs/                       # Documentation
│   └── FAQ.md                 # Frequently Asked Questions
│
├── setup.py                    # Package setup configuration
├── requirements.txt            # Python dependencies
├── install.sh                  # Termux installation script
├── config.example.toml         # Example configuration
│
├── README.md                   # Main documentation
├── LICENSE                     # MIT License
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── MANIFEST.in                # Package manifest
└── .gitignore                 # Git ignore rules
```

## Module Breakdown

### Core Modules (`gemini_cli/core/`)

#### auth.py
- **Purpose**: API key authentication and secure storage
- **Features**:
  - Environment variable support (`GEMINI_API_KEY`)
  - File-based secure storage (`~/.config/gemini-cli/api_key`)
  - Permission management (0600)
  - Basic API key validation

#### client.py
- **Purpose**: Gemini API interaction wrapper
- **Features**:
  - Multi-model support (Gemini 2.0 & 1.5 families)
  - Chat session management
  - File upload support (images, PDFs, documents)
  - Streaming and non-streaming responses
  - Generation parameter configuration
  - Conversation history tracking

#### config.py
- **Purpose**: Configuration management via TOML
- **Features**:
  - Termux-aware path handling
  - Default configuration
  - TOML file parsing
  - Dataclass-based settings
  - Save/load/reset functionality

### UI Modules (`gemini_cli/ui/`)

#### display.py
- **Purpose**: Rich terminal output formatting
- **Features**:
  - Markdown rendering
  - Syntax highlighting for code
  - Panels and tables
  - Colored output (success, error, warning, info)
  - Progress spinners
  - Terminal clearing and rules

#### chat.py
- **Purpose**: Interactive chat interface
- **Features**:
  - Prompt with history and auto-suggest
  - Command system (`/exit`, `/copy`, `/save`, etc.)
  - Model switching
  - Conversation history viewing
  - Clipboard integration
  - Export to file
  - Streaming support
  - Timestamp display

### Utils Modules (`gemini_cli/utils/`)

#### clipboard.py
- **Purpose**: Termux-API clipboard integration
- **Features**:
  - Termux-API detection
  - Copy/paste/clear operations
  - Fallback file-based clipboard
  - UTF-8 support

#### files.py
- **Purpose**: File handling and validation
- **Features**:
  - Supported file type detection
  - MIME type mapping
  - File validation
  - File size formatting
  - Multi-format support (images, PDFs, documents)

#### memory.py
- **Purpose**: Conversation history management
- **Features**:
  - JSON-based persistent storage
  - Message addition with timestamps
  - History limiting (max_entries)
  - Export to markdown
  - API-formatted context retrieval

### Main Entry Point (`gemini_cli/main.py`)

#### Commands
1. **setup** - Initial configuration wizard
2. **chat** - Interactive chat session
3. **ask** - One-shot questions
4. **config** - Configuration management (show/set/reset)
5. **doctor** - Installation diagnostics

#### Features
- Argument parsing with argparse
- Environment checks
- Error handling
- Multiple file input support
- Debug mode

## Installation

### install.sh
- **Purpose**: Automated Termux installation
- **Features**:
  - Termux environment validation
  - Package installation (python, git, termux-api)
  - Python dependency installation
  - CLI installation in development mode
  - Permissions setup
  - Diagnostic verification
  - Setup wizard launcher
  - Colored output

## Configuration

### Default Paths (Termux-aware)
```
Config:  ~/.config/gemini-cli/
         ├── config.toml      # User configuration
         └── api_key          # Secure API key storage

Cache:   ~/.cache/gemini-cli/

Data:    ~/.local/share/gemini-cli/
         ├── history.json     # Conversation history
         └── prompt_history   # Command history
```

### Configuration Sections
1. **[api]** - API settings (model, timeout)
2. **[generation]** - Generation parameters (temperature, top_p, top_k, max_tokens)
3. **[ui]** - UI preferences (theme, highlighting, timestamps, streaming)
4. **[history]** - History settings (enabled, max_entries, auto_save)
5. **[clipboard]** - Clipboard configuration (use_termux_api, auto_copy_code)

## Dependencies

### Runtime Dependencies
```
google-generativeai >= 0.8.0   # Gemini API client
rich >= 13.7.0                  # Terminal UI
prompt-toolkit >= 3.0.43        # Interactive prompts
httpx >= 0.27.0                 # HTTP client
toml >= 0.10.2                  # Config parsing
Pillow >= 10.3.0                # Image processing
PyPDF2 >= 3.0.1                 # PDF processing
python-dateutil >= 2.9.0        # Date utilities
aiofiles >= 23.2.1              # Async file I/O
```

### Development Dependencies
```
pytest >= 7.4.0                 # Testing framework
pytest-asyncio >= 0.21.0        # Async testing
black >= 23.0.0                 # Code formatting
isort >= 5.12.0                 # Import sorting
flake8 >= 6.0.0                 # Linting
mypy >= 1.4.0                   # Type checking
```

## Testing

### Test Coverage
- Authentication (save, load, delete API keys)
- Configuration (defaults, get/set, persistence)
- File handling (validation, MIME types, size formatting)
- Clipboard (creation, fallback)

### Run Tests
```bash
python -m pytest tests/ -v
```

## Key Features

### What Makes This Different
1. **Zero Native Dependencies** - Pure Python, no compilation
2. **Termux-Optimized** - Built specifically for Android/Termux
3. **Simple Authentication** - API key only, no OAuth complexity
4. **Direct Clipboard** - Native Termux-API integration
5. **Beautiful UI** - Rich terminal interface
6. **Lightweight** - Minimal resource usage (~50MB with deps)
7. **Production-Ready** - Complete error handling, logging, diagnostics

### Solved Problems
- ❌ **node-pty** - Eliminated (Python-based)
- ❌ **keytar** - Eliminated (file-based storage)
- ❌ **clipboardy** - Replaced (direct Termux-API)
- ❌ **OAuth2** - Eliminated (API key auth)
- ❌ **Platform detection** - Fixed (Termux-aware paths)
- ❌ **Native builds** - Eliminated (pure Python)

## Development

### Code Style
- PEP 8 compliant
- Type hints where appropriate
- Docstrings for all public functions
- Modular architecture
- Clear separation of concerns

### Adding Features
1. Create module in appropriate package
2. Update `__init__.py` exports
3. Add tests in `tests/`
4. Update documentation
5. Add to CHANGELOG.md

## Deployment

### As Package
```bash
# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI (when ready)
twine upload dist/*
```

### Direct Installation
```bash
# From source
pip install --break-system-packages -e .

# From GitHub
pip install --break-system-packages git+https://github.com/Alex72-py/gemini-cli-termux.git
```

## Future Enhancements

### Planned Features
- MCP (Model Context Protocol) server support
- Voice input/output via Termux-API (TTS/STT)
- Image generation support
- Context file (GEMINI.md) support
- Plugin system for extensions
- Multi-language support
- Conversation search functionality
- Cloud sync for conversations
- Custom themes
- Prompt templates
- Batch processing utilities
- Web UI option

### Performance Optimizations
- Response caching
- Conversation compression
- Lazy loading of large histories
- Memory usage optimization
- Battery usage profiling

## Metrics

- **Code**: ~1,891 lines of Python
- **Modules**: 12 Python modules
- **Commands**: 5 main commands
- **Chat Commands**: 7 in-chat commands
- **Supported Models**: 5 Gemini models
- **File Types**: 9 supported formats
- **Config Options**: 13 settings
- **Installation Time**: ~2 minutes
- **Disk Usage**: ~50MB with dependencies

---

**Ready to use! 🚀**

See [README.md](README.md) for usage instructions.
