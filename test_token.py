import secrets

# Test token generation
token1 = secrets.token_urlsafe(32)
token2 = secrets.token_urlsafe(32)

print("Token 1:", token1)
print("Token 2:", token2)
print()
print("Token 1 length:", len(token1))
print("Token 2 length:", len(token2))
print()
print("Characters in token 1:", set(token1))
print("Characters in token 2:", set(token2))

# Check if they contain URL-safe characters
import string
url_safe = string.ascii_letters + string.digits + '-_'
print()
print("All characters URL-safe in token 1?", all(c in url_safe for c in token1))
print("All characters URL-safe in token 2?", all(c in url_safe for c in token2))
