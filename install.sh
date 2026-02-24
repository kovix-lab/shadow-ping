#!/bin/bash

echo "🚀 Starting Shadow-Ping Installation..."

# 1. Define the project directory
PROJECT_DIR=$(pwd)
APP_DIR="$HOME/.local/share/shadow-ping"

# 2. Create a permanent home for the app files
mkdir -p "$APP_DIR"
cp -r "$PROJECT_DIR"/* "$APP_DIR/"

# 3. Build the virtual environment in the permanent home
echo "📦 Setting up Python environment..."
python3 -m venv "$APP_DIR/venv"
source "$APP_DIR/venv/bin/activate"
pip install -r "$APP_DIR/requirements.txt"
deactivate

# 4. Create the system-compatible .desktop file
echo "🖥️ Integrating with Desktop Environment..."
DESKTOP_FILE="$HOME/.local/share/applications/shadow-ping.desktop"

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Name=Shadow-Ping
Comment=Secure IP and URL Locator
Exec=$APP_DIR/venv/bin/python $APP_DIR/main.py
Icon=$APP_DIR/icons/icon.png
Terminal=false
Type=Application
Categories=Network;Security;Utility;
EOF

chmod +x "$DESKTOP_FILE"

echo "✅ Installation Complete! You can now find Shadow-Ping in your Applications menu."