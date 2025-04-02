from sqlalchemy import Column, String, Date, Integer
from models import Base

class Person(Base):
    __tablename__ = "person"

    id = Column("pk_person", Integer, primary_key=True)
    name = Column(String(100))
    image_url = Column(String(2100))

    def __init__(self, name:str, image_url:str):
        self.name = name
        self.image_url = image_url
        
