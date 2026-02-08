#!/data/data/com.termux/files/usr/bin/bash

# Gemini CLI Termux Installer (Final Fixed Version)
# This script handles dependencies, cloning, and manual building to avoid npm lifecycle errors.

set -e

echo "🚀 Starting Gemini CLI (Termux/Android Fork) installation..."
echo "Forked from google-gemini/gemini-cli and adapted for Android."

# 1. Update and Install System Dependencies
echo "📦 Updating packages and installing system dependencies..."
pkg update -y && pkg upgrade -y
pkg install nodejs-lts python make clang binutils termux-api git -y

# 2. Setup Installation Directory
INSTALL_DIR="$HOME/gemini-cli-termux"
echo "📥 Setting up repository in $INSTALL_DIR..."

if [ -d "$INSTALL_DIR" ]; then
    echo "♻️ Existing installation found, cleaning up for a fresh build..."
    rm -rf "$INSTALL_DIR"
fi

cd "$HOME"
git clone https://github.com/Alex72-py/gemini-cli-termux.git
cd gemini-cli-termux

# 3. Install Node Dependencies
echo "📥 Installing Node.js dependencies (ignoring scripts)..."
# We use --ignore-scripts to prevent 'prepare' or 'postinstall' from running in the wrong context
npm install --ignore-scripts

# 4. Manual Build Process
# We manually execute the steps that the original 'prepare' and 'build' scripts would do
echo "🔨 Starting manual build process..."

echo "📦 Generating commit info..."
node scripts/generate-git-commit-info.js

echo "📦 Bundling assets with esbuild..."
node esbuild.config.js

echo "📦 Copying bundle assets..."
node scripts/copy_bundle_assets.js

echo "🏗️ Building TypeScript packages..."
# We run the build script which handles the workspace compilation
npm run build

# 5. Global Installation
echo "🌍 Installing Gemini CLI globally..."
# Install the current directory as a global package
npm install -g .

echo ""
echo "✅ SUCCESS: Gemini CLI is now installed!"
echo "💡 To get started, run: gemini login"
echo "🔗 Note: Ensure the 'Termux:API' app is installed on your Android device for browser support."
