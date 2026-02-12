# Frequently Asked Questions (FAQ)

## Installation & Setup

### Q: How do I install Gemini CLI on Termux?

```bash
# Quick installation
pkg install python git termux-api -y
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux
./install.sh
```

### Q: Do I need an API key?

Yes! Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey). The free tier is generous and suitable for most personal use.

### Q: Where is my API key stored?

Your API key is stored securely in `~/.config/gemini-cli/api_key` with permissions set to 0600 (owner read/write only).

### Q: Can I use environment variables instead?

Yes! Set `GEMINI_API_KEY` environment variable:

```bash
export GEMINI_API_KEY="your-key-here"
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
```

## Usage

### Q: How do I start a chat?

```bash
gemini-termux chat
```

### Q: How do I ask a quick question?

```bash
gemini-termux ask "What is the capital of France?"
```

### Q: Can I upload images?

Yes! Use the `--image` flag:

```bash
gemini-termux chat --image photo.jpg
gemini-termux ask "Describe this image" --image screenshot.png
```

### Q: What file types are supported?

- **Images**: PNG, JPG, JPEG, WEBP, GIF
- **Documents**: PDF, TXT, MD
- **Data**: CSV, JSON, XML

### Q: How do I switch models?

In chat, use `/model` command:

```bash
/model gemini-1.5-pro
```

Or configure default model:

```bash
gemini-termux config set api.model gemini-1.5-pro
```

## Features

### Q: Does clipboard work?

Yes! If you have `termux-api` installed:

```bash
pkg install termux-api
```

In chat, use `/copy` to copy the last response.

### Q: Is conversation history saved?

Yes! Conversations are automatically saved to `~/.local/share/gemini-cli/history.json`. Use `/history` in chat to view, or `/save` to export to a file.

### Q: Can I stream responses?

Yes! Streaming is enabled by default. To disable:

```bash
gemini-termux config set ui.streaming false
```

## Troubleshooting

### Q: "API key not found" error

Run the setup wizard:

```bash
gemini-termux setup
```

Or manually set your API key:

```bash
export GEMINI_API_KEY="your-key-here"
```

### Q: "Module not found" errors

Reinstall dependencies:

```bash
pip install --break-system-packages -r requirements.txt --force-reinstall
```

### Q: Clipboard not working

Install Termux-API:

```bash
pkg install termux-api
```

Also install the Termux:API app from F-Droid.

### Q: Permission denied errors

Make install script executable:

```bash
chmod +x install.sh
```

### Q: How do I check if everything is working?

Run diagnostics:

```bash
gemini-termux doctor
```

## Configuration

### Q: Where is the config file?

`~/.config/gemini-cli/config.toml`

### Q: How do I reset configuration?

```bash
gemini-termux config reset
```

### Q: Can I customize generation parameters?

Yes! Edit config file or use CLI:

```bash
gemini-termux config set generation.temperature 0.7
gemini-termux config set generation.max_output_tokens 4096
```

## Models

### Q: Which model should I use?

- **gemini-2.0-flash-exp** - Recommended for most use cases (fast, capable)
- **gemini-1.5-pro** - Most capable, best for complex tasks
- **gemini-1.5-flash** - Fast and efficient
- **gemini-1.5-flash-8b** - Lightweight, good for simple tasks

### Q: How do I see available models?

In chat mode:

```bash
/model
```

## Performance

### Q: Does it drain battery?

No! This is a Python-based CLI that's much more efficient than the Node.js version. It uses minimal resources.

### Q: Is it fast?

Yes! With streaming enabled, you get real-time responses. The CLI itself has minimal overhead.

### Q: How much storage does it use?

The installation is very lightweight:
- CLI: ~100KB
- Dependencies: ~50MB (including Rich, google-generativeai)
- Conversation history: Grows over time but limited by max_entries

## Comparison

### Q: Why not use the official @google/gemini-cli?

The official CLI doesn't work on Termux due to:
- Native module compilation failures (node-pty, keytar)
- Platform detection issues
- Clipboard problems
- Complex OAuth2 authentication

This project was built from scratch to solve all those issues.

### Q: What's different from other Gemini CLIs?

- ✅ **Native Termux support** - Built specifically for Android/Termux
- ✅ **Zero native dependencies** - Pure Python, no compilation needed
- ✅ **Better clipboard** - Direct Termux-API integration
- ✅ **Simpler auth** - Just an API key, no OAuth complexity
- ✅ **Beautiful UI** - Rich terminal interface
- ✅ **Lightweight** - Minimal resource usage

## Advanced

### Q: Can I use this in scripts?

Yes! Use the `ask` command:

```bash
answer=$(gemini-termux ask "What is 2+2?")
echo "Answer: $answer"
```

### Q: Can I batch process files?

Yes! Example:

```bash
for img in *.png; do
    gemini-termux ask "Describe this" --image "$img" >> results.txt
done
```

### Q: Is there an API wrapper?

Yes! You can import the Python modules:

```python
from gemini_cli import GeminiClient, Config, Auth

auth = Auth()
api_key = auth.get_api_key()
client = GeminiClient(api_key=api_key)
response = client.generate_content("Hello!")
```

## Getting Help

### Q: Where can I get support?

- **GitHub Issues**: [Report bugs](https://github.com/Alex72-py/gemini-cli-termux/issues)
- **Discussions**: [Ask questions](https://github.com/Alex72-py/gemini-cli-termux/discussions)
- **README**: [Documentation](https://github.com/Alex72-py/gemini-cli-termux#readme)

### Q: How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines!

### Q: Found a bug?

Please report it with:
1. Description of the issue
2. Steps to reproduce
3. Error messages
4. Your environment (Termux version, Android version)

---

**Still have questions?** [Open an issue](https://github.com/Alex72-py/gemini-cli-termux/issues/new) and we'll help!
