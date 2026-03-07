#!/bin/bash
# ============================================================
#  NetAudit Pro — Linux/macOS Launcher
#  Auto-installs dependencies + requests sudo
# ============================================================

cd "$(dirname "$0")"

echo ""
echo "  ============================================================"
echo "   NetAudit Pro — Home Network Security Audit Tool"
echo "  ============================================================"
echo ""

# Find Python
PYTHON=""
command -v python3 &>/dev/null && PYTHON="python3"
command -v python  &>/dev/null && [ -z "$PYTHON" ] && PYTHON="python"

if [ -z "$PYTHON" ]; then
    echo "  ERROR: Python not found!"
    echo "  Install with: sudo apt install python3"
    exit 1
fi

# ── AUTO INSTALL DEPENDENCIES ────────────────────────────
echo "  Checking dependencies..."
echo ""

install_pkg() {
    $PYTHON -c "import $1" &>/dev/null
    if [ $? -ne 0 ]; then
        echo "  Installing $2..."
        if [ "$EUID" -eq 0 ]; then
            pip3 install $2 --break-system-packages --quiet 2>/dev/null || \
            pip3 install $2 --quiet 2>/dev/null || \
            $PYTHON -m pip install $2 --break-system-packages --quiet
        else
            sudo pip3 install $2 --break-system-packages --quiet 2>/dev/null || \
            pip3 install $2 --quiet 2>/dev/null
        fi
        echo "  $2 installed!"
    fi
}

install_pkg "reportlab" "reportlab"
install_pkg "scapy"     "scapy"
install_pkg "PIL"       "pillow"

echo ""
echo "  All dependencies ready!"
echo "  ============================================================"
echo ""

# ── CHECK ROOT ───────────────────────────────────────────
if [ "$EUID" -ne 0 ]; then
    echo "  Requesting root for ARP network scanning..."
    sudo $PYTHON launch.py
else
    $PYTHON launch.py
fi