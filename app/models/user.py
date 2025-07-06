from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    password_hash = Column(String, nullable=False)

    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    cars = relationship("Car", back_populates="owner")

