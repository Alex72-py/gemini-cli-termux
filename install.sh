#!/data/data/com.termux/files/usr/bin/bash

# Gemini CLI for Termux - Installation Script
# Author: Alex72-py
# License: MIT

set -e  # Exit on error

# Colors
RED=\'\\033[0;31m\'
GREEN=\'\\033[0;32m\'
YELLOW=\'\\033[1;33m\'
BLUE=\'\\033[0;34m\'
NC=\'\\033[0m\' # No Color

# Functions
print_header() {
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  🤖 Gemini CLI for Termux - Installer${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

check_termux() {
    if [ -z "$PREFIX" ]; then
        print_error "This script must be run in Termux"
        exit 1
    fi
    print_success "Running in Termux"
}

install_dependencies() {
    print_step "Installing system dependencies..."
    
    # Update package lists
    pkg update -y || {
        print_error "Failed to update package lists"
        exit 1
    }
    
    # Install required packages INCLUDING pre-compiled native libraries
    # CRITICAL: These must be installed via pkg, NOT pip:
    # - python-grpcio: Required by google-generativeai (gRPC library)
    # - python-pillow: Image processing library
    # - python-cryptography: Cryptographic library (Rust-based)
    # - python-pydantic: Validation library (Rust-based pydantic-core)
    pkg install -y python git termux-api python-grpcio python-pillow python-cryptography python-pydantic || {
        print_error "Failed to install packages"
        exit 1
    }
    
    print_success "System dependencies installed"
}

install_python_packages() {
    print_step "Installing Python packages..."
    
    # NOTE: DO NOT upgrade pip in Termux - it breaks the python-pip package
    
    # FIRST: Install requirements.txt (pure Python packages)
    print_step "Installing base Python dependencies..."
    pip install --break-system-packages -r requirements.txt || {
        print_error "Failed to install Python packages"
        exit 1
    }
    
    # SECOND: Install google-generativeai dependencies (BEFORE google-generativeai)
    # Note: pydantic is already installed via pkg, so we only install these
    print_step "Installing google-generativeai dependencies..."
    pip install --break-system-packages google-ai-generativelanguage protobuf || {
        print_error "Failed to install google-generativeai dependencies"
        exit 1
    }
    
    # THIRD: Install google-generativeai with --no-deps (uses system packages)
    print_step "Installing google-generativeai (using system grpcio and pydantic)..."
    pip install --break-system-packages --no-deps google-generativeai || {
        print_error "Failed to install google-generativeai"
        exit 1
    }
    
    print_success "Python packages installed"
}

verify_imports() {
    print_step "Verifying core imports..."
    
    # Run Python verification and capture exit code
    if ! python3 << \'EOF\'
import sys
errors = []

try:
    import grpc
    print("✓ grpcio:", grpc.__version__)
except ImportError as e:
    errors.append(f"✗ grpcio: {e}")

try:
    from PIL import Image
    print("✓ Pillow: OK")
except ImportError as e:
    errors.append(f"✗ Pillow: {e}")

try:
    import cryptography
    print("✓ cryptography: OK")
except ImportError as e:
    errors.append(f"✗ cryptography: {e}")

try:
    import httpx
    print("✓ httpx:", httpx.__version__)
except ImportError as e:
    errors.append(f"✗ httpx: {e}")

try:
    import pydantic
    print("✓ pydantic:", pydantic.__version__)
except ImportError as e:
    errors.append(f"✗ pydantic: {e}")

try:
    import google.ai.generativelanguage
    print("✓ google-ai-generativelanguage: OK")
except ImportError as e:
    errors.append(f"✗ google-ai-generativelanguage: {e}")

try:
    import google.protobuf
    print("✓ protobuf: OK")
except ImportError as e:
    errors.append(f"✗ protobuf: {e}")

try:
    import google.generativeai as genai
    print("✓ google-generativeai: OK")
except ImportError as e:
    errors.append(f"✗ google-generativeai: {e}")

if errors:
    print("\nERRORS:")
    for error in errors:
        print(error)
    sys.exit(1)
EOF
    then
        print_error "Import verification failed"
        exit 1
    fi
    
    print_success "All imports verified"
}

install_cli() {
    print_step "Installing Gemini CLI..."
    
    # Install in development mode
    pip install --break-system-packages -e . || {
        print_error "Failed to install CLI"
        exit 1
    }
    
    print_success "Gemini CLI installed"
}

setup_permissions() {
    print_step "Setting up permissions..."
    
    # Make executable
    chmod +x gemini_cli/main.py 2>/dev/null || true
    
    print_success "Permissions configured"
}

run_setup_wizard() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Would you like to run the setup wizard?${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════${NC}"
    echo ""
    echo "This will configure your API key and preferences."
    echo ""
    read -p "Run setup now? (Y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        gemini-termux setup
    else
        print_warning "Setup skipped. Run \'gemini-termux setup\' later."
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    # Check if command is available
    if command -v gemini-termux &> /dev/null; then
        print_success "CLI command available"
        
        # Check version
        VERSION=$(gemini-termux --version 2>&1 | grep -oP \'\\d+\\.\\d+\\.\\d+\' || echo "unknown")
        print_success "Version: $VERSION"
    else
        print_error "CLI command not found"
        print_warning "Try restarting your terminal"
        return 1
    fi
    
    # Run doctor
    echo ""
    print_step "Running diagnostics..."
    gemini-termux doctor || true
}

print_completion() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ Installation Complete!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════${NC}"
    echo ""
    echo "Quick Start Commands:"
    echo ""
    echo -e "  ${BLUE}gemini-termux setup${NC}        - Configure API key"
    echo -e "  ${BLUE}gemini-termux chat${NC}         - Start interactive chat"
    echo -e "  ${BLUE}gemini-termux ask \"...\"${NC}    - Quick question"
    echo -e "  ${BLUE}gemini-termux --help${NC}       - Show all commands"
    echo ""
    echo "Documentation:"
    echo -e "  ${BLUE}https://github.com/Alex72-py/gemini-cli-termux${NC}"
    echo ""
}

# Main installation flow
main() {
    print_header
    
    # Check environment
    check_termux
    
    # Install
    install_dependencies
    install_python_packages
    verify_imports  # Verify imports work
    install_cli
    setup_permissions
    
    # Verify
    verify_installation
    
    # Setup wizard
    run_setup_wizard
    
    # Done
    print_completion
}

# Run installation
main
