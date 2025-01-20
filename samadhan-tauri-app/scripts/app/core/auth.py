from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# These users are only for getting access tokens
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("adminpassword"),
    },
    "test_user": {
        "username": "test_user",
        "hashed_password": pwd_context.hash("test123"),
    }
} 