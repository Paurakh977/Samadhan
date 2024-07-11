import bcrypt

# Fixed salt for consistent hashing
fixed_salt = b'$2b$12$WMDnjnQGHfHlO7xVxtsUj.'

# Function to hash a password
def hash_password(password):
    # Hash the password using the fixed salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), fixed_salt)
    return hashed

# Function to check a password
def check_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

# Example usage
if __name__ == "__main__":
    password = "dada"
    hashed_password = hash_password(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed_password}")

    # Verify the password
    is_correct = check_password(hashed_password, "dada")
    print(f"Password is correct: {is_correct}")

   