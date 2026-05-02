import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import sqlite3

from src.session_namer import SessionTitleUpdater

def test_session_title_updater_init():
    """Test SessionTitleUpdater initialization."""
    updater = SessionTitleUpdater()
    assert updater.db_path == Path.home() / ".opencode" / "opencode.db"
    assert updater.llama_url == "http://localhost:8080/v1/chat/completions"
    assert updater.model == "llama-3.2-3b-instruct-q4_k_m.gguf"
    assert updater.session_states == {}

def test_session_title_updater_custom_init():
    """Test SessionTitleUpdater with custom parameters."""
    custom_db = Path("/custom/path.db")
    custom_url = "http://custom:9090/v1/chat/completions"
    custom_model = "custom-model.gguf"
    
    updater = SessionTitleUpdater(
        db_path=custom_db,
        llama_url=custom_url,
        model=custom_model
    )
    
    assert updater.db_path == custom_db
    assert updater.llama_url == custom_url
    assert updater.model == custom_model

def test_generate_title_fallback():
    """Test title generation fallback when LLM fails."""
    updater = SessionTitleUpdater()
    
    with patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Network error")
        
        title = updater.generate_title("test context", False)
        assert title.startswith("session-")
        assert len(title) > 8

def test_get_session_context_no_messages():
    """Test context extraction with no messages."""
    updater = SessionTitleUpdater()
    
    # Create a temporary database
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        updater.db_path = Path(tmp.name)
        updater.connect()
        
        # Create sessions table
        cursor = updater.conn.cursor()
        cursor.execute("""
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY,
                title TEXT,
                message_count INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE messages (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                content TEXT,
                created_at INTEGER
            )
        """)
        
        context = updater.get_session_context("test-session-id")
        assert context == "code"
        
        updater.disconnect()

def test_update_session():
    """Test updating session title in database."""
    updater = SessionTitleUpdater()
    
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        updater.db_path = Path(tmp.name)
        updater.connect()
        
        # Create sessions table
        cursor = updater.conn.cursor()
        cursor.execute("""
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY,
                title TEXT,
                message_count INTEGER
            )
        """)
        
        # Insert test session
        cursor.execute(
            "INSERT INTO sessions (id, title, message_count) VALUES (?, ?, ?)",
            ("test-session", "old title", 10)
        )
        updater.conn.commit()
        
        # Update title
        success = updater.update_session("test-session", "new title")
        assert success
        
        # Verify update
        cursor.execute("SELECT title FROM sessions WHERE id = ?", ("test-session",))
        result = cursor.fetchone()
        assert result[0] == "new title"
        
        updater.disconnect()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])