"""
Chat Service for managing conversations and messages
"""

from eduassist.data.database import get_db
from datetime import datetime
from typing import List, Dict, Optional


def create_conversation(user_id: int, title: str, model: str, language: str = 'english') -> Optional[int]:
    """Create a new chat conversation"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_conversations (user_id, title, model, language, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, title, model, language, datetime.now(), datetime.now()))
        return cursor.lastrowid


def get_user_conversations(user_id: int) -> List[Dict]:
    """Get all conversations for a user, ordered by most recent"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, model, language, created_at, updated_at
            FROM chat_conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC
        """, (user_id,))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'id': row[0],
                'title': row[1],
                'model': row[2],
                'language': row[3],
                'created_at': row[4],
                'updated_at': row[5]
            })
        return conversations


def get_conversation(conversation_id: int, user_id: int) -> Optional[Dict]:
    """Get a specific conversation with its messages"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get conversation details
        cursor.execute("""
            SELECT id, title, model, language, created_at, updated_at
            FROM chat_conversations
            WHERE id = ? AND user_id = ?
        """, (conversation_id, user_id))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        conversation = {
            'id': row[0],
            'title': row[1],
            'model': row[2],
            'language': row[3],
            'created_at': row[4],
            'updated_at': row[5],
            'messages': []
        }
        
        # Get messages
        cursor.execute("""
            SELECT id, role, content, created_at
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY created_at ASC
        """, (conversation_id,))
        
        for msg_row in cursor.fetchall():
            conversation['messages'].append({
                'id': msg_row[0],
                'role': msg_row[1],
                'content': msg_row[2],
                'created_at': msg_row[3]
            })
        
        return conversation


def add_message(conversation_id: int, role: str, content: str) -> int:
    """Add a message to a conversation"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_messages (conversation_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, role, content, datetime.now()))
        
        # Update conversation's updated_at timestamp
        cursor.execute("""
            UPDATE chat_conversations
            SET updated_at = ?
            WHERE id = ?
        """, (datetime.now(), conversation_id))
        
        return cursor.lastrowid


def delete_conversation(conversation_id: int, user_id: int) -> bool:
    """Delete a conversation and all its messages"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Verify ownership
        cursor.execute("""
            SELECT id FROM chat_conversations
            WHERE id = ? AND user_id = ?
        """, (conversation_id, user_id))
        
        if not cursor.fetchone():
            return False
        
        # Delete conversation (messages will cascade delete)
        cursor.execute("""
            DELETE FROM chat_conversations
            WHERE id = ?
        """, (conversation_id,))
        
        return True


def update_conversation_title(conversation_id: int, user_id: int, title: str) -> bool:
    """Update conversation title"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE chat_conversations
            SET title = ?, updated_at = ?
            WHERE id = ? AND user_id = ?
        """, (title, datetime.now(), conversation_id, user_id))
        
        return cursor.rowcount > 0


def generate_title_from_message(message: str) -> str:
    """Generate a conversation title from the first message"""
    # Take first 50 characters and add ellipsis if longer
    title = message.strip()[:50]
    if len(message) > 50:
        title += "..."
    return title
