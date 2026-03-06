#!/bin/bash
# ============================================================
#  NetAudit Pro — Linux / macOS Launcher
#  Double-click or run:  bash RUN_ME.sh
#  Automatically requests sudo for ARP scanning
# ============================================================

# Go to the folder where this script lives
cd "$(dirname "$0")"

echo ""
echo "============================================"
echo "  🛡️  NetAudit Pro — Network Audit Tool"
echo "  By SaiDinesh Andekar"
echo "============================================"
echo ""

# Find Python
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
fi

if [ -z "$PYTHON" ]; then
    echo "  ❌ Python not found!"
    echo "  Install Python:"
    echo ""
    echo "  Ubuntu/Debian:  sudo apt install python3 python3-pip"
    echo "  macOS:          brew install python3"
    echo "  Or visit:       https://python.org"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi

# Check if already root
if [ "$EUID" -eq 0 ]; then
    echo "  ✅ Running as root"
    $PYTHON launch.py
else
    echo "  🔐 Root required for ARP network scanning."
    echo "  Requesting sudo — enter your password:"
    echo ""
    sudo $PYTHON launch.py
fi
