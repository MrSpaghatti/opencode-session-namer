import sqlite3
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

class SessionTitleUpdater:
    """OpenCode session title updater using local LLM."""
    
    UPDATE_INTERVAL = 50
    CHECK_INTERVAL = 30
    DEFAULT_DB_PATH = Path.home() / ".opencode" / "opencode.db"
    DEFAULT_LLAMA_URL = "http://localhost:8080/v1/chat/completions"
    DEFAULT_MODEL = "llama-3.2-3b-instruct-q4_k_m.gguf"
    
    def __init__(
        self,
        db_path: Optional[Path] = None,
        llama_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.db_path = Path(db_path) if db_path else self.DEFAULT_DB_PATH
        self.llama_url = llama_url or self.DEFAULT_LLAMA_URL
        self.model = model or self.DEFAULT_MODEL
        self.conn = None
        self.session_states = {}
        
    def connect(self) -> bool:
        """Connect to OpenCode database."""
        if not self.db_path.exists():
            return False
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        return True
    
    def disconnect(self):
        """Disconnect from database."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def generate_title(self, context: str, is_update: bool = False) -> str:
        """Generate session title using local LLM or fallback."""
        try:
            prompt = f"Update: {context}" if is_update else f"New: {context}"
            response = requests.post(
                self.llama_url,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "Make 2-4 word kebab-case titles."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 12,
                    "temperature": 0.2
                },
                timeout=3
            )
            if response.status_code == 200:
                title = response.json()["choices"][0]["message"]["content"].strip()
                return title.replace('`', '').replace('"', '').replace('.', '')[:40]
        except Exception:
            pass
        return f"session-{datetime.now().strftime('%H%M')}"
    
    def get_session_context(self, session_id: str) -> str:
        """Extract context from last message in session."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT content FROM messages 
                WHERE session_id = ? 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (session_id,))
            row = cursor.fetchone()
            return row[0][:50] if row and row[0] else "code"
        except Exception:
            return "code"
    
    def update_session(self, session_id: str, new_title: str) -> bool:
        """Update session title in database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE sessions SET title = ? WHERE id = ?",
                (new_title, session_id)
            )
            return True
        except Exception:
            return False
    
    def check_and_update_sessions(self):
        """Check all sessions and update titles if needed."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, title, message_count FROM sessions")
            
            for session in cursor.fetchall():
                session_id = session['id']
                msg_count = session['message_count'] or 0
                current_title = session['title'] or ""
                
                if session_id not in self.session_states:
                    context = self.get_session_context(session_id)
                    new_title = self.generate_title(context, False)
                    if new_title != current_title:
                        self.update_session(session_id, new_title)
                    self.session_states[session_id] = msg_count
                    
                elif msg_count - self.session_states[session_id] >= self.UPDATE_INTERVAL:
                    context = self.get_session_context(session_id)
                    new_title = self.generate_title(context, True)
                    if new_title != current_title:
                        self.update_session(session_id, new_title)
                    self.session_states[session_id] = msg_count
            
            self.conn.commit()
        except Exception as e:
            print(f"Error checking sessions: {e}")
    
    def run(self):
        """Main loop for the session naming service."""
        print(f"OpenCode Session Namer - Local LLM")
        print(f"Model: {self.model}")
        print(f"Update every: {self.UPDATE_INTERVAL} messages")
        print(f"Check interval: {self.CHECK_INTERVAL} seconds")
        print("Press Ctrl+C to stop\n")
        
        if not self.connect():
            print(f"Database not found: {self.db_path}")
            return
        
        try:
            while True:
                self.check_and_update_sessions()
                time.sleep(self.CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.disconnect()
            print("Stopped")