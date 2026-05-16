import sqlite3

conn = sqlite3.connect('eduassist.db')
cursor = conn.cursor()

# Get the latest token
cursor.execute("SELECT email, reset_token FROM users WHERE email = 'mf9315268@gmail.com'")
result = cursor.fetchone()

if result:
    email, token = result
    print(f"Email: {email}")
    print(f"Token: {token}")
    print(f"\nReset URL: http://127.0.0.1:5000/reset-password/{token}")
else:
    print("No token found")

conn.close()
