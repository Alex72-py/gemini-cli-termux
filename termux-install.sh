#!/data/data/com.termux/files/usr/bin/bash

# Gemini CLI Termux Installer
# This script installs the Gemini CLI and its dependencies in Termux.

set -e

echo "🚀 Starting Gemini CLI (Termux/Android Fork) installation..."
echo "Forked from google-gemini/gemini-cli and adapted for Android."

# Update packages
echo "📦 Updating packages..."
pkg update -y && pkg upgrade -y

# Install dependencies
echo "🛠️ Installing dependencies (Node.js, Python, Build Tools, Git)..."
pkg install nodejs-lts python make clang binutils termux-api git -y

# Clone the repository
echo "📥 Cloning the repository..."
cd $HOME
rm -rf gemini-cli-termux
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux

# Install the CLI
echo "📥 Installing Gemini CLI..."
# Install from this fork's source to ensure Termux patches are applied
echo "🔨 Building and installing from source..."
npm install
npm run build
npm install -g .

echo ""
echo "✅ Installation complete!"
echo "💡 To get started, run: gemini login"
echo "🔗 Make sure you have the 'Termux:API' app installed from F-Droid or Play Store for browser support."
