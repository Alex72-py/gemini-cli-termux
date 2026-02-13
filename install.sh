#!/data/data/com.termux/files/usr/bin/bash

# Gemini CLI for Termux - Installation Script
# Author: Alex72-py
# License: MIT

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    # - python-grpcio: Required by google-generativeai
    # - python-pillow: Image processing library
    pkg install -y python git termux-api python-grpcio python-pillow || {
        print_error "Failed to install packages"
        exit 1
    }
    
    print_success "System dependencies installed"
}

install_python_packages() {
    print_step "Installing Python packages..."
    
    # Upgrade pip
    pip install --upgrade pip --break-system-packages || {
        print_warning "Failed to upgrade pip (continuing anyway)"
    }
    
    # Install requirements (WITHOUT google-generativeai, it needs special handling)
    pip install --break-system-packages -r requirements.txt || {
        print_error "Failed to install Python packages"
        exit 1
    }
    
    # NOW install google-generativeai (will use the system grpcio)
    print_step "Installing google-generativeai (using system grpcio)..."
    pip install --break-system-packages --no-deps google-generativeai || {
        print_error "Failed to install google-generativeai"
        exit 1
    }
    
    # Install missing dependencies of google-generativeai (except grpcio)
    pip install --break-system-packages google-ai-generativelanguage protobuf || {
        print_error "Failed to install google-generativeai dependencies"
        exit 1
    }
    
    print_success "Python packages installed"
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
        print_warning "Setup skipped. Run 'gemini-termux setup' later."
    fi
}

verify_installation() {
    print_step "Verifying installation..."
    
    # Check if command is available
    if command -v gemini-termux &> /dev/null; then
        print_success "CLI command available"
        
        # Check version
        VERSION=$(gemini-termux --version 2>&1 | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
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
