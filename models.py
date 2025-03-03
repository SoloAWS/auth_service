from sqlalchemy import Column, String
from database import Base

class TokenModel(Base):
    __tablename__ = "tokens"
    
    token = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)