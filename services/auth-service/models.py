from sqlalchemy import Column, Integer, String
from dependencies import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, nullable = False)
    email = Column(String, unique = True, index = True, nullable = False)
    password = Column(String, nullable = False)
    profile_picture = Column(String, nullable = True)