from models import Base
from sqlalchemy import Column, Integer, ForeignKey

class MoviePersonRole(Base):
    __tablename__ = 'movie_person_role'

    id = Column("pk_movie_person_role", Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie.pk_movie"), nullable=False)
    person_id = Column(Integer, ForeignKey("person.pk_person"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.pk_role"), nullable=False)
    