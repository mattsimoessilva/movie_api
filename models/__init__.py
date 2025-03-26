from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from models.base import Base
from models.movie import Movie
from models.company import Company
from models.company_and_role import CompanyAndRole
from models.movie_and_person import MovieAndPerson
from models.person import Person
from models.person_and_role import PersonAndRole
from models.movie_and_company import MovieAndCompany
from models.role import Role

db_path = "database/"

if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = 'sqlite:///%s/db.sqlite3' % db_path

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)