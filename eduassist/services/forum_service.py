"""Forum service with SQLite/PostgreSQL compatibility."""

from eduassist.data.database import get_db, USE_SQLITE
from eduassist.services.auth_service import get_user_by_id

CATEGORIES = [
    "General Discussion",
    "Academic Help",
    "Exam Preparation",
    "Placements & Career",
    "Projects",
    "Campus Life",
    "Announcements"
]


def _placeholder():
    """Return the correct placeholder for the current database."""
    return "?" if USE_SQLITE else "%s"


def _dict_from_row(row):
    """Convert a database row to a dictionary."""
    if row is None:
        return None
    return dict(row)


def _false_val():
    """Return FALSE value appropriate for database."""
    return "0" if USE_SQLITE else "FALSE"


def create_post(user_id: int, title: str, content: str, category: str, image_url: str = None):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if USE_SQLITE:
            cursor.execute(f"""
                INSERT INTO forum_posts (user_id, title, content, category, image_url)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
            """, (user_id, title, content, category, image_url))
            conn.commit()
            post_id = cursor.lastrowid
            cursor.execute(f"""
                SELECT id, title, content, category, image_url, created_at
                FROM forum_posts WHERE id = {ph}
            """, (post_id,))
            post = cursor.fetchone()
        else:
            cursor.execute(f"""
                INSERT INTO forum_posts (user_id, title, content, category, image_url)
                VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
                RETURNING id, title, content, category, image_url, created_at
            """, (user_id, title, content, category, image_url))
            post = cursor.fetchone()
            conn.commit()
        
        return _dict_from_row(post)


def get_posts(page: int = 1, per_page: int = 10, category: str = None):
    offset = (page - 1) * per_page
    ph = _placeholder()
    false_val = "0" if USE_SQLITE else "FALSE"
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if category and category != "All":
            cursor.execute(f"""
                SELECT p.id, p.user_id, p.title, p.content, p.image_url, p.category, p.created_at, p.updated_at,
                       u.username, u.full_name, u.branch, u.role as user_role,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                       (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count
                FROM forum_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.is_deleted = {false_val} AND p.category = {ph}
                ORDER BY p.created_at DESC
                LIMIT {ph} OFFSET {ph}
            """, (category, per_page, offset))
        else:
            cursor.execute(f"""
                SELECT p.id, p.user_id, p.title, p.content, p.image_url, p.category, p.created_at, p.updated_at,
                       u.username, u.full_name, u.branch, u.role as user_role,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                       (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count
                FROM forum_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.is_deleted = {false_val}
                ORDER BY p.created_at DESC
                LIMIT {ph} OFFSET {ph}
            """, (per_page, offset))
        
        posts = cursor.fetchall()
        return [_dict_from_row(p) for p in posts]


def get_post_by_id(post_id: int):
    ph = _placeholder()
    false_val = "0" if USE_SQLITE else "FALSE"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT p.id, p.title, p.content, p.image_url, p.category, p.created_at, p.updated_at, p.user_id,
                   u.username, u.full_name, u.branch, u.role as user_role,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes
            FROM forum_posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = {ph} AND p.is_deleted = {false_val}
        """, (post_id,))
        
        post = cursor.fetchone()
        return _dict_from_row(post)


def toggle_reaction(post_id: int, user_id: int, reaction_type: str):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT id, reaction_type FROM post_reactions
            WHERE post_id = {ph} AND user_id = {ph}
        """, (post_id, user_id))
        
        existing = cursor.fetchone()
        
        if existing:
            existing_dict = _dict_from_row(existing)
            if existing_dict['reaction_type'] == reaction_type:
                cursor.execute(f"""
                    DELETE FROM post_reactions WHERE id = {ph}
                """, (existing_dict['id'],))
            else:
                cursor.execute(f"""
                    UPDATE post_reactions SET reaction_type = {ph} WHERE id = {ph}
                """, (reaction_type, existing_dict['id']))
        else:
            cursor.execute(f"""
                INSERT INTO post_reactions (post_id, user_id, reaction_type)
                VALUES ({ph}, {ph}, {ph})
            """, (post_id, user_id, reaction_type))
        
        conn.commit()
        return True


def get_user_reaction(post_id: int, user_id: int):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT reaction_type FROM post_reactions
            WHERE post_id = {ph} AND user_id = {ph}
        """, (post_id, user_id))
        
        result = cursor.fetchone()
        if result:
            return _dict_from_row(result)['reaction_type']
        return None


def add_comment(post_id: int, user_id: int, content: str):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if USE_SQLITE:
            cursor.execute(f"""
                INSERT INTO post_comments (post_id, user_id, content)
                VALUES ({ph}, {ph}, {ph})
            """, (post_id, user_id, content))
            conn.commit()
            comment_id = cursor.lastrowid
            cursor.execute(f"""
                SELECT id, content, created_at
                FROM post_comments WHERE id = {ph}
            """, (comment_id,))
            comment = cursor.fetchone()
        else:
            cursor.execute(f"""
                INSERT INTO post_comments (post_id, user_id, content)
                VALUES ({ph}, {ph}, {ph})
                RETURNING id, content, created_at
            """, (post_id, user_id, content))
            comment = cursor.fetchone()
            conn.commit()
        
        return _dict_from_row(comment)


def get_comments(post_id: int):
    ph = _placeholder()
    false_val = "0" if USE_SQLITE else "FALSE"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT c.id, c.content, c.created_at,
                   u.username, u.full_name, u.role as user_role
            FROM post_comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = {ph} AND c.is_deleted = {false_val}
            ORDER BY c.created_at ASC
        """, (post_id,))
        
        comments = cursor.fetchall()
        return [_dict_from_row(c) for c in comments]


def delete_post(post_id: int, user_id: int):
    user = get_user_by_id(user_id)
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT user_id FROM forum_posts WHERE id = {ph}", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return False, "Post not found"
        
        post_dict = _dict_from_row(post)
        if user['role'] != 'admin' and post_dict['user_id'] != user_id:
            return False, "Unauthorized"
        
        true_val = "1" if USE_SQLITE else "TRUE"
        cursor.execute(f"""
            UPDATE forum_posts SET is_deleted = {true_val} WHERE id = {ph}
        """, (post_id,))
        
        conn.commit()
        return True, "Post deleted"


def delete_comment(comment_id: int, user_id: int):
    user = get_user_by_id(user_id)
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT user_id FROM post_comments WHERE id = {ph}", (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            return False, "Comment not found"
        
        comment_dict = _dict_from_row(comment)
        if user['role'] != 'admin' and comment_dict['user_id'] != user_id:
            return False, "Unauthorized"
        
        true_val = "1" if USE_SQLITE else "TRUE"
        cursor.execute(f"""
            UPDATE post_comments SET is_deleted = {true_val} WHERE id = {ph}
        """, (comment_id,))
        
        conn.commit()
        return True, "Comment deleted"


def get_total_posts(category: str = None):
    ph = _placeholder()
    false_val = "0" if USE_SQLITE else "FALSE"
    
    with get_db() as conn:
        cursor = conn.cursor()
        if category and category != "All":
            cursor.execute(f"""
                SELECT COUNT(*) as count FROM forum_posts WHERE is_deleted = {false_val} AND category = {ph}
            """, (category,))
        else:
            cursor.execute(f"""
                SELECT COUNT(*) as count FROM forum_posts WHERE is_deleted = {false_val}
            """)
        result = cursor.fetchone()
        return _dict_from_row(result)['count']
