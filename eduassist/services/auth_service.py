"""Authentication service with SQLite/PostgreSQL compatibility."""

import bcrypt
import secrets
from datetime import datetime, timedelta
from eduassist.data.database import get_db, USE_SQLITE

BRANCHES = [
    "CSE",
    "CSE (AI & ML)",
    "CSE (Cyber Security)",
    "CSE (Data Science)",
    "ECE",
    "EEE",
    "MECH",
    "CIVIL",
    "CHEMICAL",
    "IT",
    "Aeronautical",
    "Other"
]

ROLES = ["student", "teacher", "admin"]


def _placeholder():
    """Return the correct placeholder for the current database."""
    return "?" if USE_SQLITE else "%s"


def _dict_from_row(row):
    """Convert a database row to a dictionary."""
    if row is None:
        return None
    if USE_SQLITE:
        return dict(row)
    return dict(row)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def create_user(username: str, email: str, password: str, full_name: str, branch: str, role: str = "student"):
    password_hash = hash_password(password)
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            if USE_SQLITE:
                cursor.execute(f"""
                    INSERT INTO users (username, email, password_hash, full_name, branch, role)
                    VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                """, (username, email, password_hash, full_name, branch, role))
                conn.commit()
                user_id = cursor.lastrowid
                cursor.execute(f"""
                    SELECT id, username, email, full_name, branch, role
                    FROM users WHERE id = {ph}
                """, (user_id,))
                user = cursor.fetchone()
            else:
                cursor.execute(f"""
                    INSERT INTO users (username, email, password_hash, full_name, branch, role)
                    VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph})
                    RETURNING id, username, email, full_name, branch, role
                """, (username, email, password_hash, full_name, branch, role))
                user = cursor.fetchone()
                conn.commit()
            
            return _dict_from_row(user), None
        except Exception as e:
            error_msg = str(e).lower()
            if "unique" in error_msg or "duplicate" in error_msg:
                if "username" in error_msg:
                    return None, "Username already exists"
                elif "email" in error_msg:
                    return None, "Email already exists"
                return None, "Username or email already exists"
            return None, str(e)


def authenticate_user(username_or_email: str, password: str):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, username, email, password_hash, full_name, branch, role
            FROM users
            WHERE username = {ph} OR email = {ph}
        """, (username_or_email, username_or_email))
        
        user = cursor.fetchone()
        
        if user:
            user_dict = _dict_from_row(user)
            if verify_password(password, user_dict['password_hash']):
                del user_dict['password_hash']
                return user_dict, None
        
        return None, "Invalid credentials"


def get_user_by_id(user_id: int):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, username, email, full_name, branch, role, created_at
            FROM users
            WHERE id = {ph}
        """, (user_id,))
        
        user = cursor.fetchone()
        return _dict_from_row(user)


def get_user_by_email(email: str):
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, username, email, full_name, branch, role
            FROM users
            WHERE email = {ph}
        """, (email,))
        
        user = cursor.fetchone()
        return _dict_from_row(user)


def get_user_by_username(username: str):
    """Get user by username for profile lookups."""
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, username, email, full_name, branch, role
            FROM users
            WHERE username = {ph}
        """, (username,))
        
        user = cursor.fetchone()
        return _dict_from_row(user)



def generate_reset_token(email: str):
    token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(hours=1)
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        if USE_SQLITE:
            cursor.execute(f"""
                UPDATE users
                SET reset_token = {ph}, reset_token_expiry = {ph}
                WHERE email = {ph}
            """, (token, expiry.isoformat(), email))
            conn.commit()
            if cursor.rowcount > 0:
                return token
            return None
        else:
            cursor.execute(f"""
                UPDATE users
                SET reset_token = {ph}, reset_token_expiry = {ph}
                WHERE email = {ph}
                RETURNING id
            """, (token, expiry, email))
            result = cursor.fetchone()
            conn.commit()
            if result:
                return token
            return None


def reset_password_with_token(token: str, new_password: str):
    ph = _placeholder()
    now = datetime.now()
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # First check if token exists at all
        cursor.execute(f"""
            SELECT id, email, reset_token_expiry FROM users
            WHERE reset_token = {ph}
        """, (token,))
        
        token_user = cursor.fetchone()
        
        if not token_user:
            return False, "Invalid reset link. This link may have been replaced by a newer password reset request. Please request a new password reset."
        
        # Token exists, now check if it's expired
        token_dict = _dict_from_row(token_user)
        
        if USE_SQLITE:
            # For SQLite, compare ISO strings
            expiry_str = token_dict['reset_token_expiry']
            if expiry_str <= now.isoformat():
                return False, "This reset link has expired. Password reset links are valid for 1 hour. Please request a new password reset."
        else:
            # For PostgreSQL, compare datetime objects
            expiry_dt = token_dict['reset_token_expiry']
            if expiry_dt <= now:
                return False, "This reset link has expired. Password reset links are valid for 1 hour. Please request a new password reset."
        
        # Token is valid, proceed with password reset
        new_hash = hash_password(new_password)
        
        cursor.execute(f"""
            UPDATE users
            SET password_hash = {ph}, reset_token = NULL, reset_token_expiry = NULL
            WHERE id = {ph}
        """, (new_hash, token_dict['id']))
        
        conn.commit()
        return True, "Password reset successfully"


def update_user_role(user_id: int, new_role: str, admin_id: int):
    admin = get_user_by_id(admin_id)
    if not admin or admin['role'] != 'admin':
        return False, "Unauthorized"
    
    if new_role not in ROLES:
        return False, "Invalid role"
    
    ph = _placeholder()
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE users SET role = {ph} WHERE id = {ph}
        """, (new_role, user_id))
        conn.commit()
        return True, "Role updated"
