# OpenCode Session Namer

**Intelligent, automatic session naming for OpenCode using local LLMs**

Automatically gives your OpenCode sessions descriptive, meaningful names that update as you work. Uses your local llama.cpp instance for privacy and efficiency.

## ✨ Features

- **🤖 Local LLM Integration**: Uses llama.cpp with models like Llama 3.2 3B or TinyLlama
- **📊 Smart Updates**: Session titles update every 50 messages to reflect progress
- **🔍 Context-Aware**: Analyzes recent messages to generate relevant titles
- **⚡ Efficient**: Minimal prompts, fast inference, low resource usage
- **🔧 Configurable**: Customize update intervals, models, and prompts
- **📦 Easy Setup**: Simple installation with systemd service

## 🚀 Quick Start

### Prerequisites
- [OpenCode](https://github.com/opencode-ai/opencode) installed and running
- [llama.cpp](https://github.com/ggerganov/llama.cpp) server running (port 8080)
- Python 3.8+ with `requests` library

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/opencode-session-namer.git
cd opencode-session-namer

# Run the installer
chmod +x install-llm-namer.sh
./install-llm-namer.sh

# Follow the printed instructions to install systemd service
```

### Manual Run
```bash
python3 src/opencode-session-namer.py
```

## 🛠️ Configuration

### Environment Variables
```bash
# Database path (default: ~/.opencode/opencode.db)
export OPENCODE_DB_PATH="/path/to/opencode.db"

# LLM server URL (default: http://localhost:8080/v1/chat/completions)
export LLAMA_SERVER_URL="http://localhost:8080/v1/chat/completions"

# Model name (default: llama-3.2-3b-instruct-q4_k_m.gguf)
export LLAMA_MODEL="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

# Update interval (default: 50 messages)
export UPDATE_INTERVAL=50

# Check interval (default: 30 seconds)
export CHECK_INTERVAL=30
```

### Python API
```python
from src.session_namer import SessionTitleUpdater

# Custom configuration
updater = SessionTitleUpdater(
    db_path="~/.opencode/opencode.db",
    llama_url="http://localhost:8080/v1/chat/completions",
    model="llama-3.2-3b-instruct-q4_k_m.gguf"
)

# Run the service
updater.run()
```

## 📋 How It Works

1. **Monitors** OpenCode SQLite database for new/updated sessions
2. **Extracts** context from recent messages (last 50 chars)
3. **Generates** descriptive titles using local LLM
4. **Updates** session titles in the database
5. **Repeats** every 50 messages with progress-aware updates

### Example Titles
- New session: `api-auth-implementation`, `bug-fix-express`, `ui-refactor-react`
- Updated (progress): `api-75%-2h`, `bug-fix-complete`, `ui-50%-components`

## 🐳 Docker Support

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install requests

CMD ["python", "src/opencode-session-namer.py"]
```

## 🔧 Development

### Project Structure
```
opencode-session-namer/
├── src/
│   ├── __init__.py          # Package exports
│   ├── session_namer.py     # Main implementation
│   └── opencode-session-namer.py  # CLI entry point
├── tests/                   # Test suite
├── docs/                    # Documentation
├── install-llm-namer.sh     # Installation script
└── README.md               # This file
```

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

### Building from Source
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/opencode-session-namer.git
cd opencode-session-namer
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenCode](https://github.com/opencode-ai/opencode) for the amazing AI coding assistant
- [llama.cpp](https://github.com/ggerganov/llama.cpp) for efficient local LLM inference
- All contributors and users of this project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/opencode-session-namer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/opencode-session-namer/discussions)
- **Email**: your-email@example.com

---

## 🚀 Pushing to GitHub

### Using the Helper Script
```bash
# Make the script executable
chmod +x push-to-github.sh

# Run the interactive push helper
./push-to-github.sh
```

### Manual Push
```bash
# Create repository on GitHub (https://github.com/new)
# Name: opencode-session-namer
# Don't initialize with README, .gitignore, or license

# Add remote and push
git remote add origin https://github.com/yourusername/opencode-session-namer.git
git branch -M main
git push -u origin main
```