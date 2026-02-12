# Quick Start Guide

Get up and running with Gemini CLI in under 5 minutes!

## Step 1: Install (2 minutes)

```bash
# In Termux
pkg update && pkg upgrade -y
pkg install python git termux-api -y

git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux
chmod +x install.sh
./install.sh
```

## Step 2: Get API Key (1 minute)

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 3: Configure (1 minute)

```bash
gemini-termux setup
```

Paste your API key when prompted.

## Step 4: Start Using! (30 seconds)

### Quick Question
```bash
gemini-termux ask "What is Termux?"
```

### Interactive Chat
```bash
gemini-termux chat
```

### With Image
```bash
gemini-termux chat --image screenshot.png
```

## Common Commands

```bash
# Interactive chat
gemini-termux chat

# One-off question
gemini-termux ask "your question here"

# Ask about an image
gemini-termux ask "Describe this" --image photo.jpg

# Check configuration
gemini-termux config show

# Change model
gemini-termux config set api.model gemini-1.5-pro

# Get help
gemini-termux --help
```

## Chat Commands (Inside `gemini-termux chat`)

- `/exit` - Quit chat
- `/clear` - Clear history
- `/history` - Show conversation
- `/copy` - Copy last response
- `/save` - Save conversation to file
- `/model` - Switch AI model
- `/help` - Show all commands

## Tips

✅ **Install Termux:API** for clipboard support  
✅ Use `/copy` to quickly copy responses  
✅ Try different models with `/model`  
✅ Enable streaming for real-time responses  
✅ Save important conversations with `/save`  

## Troubleshooting

**API key not working?**
```bash
export GEMINI_API_KEY="your-key-here"
```

**Command not found?**
```bash
source ~/.bashrc
# or restart Termux
```

**Clipboard not working?**
```bash
pkg install termux-api
# Also install Termux:API app from F-Droid
```

**Need help?**
```bash
gemini-termux doctor
```

## What's Next?

- Read the full [README.md](README.md)
- Check [FAQ](docs/FAQ.md) for more info
- Explore [configuration options](config.example.toml)

That's it! You're ready to go! 🚀
