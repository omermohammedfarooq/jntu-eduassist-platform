"""Database abstraction layer with SQLite fallback for local development."""

import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Check for PostgreSQL connection string
DATABASE_URL = os.environ.get("DATABASE_URL")
USE_SQLITE = DATABASE_URL is None

# SQLite database path (project root)
SQLITE_PATH = Path(__file__).parent.parent.parent / "eduassist.db"


def get_connection():
    """Get database connection - SQLite for local dev, PostgreSQL for production."""
    if USE_SQLITE:
        conn = sqlite3.connect(str(SQLITE_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


@contextmanager
def get_db():
    """Context manager for database connections with auto-commit/rollback."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """Initialize database tables - works with both SQLite and PostgreSQL."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        if USE_SQLITE:
            # SQLite table definitions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    branch VARCHAR(100),
                    role VARCHAR(50) DEFAULT 'student',
                    bio TEXT,
                    reset_token VARCHAR(255),
                    reset_token_expiry TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS forum_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    title VARCHAR(500) NOT NULL,
                    content TEXT NOT NULL,
                    image_url VARCHAR(500),
                    category VARCHAR(100),
                    is_deleted BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_reactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER REFERENCES forum_posts(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    reaction_type VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(post_id, user_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER REFERENCES forum_posts(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    is_deleted BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # New table: User follows
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_follows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    follower_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    following_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(follower_id, following_id)
                )
            """)
            
            # New table: Comment reactions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comment_reactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comment_id INTEGER REFERENCES post_comments(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    reaction_type VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(comment_id, user_id)
                )
            """)
            
            # New table: Chat conversations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    title VARCHAR(500) NOT NULL,
                    model VARCHAR(50) NOT NULL,
                    language VARCHAR(20) DEFAULT 'english',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # New table: Chat messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER REFERENCES chat_conversations(id) ON DELETE CASCADE,
                    role VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for SQLite
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_user ON forum_posts(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_category ON forum_posts(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_created ON forum_posts(created_at DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reactions_post ON post_reactions(post_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_comments_post ON post_comments(post_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_comments_user ON post_comments(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_follows_follower ON user_follows(follower_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_follows_following ON user_follows(following_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_comment_reactions ON comment_reactions(comment_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_conversations_user ON chat_conversations(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation ON chat_messages(conversation_id)")
            
            # Migration: Add image_url column if it doesn't exist
            try:
                cursor.execute("SELECT image_url FROM forum_posts LIMIT 1")
            except:
                try:
                    cursor.execute("ALTER TABLE forum_posts ADD COLUMN image_url VARCHAR(500)")
                    print("[Migration] Added image_url column to forum_posts table")
                except Exception as e:
                    print(f"[Migration] Could not add image_url column: {e}")
        else:
            # PostgreSQL table definitions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255),
                    branch VARCHAR(100),
                    role VARCHAR(50) DEFAULT 'student',
                    bio TEXT,
                    reset_token VARCHAR(255),
                    reset_token_expiry TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS forum_posts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    title VARCHAR(500) NOT NULL,
                    content TEXT NOT NULL,
                    image_url VARCHAR(500),
                    category VARCHAR(100),
                    is_deleted BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_reactions (
                    id SERIAL PRIMARY KEY,
                    post_id INTEGER REFERENCES forum_posts(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    reaction_type VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(post_id, user_id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS post_comments (
                    id SERIAL PRIMARY KEY,
                    post_id INTEGER REFERENCES forum_posts(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    is_deleted BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # New table: User follows
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_follows (
                    id SERIAL PRIMARY KEY,
                    follower_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    following_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(follower_id, following_id)
                )
            """)
            
            # New table: Comment reactions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comment_reactions (
                    id SERIAL PRIMARY KEY,
                    comment_id INTEGER REFERENCES post_comments(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    reaction_type VARCHAR(20) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(comment_id, user_id)
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_posts_user ON forum_posts(user_id);
                CREATE INDEX IF NOT EXISTS idx_posts_category ON forum_posts(category);
                CREATE INDEX IF NOT EXISTS idx_posts_created ON forum_posts(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_reactions_post ON post_reactions(post_id);
                CREATE INDEX IF NOT EXISTS idx_comments_post ON post_comments(post_id);
                CREATE INDEX IF NOT EXISTS idx_comments_user ON post_comments(user_id);
                CREATE INDEX IF NOT EXISTS idx_follows_follower ON user_follows(follower_id);
                CREATE INDEX IF NOT EXISTS idx_follows_following ON user_follows(following_id);
                CREATE INDEX IF NOT EXISTS idx_comment_reactions ON comment_reactions(comment_id);
            """)
            
            # Migration: Add image_url column if it doesn't exist (PostgreSQL)
            try:
                cursor.execute("SELECT image_url FROM forum_posts LIMIT 1")
            except:
                try:
                    cursor.execute("ALTER TABLE forum_posts ADD COLUMN image_url VARCHAR(500)")
                    print("[Migration] Added image_url column to forum_posts table (PostgreSQL)")
                except Exception as e:
                    print(f"[Migration] Could not add image_url column: {e}")
        
        conn.commit()
