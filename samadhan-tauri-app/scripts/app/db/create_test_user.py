from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User, AuthType
import bcrypt

# Fixed salt for consistent hashing
FIXED_SALT = b"$2b$12$WMDnjnQGHfHlO7xVxtsUj."

def hash_password(password: str) -> str:
    """Hash password using fixed salt"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), FIXED_SALT)
    return hashed.decode("utf-8")

def create_test_user():
    db = SessionLocal()
    try:
        # Check if test user exists
        test_user = db.query(User).filter(User.email == "dada@gmail.com").first()
        if not test_user:
            # Hash password with fixed salt
            hashed_password = hash_password("dada")
            print(f"Creating test user with password hash: {hashed_password}")
            
            # Create test user
            test_user = User(
                username="dada",
                email="dada@gmail.com",
                password=hashed_password,
                auth_type=AuthType.MANUAL
            )
            db.add(test_user)
            db.commit()
            print("Test user created successfully!")
        else:
            print(f"Test user already exists with password hash: {test_user.password}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 