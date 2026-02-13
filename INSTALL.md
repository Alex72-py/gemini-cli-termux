# Installation Guide

## Prerequisites

### Required
- **Termux** - Install from [F-Droid](https://f-droid.org/packages/com.termux/)
- **Android 7.0+** - Minimum Android version
- **Storage**: ~100MB free space

### Recommended
- **Termux:API** - For clipboard integration ([F-Droid](https://f-droid.org/packages/com.termux.api/))

---

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Update Termux
pkg update && pkg upgrade -y

# Install dependencies (CRITICAL: includes python-grpcio and python-pillow)
pkg install python git termux-api python-grpcio python-pillow -y

# Clone repository
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux

# Run installer
chmod +x install.sh
./install.sh
```

**Important**: The installer uses pre-compiled Termux packages for native libraries:
- `python-grpcio` - Required by google-generativeai (won't compile via pip)
- `python-pillow` - Image processing library (won't compile via pip)

The installer will:
- ✅ Check environment
- ✅ Install Python packages
- ✅ Install google-generativeai with system grpcio
- ✅ Set up CLI commands
- ✅ Run diagnostics
- ✅ Launch setup wizard

---

### Method 2: Download Archive

If you can't use git, download the project as an archive:

#### Option A: Using wget
```bash
# Download
wget https://github.com/Alex72-py/gemini-cli-termux/archive/refs/heads/main.zip

# Extract
unzip main.zip
cd gemini-cli-termux-main

# Install
chmod +x install.sh
./install.sh
```

#### Option B: Using curl
```bash
# Download
curl -L -o gemini-cli-termux.zip https://github.com/Alex72-py/gemini-cli-termux/archive/refs/heads/main.zip

# Extract
unzip gemini-cli-termux.zip
cd gemini-cli-termux-main

# Install
chmod +x install.sh
./install.sh
```

#### Option C: Manual Browser Download
1. Visit: https://github.com/Alex72-py/gemini-cli-termux
2. Click green "Code" button
3. Select "Download ZIP"
4. Open Termux and navigate to Downloads:
   ```bash
   cd ~/storage/downloads  # May need: termux-setup-storage first
   unzip gemini-cli-termux-main.zip
   cd gemini-cli-termux-main
   chmod +x install.sh
   ./install.sh
   ```

---

### Method 3: Manual Installation

If the installer fails, install manually:

```bash
# 1. Install system packages (CRITICAL: python-grpcio and python-pillow from pkg)
pkg update && pkg upgrade -y
pkg install python git termux-api python-grpcio python-pillow -y

# 2. Clone or download project
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux

# 3. Install Python dependencies (Pillow and google-generativeai excluded)
pip install --break-system-packages -r requirements.txt

# 4. Install google-generativeai (uses system grpcio)
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf

# 5. Install CLI
pip install --break-system-packages -e .

# 6. Verify installation
gemini-termux --version

# 7. Run setup
gemini-termux setup
```

**Why this process?**
- `grpcio` (needed by google-generativeai) won't compile via pip on Termux
- `Pillow` (image processing) won't compile via pip on Termux
- We install both as pre-compiled packages from Termux repos
- Then install other packages normally via pip

---

### Method 4: From PyPI (When Available)

Once published to PyPI:

```bash
pip install --break-system-packages gemini-cli-termux
gemini-termux setup
```

---

## Post-Installation

### 1. Setup API Key

Run the setup wizard:
```bash
gemini-termux setup
```

Or manually set your API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
```

Get your API key from: https://aistudio.google.com/app/apikey

### 2. Test Installation

```bash
# Check installation
gemini-termux doctor

# Test with a question
gemini-termux ask "Hello, how are you?"

# Start interactive chat
gemini-termux chat
```

### 3. Optional: Install Termux:API

For full clipboard support:

1. Install **Termux:API** app from F-Droid: https://f-droid.org/packages/com.termux.api/
2. In Termux, run:
   ```bash
   pkg install termux-api
   ```

---

## Troubleshooting Installation

### "Permission denied" on install.sh
```bash
chmod +x install.sh
```

### "Command not found: gemini-termux"
```bash
# Restart Termux or source bashrc
source ~/.bashrc

# Or use full path
~/.local/bin/gemini-termux
```

### Python package installation fails
```bash
# Upgrade pip first
pip install --upgrade pip --break-system-packages

# If grpcio fails:
# DO NOT use pip for grpcio on Termux!
pkg install python-grpcio

# Then install google-generativeai
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf

# Install other dependencies
pip install --break-system-packages rich prompt-toolkit httpx toml Pillow PyPDF2
```

### "Failed building wheel for grpcio"
This is a common error. **Solution:**

```bash
# NEVER use pip for grpcio on Termux
# Use Termux package manager instead:
pkg install python-grpcio

# Verify it's installed
python -c "import grpc; print(grpc.__version__)"
```

### "Failed building wheel for Pillow"
Another common compilation error. **Solution:**

```bash
# NEVER use pip for Pillow on Termux
# Use Termux package manager instead:
pkg install python-pillow

# Verify it's installed
python -c "from PIL import Image; print('Pillow OK')"
```

### "ERROR: Could not build wheels for Pillow"
Same as above. Pillow requires native C libraries that fail to compile on Termux.

```bash
pkg install python-pillow
```

### "pkg: command not found"
You're not in Termux. This only works in the Termux app on Android.

### Storage permission errors
```bash
# Grant storage access
termux-setup-storage
```

### Git clone fails
Try these alternatives:
1. Use wget/curl to download ZIP (see Method 2)
2. Download manually from browser (see Method 2, Option C)
3. Check your internet connection

---

## Updating

### Update from Git
```bash
cd gemini-cli-termux
git pull origin main
pip install --break-system-packages -e . --force-reinstall
```

### Manual Update
1. Delete old directory
2. Download new version
3. Reinstall using any method above

---

## Uninstalling

### Remove CLI
```bash
pip uninstall gemini-cli-termux
```

### Remove All Data
```bash
# Remove configuration
rm -rf ~/.config/gemini-cli

# Remove data (history)
rm -rf ~/.local/share/gemini-cli

# Remove cache
rm -rf ~/.cache/gemini-cli
```

---

## Verification

After installation, verify everything works:

```bash
# 1. Check version
gemini-termux --version

# 2. Run diagnostics
gemini-termux doctor

# 3. Test basic functionality
gemini-termux ask "What is 2+2?"
```

Expected output:
```
✓ API key found
✓ Config file: ~/.config/gemini-cli/config.toml
✓ Termux-API available
✅ All checks passed!
```

---

## Getting Help

If installation fails:

1. **Check diagnostics**: `gemini-termux doctor`
2. **Read FAQ**: [docs/FAQ.md](docs/FAQ.md)
3. **Report issue**: https://github.com/Alex72-py/gemini-cli-termux/issues

Include:
- Error messages
- Termux version: `termux-info`
- Android version
- Installation method used

---

## Next Steps

Once installed:

1. Read the [README.md](README.md) for usage instructions
2. Check the [FAQ](docs/FAQ.md) for common questions
3. Try some examples:
   ```bash
   gemini-termux chat
   gemini-termux ask "Explain quantum computing"
   gemini-termux config show
   ```

Happy chatting! 🤖
