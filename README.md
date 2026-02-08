# Gemini CLI for Termux (Android)

[![License](https://img.shields.io/github/license/google-gemini/gemini-cli)](https://github.com/google-gemini/gemini-cli/blob/main/LICENSE)
[![Fork of](https://img.shields.io/badge/fork%20of-google--gemini%2Fgemini--cli-blue)](https://github.com/google-gemini/gemini-cli)

This is an **explicit fork** of the [Google Gemini CLI](https://github.com/google-gemini/gemini-cli), specifically adapted and optimized for **Android devices running Termux**.

## 📱 Why this fork?

The original Gemini CLI is designed for desktop environments. This fork introduces several changes to make it work seamlessly on Android:

- **Termux Browser Support**: Replaced standard browser launching with `termux-open-url` for OAuth authentication.
- **Android-Ready Installer**: A dedicated script to handle Termux-specific dependencies (Node.js LTS, Python, and build tools).
- **Environment Optimization**: Pre-configured to handle the unique filesystem and permission structure of Termux.

## 🛠️ Installation

To install Gemini CLI on your Android device:

1.  **Install Termux**: Get it from [F-Droid](https://f-droid.org/en/packages/com.termux/).
2.  **Install Termux:API**: Install the [Termux:API app](https://f-droid.org/en/packages/com.termux.api/) and the package:
    ```bash
    pkg install termux-api
    ```
3.  **Run the Installer**:
    ```bash
    curl -sL https://raw.githubusercontent.com/Alex72-py/gemini-cli-termux/master/termux-install.sh | bash
    ```

## 🚀 Getting Started

After installation, simply run:
```bash
gemini login
```
Follow the prompt to authenticate via your mobile browser.

## 📜 Acknowledgments & Credits

This project is a derivative work based on the [Gemini CLI](https://github.com/google-gemini/gemini-cli) developed by **Google**. 

- **Original Author**: [Google Gemini Team](https://github.com/google-gemini)
- **License**: This fork maintains the original **Apache License 2.0**.

We are grateful to the original authors for their incredible work in bringing Gemini to the terminal. This fork aims to extend that power to the mobile developer community.

---
*Built for the Termux community by Alex72-py.*
