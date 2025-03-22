from sqlalchemy import Column, String, Date, Integer
from model import Base

class Person(Base):
    __tablename__ = "person"

    id = Column("pk_person", Integer, primary_key=True)
    name = Column(String(100))
    birthday = Column(Date)

    def __init__(self, name:str, birthday:str):
        self.name = name
        self.birthday = birthday
        
