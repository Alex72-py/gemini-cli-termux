# Credits & Acknowledgments

## Inspiration

This project is inspired by the official **[Google Gemini CLI](https://github.com/google-gemini/gemini-cli)** created by the Google Gemini team.

## Original Repository

- **Repository**: https://github.com/google-gemini/gemini-cli
- **Author**: Google LLC
- **License**: Apache 2.0
- **Purpose**: Official CLI tool for interacting with Google's Gemini API

## This Project's Relationship

This is **NOT a fork** of the official repository. Instead, it is:

- A **complete rewrite** from scratch in Python
- **Inspired by** the functionality and features of the official CLI
- **Designed specifically** for Termux on Android
- Built to **solve compatibility issues** that prevent the official CLI from working on Termux

## Why a Rewrite?

The official Gemini CLI cannot run on Termux due to:

1. **Native Dependencies**: Requires node-pty, keytar, and other native modules that won't compile on Android
2. **Platform Detection**: Doesn't recognize Android as a valid platform
3. **Build System**: Requires node-gyp and Android NDK which aren't available in Termux
4. **Authentication**: Uses OAuth2 with system keychains not available on Android
5. **Clipboard**: Uses clipboardy which fails to detect Termux correctly

Rather than attempting to patch these fundamental incompatibilities, this project provides a clean, native Python implementation that works perfectly on Termux while maintaining similar functionality.

## Credits

### Google Gemini Team
- For creating the Gemini API and generative AI models
- For the original CLI design and feature set
- For comprehensive API documentation
- For making Gemini accessible to developers

### Original Contributors
All contributors to the [official Gemini CLI repository](https://github.com/google-gemini/gemini-cli/graphs/contributors) deserve recognition for their work on the original project.

### Dependencies
This project builds upon excellent open-source libraries:

- **[google-generativeai](https://github.com/google/generative-ai-python)** - Official Google Generative AI Python SDK
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal formatting by Will McGugan
- **[prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)** - Interactive command lines by Jonathan Slenders
- **[Pillow](https://github.com/python-pillow/Pillow)** - Python Imaging Library
- **[PyPDF2](https://github.com/py-pdf/PyPDF2)** - PDF processing

### Community
- **Termux Community** - For making Android development possible
- **F-Droid** - For distributing Termux and Termux:API
- **Android Developers** - For the platform we build on
- **Open Source Community** - For the tools and libraries that make this possible

## License Compatibility

- **Original Gemini CLI**: Apache 2.0 License
- **This Project**: MIT License

Both licenses are permissive open-source licenses. This project does not use any code from the original repository - it's an independent implementation inspired by similar goals.

## How to Credit

If you use or reference this project:

```
Gemini CLI for Termux by Alex72-py
Inspired by the official Google Gemini CLI
https://github.com/Alex72-py/gemini-cli-termux
```

If you reference the original:

```
Official Google Gemini CLI
https://github.com/google-gemini/gemini-cli
```

## Trademark Notice

"Gemini" and "Google Gemini" are trademarks of Google LLC. This project is not affiliated with, endorsed by, or sponsored by Google LLC.

## Contributing

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Thank you to everyone who makes open-source software possible! 🙏
