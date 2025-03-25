from sqlalchemy import Column, Text, String
from model import Base

class Role(Base):
    __tablename__ = "role"

    name = Column("pk_role", String(50), unique=True)
    description = Column(Text(1000))

    def __init__(self, name:str, description:str):
        self.name = name
        self.description = description

    
