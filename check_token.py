import sqlite3
from datetime import datetime

conn = sqlite3.connect('eduassist.db')
cursor = conn.cursor()

# Check tokens
cursor.execute("SELECT email, reset_token, reset_token_expiry FROM users WHERE reset_token IS NOT NULL")
rows = cursor.fetchall()

print("Current tokens in database:")
print("-" * 80)
for row in rows:
    email, token, expiry = row
    print(f"Email: {email}")
    print(f"Token: {token[:20]}...")
    print(f"Expiry (stored): {expiry}")
    print(f"Expiry type: {type(expiry)}")
    
    # Try to parse it
    try:
        if expiry:
            # Parse the ISO format
            expiry_dt = datetime.fromisoformat(expiry)
            now = datetime.now()
            print(f"Expiry (parsed): {expiry_dt}")
            print(f"Now: {now}")
            print(f"Now (ISO): {now.isoformat()}")
            print(f"Is valid? {expiry_dt > now}")
            print(f"String comparison: '{expiry}' > '{now.isoformat()}' = {expiry > now.isoformat()}")
    except Exception as e:
        print(f"Error parsing: {e}")
    print("-" * 80)

conn.close()
