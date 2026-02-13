# 🤖 Gemini CLI for Termux

<div align="center">

[![Made for Termux](https://img.shields.io/badge/Made%20for-Termux-black?style=for-the-badge&logo=android)](https://termux.dev)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**A native, lightweight Gemini AI CLI built specifically for Termux on Android**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration) • [FAQ](#-faq)

</div>

---

## 📢 About This Project

This project is **inspired by** and aims to provide similar functionality to the official [Google Gemini CLI](https://github.com/google-gemini/gemini-cli), but reimagined from the ground up for **Termux on Android**.

### 🙏 Credits

- **Inspired by**: [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) - Official Gemini CLI by Google
- **Built for**: Termux community on Android
- **Purpose**: Provide a working, native solution for Android users

> **Note**: This is **NOT a fork** of the official repository. It's a complete rewrite in Python to solve Termux-specific compatibility issues. All credit for the original concept and design goes to the Google Gemini team.

---

## 🎯 Why This Exists

The official [`@google/gemini-cli`](https://github.com/google-gemini/gemini-cli) **doesn't work on Termux** due to:
- ❌ Native module compilation failures (node-pty, keytar, etc.)
- ❌ Platform detection issues (Android not recognized)
- ❌ Clipboard integration broken
- ❌ OAuth2 authentication complexity

**This project solves these issues** by building a native Python solution specifically for Termux, while maintaining the spirit and functionality of the original CLI.

---

## ✨ Features

- ✅ **Zero Native Dependencies** - Pure Python, installs instantly
- ✅ **Termux-Optimized** - Built specifically for Android/Termux environment
- ✅ **Beautiful UI** - Rich terminal interface with syntax highlighting
- ✅ **Clipboard Integration** - Direct Termux-API support
- ✅ **Conversation History** - Persistent chat sessions
- ✅ **File Analysis** - Upload images, PDFs, and documents
- ✅ **Streaming Responses** - Real-time AI output
- ✅ **Lightweight** - Minimal resource usage, battery-friendly
- ✅ **Offline Config** - No internet needed for setup

---

## 📦 Installation

### Quick Install (Recommended)

```bash
# Install dependencies
pkg update && pkg upgrade -y
pkg install python git termux-api python-grpcio python-pillow -y

# Clone repository
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux

# Run installer
chmod +x install.sh
./install.sh
```

> **Note:** The installer uses Termux packages for `grpcio` and `Pillow` to avoid compilation errors

### Manual Installation

```bash
# Install Python packages
pip install --break-system-packages -r requirements.txt

# Install packages requiring native compilation (use Termux packages)
pkg install python-grpcio python-pillow

# Install google-generativeai (requires system grpcio)
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf

# Install CLI
pip install --break-system-packages -e .

# Setup
gemini-termux setup
```

---

## 🚀 Quick Start

### 1. Get Your API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy your API key

### 2. Configure

```bash
# Run setup wizard
gemini-termux setup

# Or set manually
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Start Chatting

```bash
# Interactive chat mode
gemini-termux chat

# Quick question
gemini-termux ask "What is Termux?"

# Analyze an image
gemini-termux chat --image screenshot.png
```

---

## 📖 Usage

### Interactive Chat

```bash
gemini-termux chat
```

**Commands in chat mode:**
- `/exit` or `/quit` - Exit chat
- `/clear` - Clear conversation history
- `/history` - Show conversation history
- `/copy` - Copy last response to clipboard
- `/save` - Save conversation to file
- `/model <name>` - Switch model
- `/help` - Show all commands

### One-Shot Questions

```bash
# Simple question
gemini-termux ask "Explain quantum computing"

# With file input
gemini-termux ask "What's in this image?" --image photo.jpg

# Stream response
gemini-termux ask "Write a story" --stream
```

### File Analysis

```bash
# Analyze image
gemini-termux chat --image screenshot.png

# Multiple files
gemini-termux chat --file document.pdf --file data.csv

# Supported: PNG, JPG, WEBP, PDF, TXT, CSV, JSON
```

### Configuration

```bash
# View current config
gemini-termux config show

# Set model
gemini-termux config set model gemini-2.0-flash-exp

# Set temperature
gemini-termux config set temperature 0.7

# Reset to defaults
gemini-termux config reset
```

---

## ⚙️ Configuration

### Config File Location

```
~/.config/gemini-cli/config.toml
```

### Example Configuration

```toml
[api]
model = "gemini-2.0-flash-exp"
timeout = 60

[generation]
temperature = 0.9
top_p = 0.95
top_k = 40
max_output_tokens = 8192

[ui]
theme = "monokai"
syntax_highlighting = true
show_timestamps = true
streaming = true

[history]
enabled = true
max_entries = 1000
auto_save = true

[clipboard]
use_termux_api = true
```

### Available Models

- `gemini-2.0-flash-exp` - Fast, multimodal (Recommended)
- `gemini-2.0-flash-thinking-exp` - Advanced reasoning
- `gemini-1.5-pro` - Most capable
- `gemini-1.5-flash` - Fast & efficient
- `gemini-1.5-flash-8b` - Lightweight

---

## 🔧 Advanced Usage

### Environment Variables

```bash
# API Configuration
export GEMINI_API_KEY="your-key"
export GEMINI_MODEL="gemini-2.0-flash-exp"

# Behavior
export GEMINI_STREAMING=true
export GEMINI_DEBUG=false
```

### Batch Processing

```bash
# Process multiple questions
cat questions.txt | while read question; do
    gemini-termux ask "$question" >> answers.txt
done

# Analyze all images
for img in *.png; do
    gemini-termux ask "Describe this" --image "$img"
done
```

---

## 🛠️ Troubleshooting

### Common Issues

**"API key not found"**
```bash
export GEMINI_API_KEY="your-key-here"
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
```

**"Clipboard not working"**
```bash
pkg install termux-api
```

**"Module not found"**
```bash
pip install --break-system-packages -r requirements.txt --force-reinstall
```

### Debug Mode

```bash
gemini-termux --debug chat
gemini-termux doctor  # Check installation
```

---

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Google Gemini Team](https://github.com/google-gemini)** - For creating the original Gemini CLI and the amazing Gemini API
- **[Official Gemini CLI](https://github.com/google-gemini/gemini-cli)** - Inspiration for features and design
- **Termux community** - For making Android development possible
- All contributors to this project

### Differences from Official CLI

This is a **complete rewrite** designed specifically for Termux:

| Feature | Official CLI | This Project |
|---------|-------------|--------------|
| **Platform** | Node.js | Python |
| **Native Deps** | Yes (node-pty, keytar) | None (pure Python) |
| **Installation** | npm (requires compilation) | pip (instant) |
| **Authentication** | OAuth2 + Keychain | API Key + File |
| **Clipboard** | clipboardy (broken) | Termux-API (native) |
| **Termux Support** | ❌ Broken | ✅ Native |
| **File Size** | ~200MB+ | ~50MB |

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Alex72-py/gemini-cli-termux/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Alex72-py/gemini-cli-termux/discussions)

---

<div align="center">

**Made with ❤️ for the Termux community**

[⬆ Back to Top](#-gemini-cli-for-termux)

</div>
