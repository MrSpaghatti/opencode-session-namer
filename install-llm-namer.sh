#!/bin/bash

set -e

echo "🚀 OpenCode Session Namer Installer"
echo "==================================="
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! python3 -c "import requests" &> /dev/null; then
    echo "⚠️  requests module not found, installing..."
    pip3 install requests || {
        echo "❌ Failed to install requests module"
        exit 1
    }
fi

echo "✅ Prerequisites satisfied"
echo ""

# Make scripts executable
echo "🔧 Setting up scripts..."
chmod +x src/opencode-session-namer.py
echo "✅ Scripts made executable"
echo ""

# Create systemd service
echo "📦 Creating systemd service..."
SERVICE_FILE="opencode-session-namer.service"
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=OpenCode Session Namer with Local LLM
After=network.target
Wants=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(which python3) $(pwd)/src/opencode-session-namer.py
Restart=on-failure
RestartSec=10
Environment="PYTHONUNBUFFERED=1"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Optional environment overrides
# Environment="OPENCODE_DB_PATH=/path/to/opencode.db"
# Environment="LLAMA_SERVER_URL=http://localhost:8080/v1/chat/completions"
# Environment="LLAMA_MODEL=llama-3.2-3b-instruct-q4_k_m.gguf"
# Environment="UPDATE_INTERVAL=50"
# Environment="CHECK_INTERVAL=30"

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file created: $SERVICE_FILE"
echo ""

echo "📋 Installation Summary"
echo "======================"
echo ""
echo "📁 Project location: $(pwd)"
echo "🐍 Python script: src/opencode-session-namer.py"
echo "⚙️  Systemd service: $SERVICE_FILE"
echo ""
echo "📝 Next Steps:"
echo "--------------"
echo ""
echo "1. Review the service file:"
echo "   cat $SERVICE_FILE"
echo ""
echo "2. Install systemd service (requires sudo):"
echo "   sudo cp $SERVICE_FILE /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo ""
echo "3. Start the service:"
echo "   sudo systemctl start opencode-session-namer"
echo ""
echo "4. Enable auto-start:"
echo "   sudo systemctl enable opencode-session-namer"
echo ""
echo "5. Check status:"
echo "   sudo systemctl status opencode-session-namer"
echo ""
echo "6. View logs:"
echo "   sudo journalctl -u opencode-session-namer -f"
echo ""
echo "🔧 Manual Testing:"
echo "-----------------"
echo "Run manually to test:"
echo "  python3 src/opencode-session-namer.py"
echo ""
echo "📚 Documentation:"
echo "----------------"
echo "See README.md for configuration options and API usage."
echo ""
echo "✅ Installation complete!"