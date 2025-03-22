from sqlalchemy import Column, Float, Integer, String
from model import Base

class Movie(Base):
    __tablename__ = 'movie'

    id = Column("pk_movie", Integer, primary_key=True)
    title = Column(String(100), unique=True)
    poster_url = Column(String(2100))
    running_time = Column(Integer, nullable=False)
    budget = Column(Integer, nullable=False)
    box_office = Column(Float)

    def __init__(self, title:str, poster_url:str,
                 running_time:int,budget:int, box_office:float):
        self.title = title
        self.poster_url = poster_url
        self.running_time = running_time
        self.budget = budget
        self.box_office = box_office