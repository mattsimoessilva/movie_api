from sqlalchemy import Integer, Column, String
from model import Base

class Company(Base):
    __tablename__ = 'company'

    id = Column("pk_company", Integer, primary_key=True)
    name = Column(String(140))
    logo_url = Column(String(2100))

    def __init__(self, name:str, logo_url:str):
        self.name = name
        self.logo_url = logo_url
