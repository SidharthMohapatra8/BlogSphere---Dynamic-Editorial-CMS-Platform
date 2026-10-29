"""
BlogSphere - Authentication & Security Module
Provides secure PBKDF2-HMAC-SHA256 password hashing, validation, and session tokens.
"""
import hashlib
import os
import secrets
from typing import Tuple

def hash_password(password: str) -> str:
    """Hashes a password with a random 16-byte salt using PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100_000
    )
    return f"{salt}${key.hex()}"

def verify_password(stored_hash: str, provided_password: str) -> bool:
    """Verifies a plain password against the stored salt$hash string."""
    try:
        salt, key_hex = stored_hash.split('$', 1)
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            provided_password.encode('utf-8'),
            salt.encode('utf-8'),
            100_000
        )
        return secrets.compare_digest(new_key.hex(), key_hex)
    except Exception:
        return False

def generate_session_token() -> str:
    """Generates a cryptographically strong session token."""
    return secrets.token_urlsafe(32)
