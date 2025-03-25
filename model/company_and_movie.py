from sqlalchemy import Column, Integer, ForeignKey
from model import Base
from sqlalchemy.orm import relationship

class CompanyAndMovie(Base):
    __tablename__ = 'company_and_movie'

    id = Column("pk_company_and_movie", Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.pk_company"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.pk_movie"), nullable=False)

    company = relationship("Company")
    movie = relationship("Movie")