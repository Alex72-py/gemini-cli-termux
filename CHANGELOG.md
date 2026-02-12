# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-11

### Added
- Initial release of Gemini CLI for Termux
- Interactive chat interface with Rich UI
- One-shot question mode
- File upload support (images, PDFs, documents)
- Termux-API clipboard integration
- Conversation history management
- Multiple model support (Gemini 2.0 and 1.5 family)
- Streaming and non-streaming responses
- Configuration management via TOML files
- API key authentication with secure storage
- Setup wizard for easy onboarding
- Diagnostic tool (`doctor` command)
- Beautiful markdown rendering
- Syntax highlighting for code
- Command history with search
- Auto-save conversation sessions
- Export conversations to file
- In-chat model switching
- Zero native dependencies (pure Python)

### Features
- ✅ Pure Python implementation (no node-gyp, no native builds)
- ✅ Termux-optimized paths and permissions
- ✅ Direct Termux-API integration for clipboard
- ✅ File-based API key storage (no keychain dependency)
- ✅ Beautiful terminal UI with Rich and prompt_toolkit
- ✅ Persistent conversation history
- ✅ Support for images, PDFs, and text files
- ✅ Configurable generation parameters
- ✅ Multiple Gemini models supported
- ✅ Lightweight and battery-friendly

### Fixed
- All 135+ issues from official gemini-cli on Termux
- Native module compilation failures
- Clipboard detection issues
- Authentication complexity
- Path resolution problems
- Terminal UI issues
- File system permissions
- Android-specific limitations

## [Unreleased]

### Planned
- MCP (Model Context Protocol) server support
- Voice input/output via Termux-API
- Image generation support
- Context file (GEMINI.md) support
- Plugin system for extensions
- Multi-language support
- Conversation search functionality
- Cloud sync for conversations
- Custom themes
- Prompt templates

---

For the complete list of changes, see the [commit history](https://github.com/Alex72-py/gemini-cli-termux/commits/main).
