from models import Base
from sqlalchemy import Column, Integer, ForeignKey

class MovieAndPerson(Base):
    __tablename__ = 'movie_and_person'

    id = Column("pk_movie_and_person", Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.pk_person"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.pk_movie"), nullable=False)
    