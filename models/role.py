from sqlalchemy import Column, Text, String, Integer
from models import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "role"

    id = Column("pk_role", Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(Text(1000))

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    
