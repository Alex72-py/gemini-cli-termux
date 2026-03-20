# Requirements Explained

## Why Split Installation?

This project uses a **split installation strategy** due to Termux/Android limitations:

### Via `pkg` (System Packages)
```bash
pkg install python-grpcio python-pillow python-cryptography python-pydantic
```

**Why?** These 4 packages contain native code that **requires compilation**:
- **grpcio**: C++ library for gRPC communication
- **Pillow**: C library for image processing (libjpeg, libpng, zlib)
- **cryptography**: Rust-based cryptographic library
- **pydantic**: Rust-based validation library (pydantic-core)

**Problem**: Android/Termux lacks:
- Android NDK (for C/C++ compilation)
- Proper Rust toolchain
- Compatible headers and build tools

**Solution**: Use pre-compiled binaries from Termux repositories.

### Via `pip` (Pure Python Packages)
```bash
pip install rich prompt-toolkit httpx toml PyPDF2 python-dateutil aiofiles
```

These packages are **pure Python** (no compilation needed).

### Via `pip` with Special Handling
```bash
pip install --no-deps google-generativeai
pip install google-ai-generativelanguage protobuf
```

`google-generativeai` depends on `grpcio`, so we:
1. Install `grpcio` via `pkg` first
2. Install `google-generativeai` with `--no-deps` (skips dependency installation)
3. Manually install its other dependencies

## Summary

**4 Native Libraries** (via `pkg`):
- python-grpcio
- python-pillow
- python-cryptography
- python-pydantic

**Pure Python** (via `pip`):
- Everything else!

This strategy ensures **100% successful installation** on Termux.
