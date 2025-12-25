import bcrypt

def hash_password(password: str) -> str:
    """
    Hashes a password for secure storage.
    """
    # Convert string to bytes
    # Truncate to 72 bytes to avoid ValueError in bcrypt 5.0+
    password_bytes = password.encode('utf-8')[:72]

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # Return as a string for database storage
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain-text password matches the stored hash.
    """
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')

    # Direct bcrypt check
    return bcrypt.checkpw(password_bytes, hashed_bytes)