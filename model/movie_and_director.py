from model import Base
from sqlalchemy import Column, Integer, ForeignKey

class MovieAndDirector(Base):
    __tablename__ = 'movie_and_director'

    id = Column("pk_movie_and_director", Integer, primary_key=True)
    director = Column(Integer, ForeignKey("director.pk_director"), nullable=False)
    movie = Column(Integer, ForeignKey("movie.pk_movie"), nullable=False)

    def __init__(self, director:int, movie:int):
        self.director = director
        self.movie = movie

    