#!/usr/bin/env python3
"""
OpenCode Session Namer with Local LLM - Main entry point
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from session_namer import SessionTitleUpdater

def main():
    """Main entry point for the CLI"""
    updater = SessionTitleUpdater()
    updater.run()

if __name__ == "__main__":
    main()