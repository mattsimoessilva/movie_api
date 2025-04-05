from models import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class MoviePersonRole(Base):
    __tablename__ = 'movie_person_role'

    id = Column("pk_movie_person_role", Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie.pk_movie", ondelete="CASCADE"), nullable=False)
    person_id = Column(Integer, ForeignKey("person.pk_person", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.pk_role", ondelete="CASCADE"), nullable=False)
    
    movie = relationship("Movie", back_populates="movie_person_roles")
    role = relationship("Role", back_populates="movie_person_roles")
    person = relationship("Person", back_populates="movie_person_roles")