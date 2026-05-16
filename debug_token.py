import sqlite3
from datetime import datetime

# Simulate the exact query from auth_service.py
conn = sqlite3.connect('eduassist.db')
cursor = conn.cursor()

# Get the token from the URL in the screenshot
token_from_url = "wKGk42Mppla-q6WURlD5RDjQRlSuIICn4makV4W_g7k"

now = datetime.now()
now_iso = now.isoformat()

print(f"Token from URL: {token_from_url}")
print(f"Current time: {now}")
print(f"Current time (ISO): {now_iso}")
print()

# Try the exact query from the code
cursor.execute("""
    SELECT id, email, reset_token, reset_token_expiry FROM users
    WHERE reset_token = ? AND reset_token_expiry > ?
""", (token_from_url, now_iso))

result = cursor.fetchone()

print("Query result:", result)

if result:
    print("Token is valid!")
    print(f"User ID: {result[0]}")
    print(f"Email: {result[1]}")
else:
    print("Token not found or expired")
    
    # Check if token exists at all
    cursor.execute("SELECT id, email, reset_token, reset_token_expiry FROM users WHERE reset_token = ?", (token_from_url,))
    token_check = cursor.fetchone()
    
    if token_check:
        print(f"Token exists but failed expiry check:")
        print(f"  Stored expiry: {token_check[3]}")
        print(f"  Current time: {now_iso}")
        print(f"  Comparison: '{token_check[3]}' > '{now_iso}' = {token_check[3] > now_iso}")
    else:
        print("Token doesn't exist in database at all")
        print("\nAll tokens in database:")
        cursor.execute("SELECT email, reset_token FROM users WHERE reset_token IS NOT NULL")
        all_tokens = cursor.fetchall()
        for email, token in all_tokens:
            print(f"  {email}: {token}")

conn.close()
