"""Enhanced Forum Service - New Features

This file contains additional forum service functions for:
- Search and sorting
- User follows
- Comment reactions  
- User profiles and activity
- Admin moderation tools
"""

from eduassist.data.database import get_db, USE_SQLITE
from eduassist.services.auth_service import get_user_by_id, get_user_by_email


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


def _true_val():
    """Return TRUE value appropriate for database."""
    return "1" if USE_SQLITE else "TRUE"


# ============================================================================
# SEARCH AND SORTING
# ============================================================================

def search_posts(query: str, sort_by: str = 'date', page: int = 1, per_page: int = 10):
    """
    Search posts by keywords in title or content.
    sort_by options: 'date', 'likes', 'comments'
    """
    offset = (page - 1) * per_page
    ph = _placeholder()
    false_val = _false_val()
    
    # Build ORDER BY clause
    if sort_by == 'likes':
        order_clause = "(SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') DESC"
    elif sort_by == 'comments':
        order_clause = f"(SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) DESC"
    else:  # date
        order_clause = "p.created_at DESC"
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        
        cursor.execute(f"""
            SELECT p.id, p.user_id, p.title, p.content, p.category, p.created_at, p.updated_at,
                   u.username, u.full_name, u.branch, u.role as user_role,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                   (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count
            FROM forum_posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.is_deleted = {false_val} 
              AND (p.title LIKE {ph} OR p.content LIKE {ph})
            ORDER BY {order_clause}
            LIMIT {ph} OFFSET {ph}
        """, (search_pattern, search_pattern, per_page, offset))
        
        posts = cursor.fetchall()
        return [_dict_from_row(p) for p in posts]


def get_posts_sorted(sort_by: str = 'date', category: str = None, page: int = 1, per_page: int = 10):
    """
    Get posts with sorting.
    sort_by options: 'date', 'likes', 'comments'
    """
    offset = (page - 1) * per_page
    ph = _placeholder()
    false_val = _false_val()
    
    # Build ORDER BY clause
    if sort_by == 'likes':
        order_clause = "(SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') DESC"
    elif sort_by == 'comments':
        order_clause = f"(SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) DESC"
    else:  # date
        order_clause = "p.created_at DESC"
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if category and category != "All":
            cursor.execute(f"""
                SELECT p.id, p.user_id, p.title, p.content, p.category, p.created_at, p.updated_at,
                       u.username, u.full_name, u.branch, u.role as user_role,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                       (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count
                FROM forum_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.is_deleted = {false_val} AND p.category = {ph}
                ORDER BY {order_clause}
                LIMIT {ph} OFFSET {ph}
            """, (category, per_page, offset))
        else:
            cursor.execute(f"""
                SELECT p.id, p.user_id, p.title, p.content, p.category, p.created_at, p.updated_at,
                       u.username, u.full_name, u.branch, u.role as user_role,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                       (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'dislike') as dislikes,
                       (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count
                FROM forum_posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.is_deleted = {false_val}
                ORDER BY {order_clause}
                LIMIT {ph} OFFSET {ph}
            """, (per_page, offset))
        
        posts = cursor.fetchall()
        return [_dict_from_row(p) for p in posts]


def search_users(query: str, limit: int = 10):
    """
    Search users by username or full name.
    Returns list of users matching the search query.
    """
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        
        cursor.execute(f"""
            SELECT id, username, full_name, branch, role, bio
            FROM users
            WHERE username LIKE {ph} OR full_name LIKE {ph}
            ORDER BY username ASC
            LIMIT {ph}
        """, (search_pattern, search_pattern, limit))
        
        users = cursor.fetchall()
        return [_dict_from_row(u) for u in users]


# ============================================================================
# USER FOLLOWS
# ============================================================================

def follow_user(follower_id: int, following_id: int):
    """Follow a user."""
    if follower_id == following_id:
        return False, "Cannot follow yourself"
    
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                INSERT INTO user_follows (follower_id, following_id)
                VALUES ({ph}, {ph})
            """, (follower_id, following_id))
            conn.commit()
            return True, "Followed successfully"
        except:
            return False, "Already following"


def unfollow_user(follower_id: int, following_id: int):
    """Unfollow a user."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            DELETE FROM user_follows
            WHERE follower_id = {ph} AND following_id = {ph}
        """, (follower_id, following_id))
        
        conn.commit()
        return True, "Unfollowed successfully"


def is_following(follower_id: int, following_id: int):
    """Check if user is following another user."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT id FROM user_follows
            WHERE follower_id = {ph} AND following_id = {ph}
        """, (follower_id, following_id))
        
        return cursor.fetchone() is not None


def get_followers(user_id: int):
    """Get list of followers for a user."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT u.id, u.username, u.full_name, u.branch, u.role, uf.created_at as followed_at
            FROM user_follows uf
            JOIN users u ON uf.follower_id = u.id
            WHERE uf.following_id = {ph}
            ORDER BY uf.created_at DESC
        """, (user_id,))
        
        followers = cursor.fetchall()
        return [_dict_from_row(f) for f in followers]


def get_following(user_id: int):
    """Get list of users that a user is following."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT u.id, u.username, u.full_name, u.branch, u.role, uf.created_at as followed_at
            FROM user_follows uf
            JOIN users u ON uf.following_id = u.id
            WHERE uf.follower_id = {ph}
            ORDER BY uf.created_at DESC
        """, (user_id,))
        
        following = cursor.fetchall()
        return [_dict_from_row(f) for f in following]


# ============================================================================
# COMMENT REACTIONS
# ============================================================================

def toggle_comment_reaction(comment_id: int, user_id: int, reaction_type: str):
    """Toggle like/dislike on a comment."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT id, reaction_type FROM comment_reactions
            WHERE comment_id = {ph} AND user_id = {ph}
        """, (comment_id, user_id))
        
        existing = cursor.fetchone()
        
        if existing:
            existing_dict = _dict_from_row(existing)
            if existing_dict['reaction_type'] == reaction_type:
                cursor.execute(f"""
                    DELETE FROM comment_reactions WHERE id = {ph}
                """, (existing_dict['id'],))
            else:
                cursor.execute(f"""
                    UPDATE comment_reactions SET reaction_type = {ph} WHERE id = {ph}
                """, (reaction_type, existing_dict['id']))
        else:
            cursor.execute(f"""
                INSERT INTO comment_reactions (comment_id, user_id, reaction_type)
                VALUES ({ph}, {ph}, {ph})
            """, (comment_id, user_id, reaction_type))
        
        conn.commit()
        return True


def get_comments_with_reactions(post_id: int, current_user_id: int = None):
    """Get comments with reaction counts and user's reaction."""
    ph = _placeholder()
    false_val = _false_val()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if current_user_id:
            cursor.execute(f"""
                SELECT c.id, c.content, c.created_at, c.user_id,
                       u.username, u.full_name, u.role as user_role,
                       (SELECT COUNT(*) FROM comment_reactions WHERE comment_id = c.id AND reaction_type = 'like') as likes,
                       (SELECT reaction_type FROM comment_reactions WHERE comment_id = c.id AND user_id = {ph}) as user_reaction
                FROM post_comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = {ph} AND c.is_deleted = {false_val}
                ORDER BY c.created_at ASC
            """, (current_user_id, post_id))
        else:
            cursor.execute(f"""
                SELECT c.id, c.content, c.created_at, c.user_id,
                       u.username, u.full_name, u.role as user_role,
                       (SELECT COUNT(*) FROM comment_reactions WHERE comment_id = c.id AND reaction_type = 'like') as likes
                FROM post_comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = {ph} AND c.is_deleted = {false_val}
                ORDER BY c.created_at ASC
            """, (post_id,))
        
        comments = cursor.fetchall()
        return [_dict_from_row(c) for c in comments]


# ============================================================================
# USER PROFILE AND ACTIVITY
# ============================================================================

def get_user_profile(user_id: int):
    """Get comprehensive user profile with stats."""
    ph = _placeholder()
    false_val = _false_val()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Get user info
        cursor.execute(f"""
            SELECT id, username, email, full_name, branch, role, bio, created_at
            FROM users WHERE id = {ph}
        """, (user_id,))
        
        user = _dict_from_row(cursor.fetchone())
        
        if not user:
            return None
        
        # Get stats
        cursor.execute(f"""
            SELECT COUNT(*) as count FROM forum_posts 
            WHERE user_id = {ph} AND is_deleted = {false_val}
        """, (user_id,))
        user['post_count'] = _dict_from_row(cursor.fetchone())['count']
        
        cursor.execute(f"""
            SELECT COUNT(*) as count FROM post_comments 
            WHERE user_id = {ph} AND is_deleted = {false_val}
        """, (user_id,))
        user['comment_count'] = _dict_from_row(cursor.fetchone())['count']
        
        cursor.execute(f"""
            SELECT COUNT(*) as count FROM user_follows WHERE follower_id = {ph}
        """, (user_id,))
        user['following_count'] = _dict_from_row(cursor.fetchone())['count']
        
        cursor.execute(f"""
            SELECT COUNT(*) as count FROM user_follows WHERE following_id = {ph}
        """, (user_id,))
        user['followers_count'] = _dict_from_row(cursor.fetchone())['count']
        
        # Get total likes received on posts
        cursor.execute(f"""
            SELECT COUNT(*) as count FROM post_reactions pr
            JOIN forum_posts p ON pr.post_id = p.id
            WHERE p.user_id = {ph} AND pr.reaction_type = 'like'
        """, (user_id,))
        user['likes_received'] = _dict_from_row(cursor.fetchone())['count']
        
        return user


def get_user_posts(user_id: int, page: int = 1, per_page: int = 10):
    """Get posts created by a user."""
    offset = (page - 1) * per_page
    ph = _placeholder()
    false_val = _false_val()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT p.id, p.title, p.content, p.category, p.created_at,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                   (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count
            FROM forum_posts p
            WHERE p.user_id = {ph} AND p.is_deleted = {false_val}
            ORDER BY p.created_at DESC
            LIMIT {ph} OFFSET {ph}
        """, (user_id, per_page, offset))
        
        posts = cursor.fetchall()
        return [_dict_from_row(p) for p in posts]


def get_user_comments(user_id: int, page: int = 1, per_page: int = 10):
    """Get comments made by a user."""
    offset = (page - 1) * per_page
    ph = _placeholder()
    false_val = _false_val()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT c.id, c.content, c.created_at, c.post_id,
                   p.title as post_title,
                   (SELECT COUNT(*) FROM comment_reactions WHERE comment_id = c.id AND reaction_type = 'like') as likes
            FROM post_comments c
            JOIN forum_posts p ON c.post_id = p.id
            WHERE c.user_id = {ph} AND c.is_deleted = {false_val}
            ORDER BY c.created_at DESC
            LIMIT {ph} OFFSET {ph}
        """, (user_id, per_page, offset))
        
        comments = cursor.fetchall()
        return [_dict_from_row(c) for c in comments]


def get_user_liked_posts(user_id: int, page: int = 1, per_page: int = 10):
    """Get posts liked by a user."""
    offset = (page - 1) * per_page
    ph = _placeholder()
    false_val = _false_val()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT p.id, p.title, p.content, p.category, p.created_at, p.user_id,
                   u.username, u.full_name,
                   (SELECT COUNT(*) FROM post_reactions WHERE post_id = p.id AND reaction_type = 'like') as likes,
                   (SELECT COUNT(*) FROM post_comments WHERE post_id = p.id AND is_deleted = {false_val}) as comment_count,
                   pr.created_at as liked_at
            FROM post_reactions pr
            JOIN forum_posts p ON pr.post_id = p.id
            JOIN users u ON p.user_id = u.id
            WHERE pr.user_id = {ph} AND pr.reaction_type = 'like' AND p.is_deleted = {false_val}
            ORDER BY pr.created_at DESC
            LIMIT {ph} OFFSET {ph}
        """, (user_id, per_page, offset))
        
        posts = cursor.fetchall()
        return [_dict_from_row(p) for p in posts]


def update_user_bio(user_id: int, bio: str):
    """Update user's bio."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            UPDATE users SET bio = {ph} WHERE id = {ph}
        """, (bio, user_id))
        
        conn.commit()
        return True


# ============================================================================
# ADMIN FUNCTIONS
# ============================================================================

def promote_to_admin(admin_user_id: int, target_email: str):
    """Promote a user to admin role (admin only)."""
    admin = get_user_by_id(admin_user_id)
    
    if admin['role'] != 'admin':
        return False, "Unauthorized: Only admins can promote users"
    
    target_user = get_user_by_email(target_email)
    
    if not target_user:
        return False, "User not found"
    
    if target_user['role'] == 'admin':
        return False, "User is already an admin"
    
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            UPDATE users SET role = 'admin' WHERE id = {ph}
        """, (target_user['id'],))
        
        conn.commit()
        return True, f"Successfully promoted {target_user['username']} to admin"


def demote_from_admin(admin_user_id: int, target_email: str):
    """Demote an admin to student role (admin only)."""
    admin = get_user_by_id(admin_user_id)
    
    if admin['role'] != 'admin':
        return False, "Unauthorized: Only admins can demote users"
    
    target_user = get_user_by_email(target_email)
    
    if not target_user:
        return False, "User not found"
    
    if target_user['id'] == admin_user_id:
        return False, "Cannot demote yourself"
    
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f"""
            UPDATE users SET role = 'student' WHERE id = {ph}
        """, (target_user['id'],))
        
        conn.commit()
        return True, f"Successfully demoted {target_user['username']} to student"


def get_all_admins():
    """Get list of all admin users."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, full_name, branch, created_at
            FROM users WHERE role = 'admin'
            ORDER BY created_at ASC
        """)
        
        admins = cursor.fetchall()
        return [_dict_from_row(a) for a in admins]
