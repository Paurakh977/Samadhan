from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base_class import Base

class User(Base):
    __tablename__ = "user_info_manual"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    phnumber = Column(String(20))
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    radio_button = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    logged_in_status = Column(Boolean, default=False)
    serial_id = Column(String(256))

    def __repr__(self):
        return f"<User {self.username}>" 