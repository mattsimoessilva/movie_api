from sqlalchemy import Column, Integer, ForeignKey
from models import Base

class MovieAndCompany(Base):
    __tablename__ = 'movie_and_company'

    id = Column("pk_movie_and_company", Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.pk_company"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.pk_movie"), nullable=False)
