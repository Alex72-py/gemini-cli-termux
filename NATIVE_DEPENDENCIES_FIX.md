# 🔧 NATIVE DEPENDENCIES FIX - All Compilation Issues Resolved

## ❌ The Problems

When trying to install Python packages on Termux, you get compilation errors:

### Problem 1: grpcio
```
ERROR: Failed building wheel for grpcio
Command '/data/data/com.termux/files/usr/bin/aarch64-linux-android-clang' failed
```

### Problem 2: Pillow
```
ERROR: Failed building wheel for Pillow
× Building wheel for Pillow (pyproject.toml) did not run successfully.
```

### Problem 3: cryptography
```
ERROR: Failed to build 'cryptography' when installing build dependencies
Rust not found, installing into a temporary directory
Unsupported platform: 312
```

## Why These Fail

All three packages require **native compilation**:

### grpcio:
- C++ library for gRPC
- Needs Android NDK
- Platform detection fails

### Pillow:
- Image processing library
- Needs libjpeg, libpng, zlib
- C extensions won't compile

### cryptography:
- Cryptographic library
- Written in Rust
- Requires Rust compiler + toolchain
- Compilation fails on Android

## ✅ The Solution

### Use Termux's Pre-Compiled Packages

```bash
# WRONG (all fail):
pip install google-generativeai  # tries to build grpcio
pip install Pillow               # tries to compile C code
pip install cryptography         # tries to compile Rust code

# CORRECT:
pkg install python-grpcio python-pillow python-cryptography
pip install --no-deps google-generativeai
pip install google-ai-generativelanguage protobuf
```

## 📋 Complete Installation Steps

### Step 1: Install System Packages
```bash
pkg update && pkg upgrade -y
pkg install python git termux-api python-grpcio python-pillow python-cryptography -y
```

### Step 2: Clone Repository
```bash
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux
```

### Step 3: Install Python Dependencies
```bash
# Install pure Python packages (native libs excluded)
pip install --break-system-packages -r requirements.txt
```

### Step 4: Install google-generativeai Properly
```bash
# grpcio, Pillow, and cryptography already installed via pkg
# Install google-generativeai WITHOUT trying to rebuild them
pip install --break-system-packages --no-deps google-generativeai

# Install other dependencies of google-generativeai
pip install --break-system-packages google-ai-generativelanguage protobuf
```

### Step 5: Install CLI
```bash
pip install --break-system-packages -e .
```

### Step 6: Verify
```bash
python -c "import grpc; print('✓ grpcio:', grpc.__version__)"
python -c "from PIL import Image; print('✓ Pillow: OK')"
python -c "import cryptography; print('✓ cryptography: OK')"
python -c "import google.generativeai as genai; print('✓ google-generativeai: OK')"
gemini-termux --version
```

## 🤖 Automated Installation

The `install.sh` script handles this automatically:

```bash
chmod +x install.sh
./install.sh
```

It will:
1. Install `python-grpcio` via pkg
2. Install requirements.txt (without google-generativeai)
3. Install google-generativeai with --no-deps
4. Install google-generativeai's other dependencies
5. Install the CLI

## 🔍 Why This Works

### Traditional pip approach (FAILS):
```
pip install google-generativeai
  └─> Tries to install grpcio
      └─> Tries to compile C++ code
          └─> ❌ FAILS on Termux
```

### Our approach (WORKS):
```
pkg install python-grpcio  ← Pre-compiled binary
  ✓ Installed

pip install --no-deps google-generativeai
  ✓ Installed (doesn't try to install grpcio)

pip install google-ai-generativelanguage protobuf
  ✓ Installed (pure Python packages)
```

## 📦 Package Details

### Termux python-grpcio package:
- **Source**: Termux official repositories
- **Version**: Usually 1.60.x - 1.70.x
- **Architecture**: Pre-compiled for ARM64/ARM32
- **Installation**: `pkg install python-grpcio`

### PyPI google-generativeai package:
- **Dependencies**: grpcio, google-ai-generativelanguage, protobuf
- **Installation**: `pip install --no-deps google-generativeai`
- **Why --no-deps**: Prevents pip from trying to install grpcio

## 🚨 Common Mistakes

### ❌ DON'T DO THIS:
```bash
# This will FAIL:
pip install google-generativeai

# This will also FAIL:
pip install grpcio
```

### ✅ DO THIS:
```bash
# Use Termux package manager for grpcio:
pkg install python-grpcio

# Then use pip with --no-deps:
pip install --break-system-packages --no-deps google-generativeai
```

## 🔬 Technical Details

### Why grpcio fails on Termux:

1. **Missing Android NDK**
   - grpcio build requires Android NDK
   - Termux doesn't provide NDK

2. **Platform Detection**
   - grpcio doesn't recognize Android
   - Tries to use Linux compilation flags
   - Fails with Android-specific errors

3. **Header Files**
   - Missing: `sys/epoll.h`, various C++ headers
   - Android versions have different headers
   - API level mismatches

4. **Compiler Issues**
   - `aarch64-linux-android-clang` differences
   - Incompatible flags
   - Linker errors

### How Termux's package solves this:

- Pre-compiled on Termux build servers
- Correct Android NDK configuration
- Platform-specific patches applied
- Binary distribution (no compilation needed)

## 📊 Version Compatibility

| Package | Version | Method | Status |
|---------|---------|--------|--------|
| grpcio | 1.60+ | pkg | ✅ Works |
| grpcio | any | pip | ❌ Fails |
| google-generativeai | 0.8.0+ | pip (with --no-deps) | ✅ Works |
| google-generativeai | any | pip (normal) | ❌ Fails (tries to build grpcio) |

## 🎯 Summary

**The key to success:**
1. Install `python-grpcio`, `python-pillow`, AND `python-cryptography` via `pkg` (not pip)
2. Install `google-generativeai` with `--no-deps` flag
3. Manually install other dependencies

**All three packages are handled automatically** by the `install.sh` script!

---

**Updated**: February 13, 2026  
**Status**: ✅ FIXED - All three native dependencies resolved (grpcio, Pillow, cryptography)
