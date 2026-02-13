# Troubleshooting Guide

## Common Installation Issues

### 🔴 "Failed building wheel for grpcio" (MOST COMMON)

**Error Message:**
```
ERROR: Failed building wheel for grpcio
Command '/data/data/com.termux/files/usr/bin/aarch64-linux-android-clang' failed
```

**Problem:**
- `google-generativeai` requires `grpcio`
- `grpcio` needs C++ compilation
- Compilation fails on Termux/Android

**✅ SOLUTION:**

```bash
# DO NOT use pip for grpcio!
# Use Termux's pre-compiled package:

pkg install python-grpcio

# Then install google-generativeai WITHOUT rebuilding grpcio:
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf

# Verify it works:
python -c "import grpc; print('grpcio:', grpc.__version__)"
python -c "import google.generativeai as genai; print('google-generativeai: OK')"
```

---

### 🔴 "Failed building wheel for Pillow" (VERY COMMON)

**Error Message:**
```
ERROR: Failed building wheel for Pillow
error: subprocess-exited-with-error
× Building wheel for Pillow (pyproject.toml) did not run successfully.
```

**Problem:**
- `Pillow` is an image processing library
- Requires compilation of C extensions (libjpeg, libpng, etc.)
- Compilation fails on Termux/Android

**✅ SOLUTION:**

```bash
# DO NOT use pip for Pillow!
# Use Termux's pre-compiled package:

pkg install python-pillow

# Verify it works:
python -c "from PIL import Image; print('Pillow: OK')"
```

---

### 🔴 "Failed to build 'cryptography' when installing build dependencies" (COMMON)

**Error Message:**
```
ERROR: Failed to build 'cryptography' when installing build dependencies for cryptography
Rust not found, installing into a temporary directory
Unsupported platform: 312
```

**Problem:**
- `cryptography` is a Rust-based cryptographic library
- Requires Rust compiler + native compilation
- Compilation fails on Termux/Android

**✅ SOLUTION:**

```bash
# DO NOT use pip for cryptography!
# Use Termux's pre-compiled package:

pkg install python-cryptography

# Verify it works:
python -c "import cryptography; print('cryptography: OK')"
```

---

### 🔴 "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
# Install with special handling for grpcio:
pkg install python-grpcio
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf
```

---

### 🔴 "API key not found"

**Solution 1: Environment Variable**
```bash
export GEMINI_API_KEY="your-api-key-here"

# Make it permanent:
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

**Solution 2: Run Setup**
```bash
gemini-termux setup
```

---

### 🔴 "Command not found: gemini-termux"

**Solution:**
```bash
# Option 1: Restart Termux or source bashrc
source ~/.bashrc

# Option 2: Use full path
~/.local/bin/gemini-termux

# Option 3: Reinstall
pip install --break-system-packages -e . --force-reinstall
```

---

### 🔴 Clipboard not working

**Problem:** Clipboard operations fail or show warnings.

**Solution:**
```bash
# 1. Install Termux:API app from F-Droid
#    https://f-droid.org/packages/com.termux.api/

# 2. Install termux-api package
pkg install termux-api

# 3. Test clipboard
echo "test" | termux-clipboard-set
termux-clipboard-get

# 4. If still not working, clipboard will fall back to file
#    Check: ~/.gemini_clipboard.txt
```

---

### 🔴 "Permission denied" errors

**Solution:**
```bash
# Make install script executable
chmod +x install.sh

# Fix CLI permissions
chmod 755 ~/.local/bin/gemini-termux
```

---

### 🔴 Pillow (PIL) installation fails

**Error:** `"jpeg support not available"`

**Solution:**
```bash
pkg install libjpeg-turbo libpng
pip install --break-system-packages Pillow --force-reinstall
```

---

### 🔴 "Killed" during installation

**Problem:** Termux kills process due to memory usage.

**Solution:**
```bash
# Install dependencies one by one
pip install --break-system-packages rich
pip install --break-system-packages prompt-toolkit
pip install --break-system-packages httpx
pip install --break-system-packages toml
pip install --break-system-packages Pillow
pip install --break-system-packages PyPDF2
pip install --break-system-packages python-dateutil
pip install --break-system-packages aiofiles

# Then install google-generativeai
pkg install python-grpcio
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf
```

---

## Verification Steps

After fixing issues, verify installation:

```bash
# 1. Check CLI is installed
gemini-termux --version

# 2. Run diagnostics
gemini-termux doctor

# 3. Test imports
python << EOF
import grpc
import google.generativeai as genai
import rich
import prompt_toolkit
print("✓ All core dependencies working!")
EOF

# 4. Test CLI
gemini-termux ask "Hello, are you working?"
```

---

## Complete Reinstall

If everything fails, start fresh:

```bash
# 1. Remove old installation
pip uninstall -y gemini-cli-termux
rm -rf ~/.config/gemini-cli
rm -rf ~/.local/share/gemini-cli
rm -rf ~/.cache/gemini-cli

# 2. Clean Python cache
rm -rf ~/.local/lib/python3.*/site-packages/gemini_cli*

# 3. Reinstall system dependencies
pkg update && pkg upgrade -y
pkg install python git termux-api python-grpcio python-pillow python-cryptography -y

# 4. Clone fresh copy
cd ~
rm -rf gemini-cli-termux
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux

# 5. Run installer
chmod +x install.sh
./install.sh
```

---

## Debug Mode

Enable detailed logging:

```bash
# Run with debug flag
gemini-termux --debug chat

# Check logs
ls -la ~/.cache/gemini-cli/

# Test Python imports
python -vv -c "import google.generativeai"
```

---

## Platform-Specific Issues

### Android Version < 7.0
Not supported. Termux requires Android 7.0+.

### ARM32 (armv7)
May have additional compilation issues. ARM64 (aarch64) recommended.

### Rooted Devices
Should work normally. No special handling needed.

---

## Still Having Issues?

1. **Check Termux version:**
   ```bash
   termux-info
   ```

2. **Check Python version:**
   ```bash
   python --version  # Should be 3.11+
   ```

3. **Check available storage:**
   ```bash
   df -h $HOME
   ```

4. **Report issue:**
   - Go to: https://github.com/Alex72-py/gemini-cli-termux/issues
   - Include:
     - Error messages
     - `termux-info` output
     - Installation method used
     - Steps to reproduce

---

## Quick Reference

### Essential Commands
```bash
# Install ALL native libraries properly
pkg install python-grpcio python-pillow python-cryptography

# Install google-generativeai
pip install --break-system-packages --no-deps google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf

# Test installation
python -c "import grpc, cryptography; from PIL import Image; import google.generativeai"

# Run diagnostics
gemini-termux doctor

# Setup API key
gemini-termux setup
```

---

**Remember:** Install grpcio, Pillow, AND cryptography via `pkg`, never via pip!
