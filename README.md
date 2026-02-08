# Gemini CLI on Termux (Experimental)

> [!WARNING]  
> This is an **experimental fork** of the official
> [Google Gemini CLI](https://github.com/google-gemini/gemini-cli). While it
> provides a path to run Gemini on Android via Termux, it is currently
> **unstable** and intended for developers and enthusiasts.

## Status

- **Installation**: ✅ Works
- **CLI Startup**: ✅ Works
- **Core Commands**: ⚠️ Partial Implementation
- **Authentication**: ❌ Unstable

## Known Issues

- **Authentication Failures**: OAuth and Web API support on Android are
  inconsistent, often leading to auth errors.
- **Dependency Issues**: `DOMException` and issues with deprecated Node.js
  dependencies in the Termux environment.
- **Stability**: Inconsistent behavior across different Node.js versions and
  Android releases.
- **UI Bugs**: Potential infinite scrolling issues when toggling the on-screen
  keyboard.

## Environment

- **Platform**: Termux (Android)
- **Node.js**: v20.x / v22.x (Behavior varies)
- **Android**: Version 10+ recommended

## Installation (Termux)

To attempt an installation in your Termux environment, run:

```bash
curl -sL https://raw.githubusercontent.com/Alex72-py/gemini-cli-termux/master/termux-install.sh | bash
```

## Notes

This repository documents a working but unstable setup to help others
experiment, debug, or improve Gemini CLI support on Termux. It is not
recommended for production use.

## Credits & Acknowledgments

This project is a fork of the
[Google Gemini CLI](https://github.com/google-gemini/gemini-cli). All core logic
and branding belong to the original Google Gemini team. This fork specifically
adds patches for Termux compatibility.

For a full list of credits, see [CREDITS.md](./CREDITS.md).

---

_Built for the Termux community by Alex72-py._
