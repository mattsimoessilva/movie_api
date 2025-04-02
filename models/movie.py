from sqlalchemy import Column, Float, Integer, String
from models import Base

class Movie(Base):
    __tablename__ = 'movie'

    id = Column("pk_movie", Integer, primary_key=True)
    title = Column(String(100), unique=True)
    image_url = Column(String(2100))
    running_time = Column(Integer, nullable=False)
    budget = Column(Float, nullable=False)
    box_office = Column(Float)
    release_year = Column(Integer, nullable=True)

    def __init__(self, title:str, image_url:str,
                 running_time:int,budget:float, box_office:float,
                 release_year:int):
        self.title = title
        self.image_url = image_url
        self.running_time = running_time
        self.budget = budget
        self.box_office = box_office
        self.release_year = release_year
