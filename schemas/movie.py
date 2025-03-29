from pydantic import BaseModel
from typing import List
from models import Session, MovieAndPerson, Role, Person, MovieAndCompany, Company
from models.movie import Movie
from schemas.person import PersonSchema
from schemas.company import CompanySchema

class MovieSchema(BaseModel):
    title: str = "A Movie Title"
    poster_url: str = "https://images.com/resources/poster.png"
    running_time: int = 60
    budget: float = 1000000
    box_office: float = 2000000
    persons: List[int] = [1]
    companies: List[int] = [1]


class MovieSearchSchema(BaseModel):
    id: int

class MovieUpdateSchema(BaseModel):
    id: int
    title: str
    poster_url: str
    running_time: int
    budget: float
    box_office: float
    persons: List[int]
    companies: List[int]

class MovieDeletionSchema(BaseModel):
    message: str
    title: str

def movie_presentation(movie: Movie):
    with Session() as session:
        def get_people_by_role(role_id):
            return (
                session.query(Person)
                .join(MovieAndPerson)
                .filter(MovieAndPerson.movie_id == movie.id)
                .filter(Role.id == role_id)
                .all()
            )
        
        def get_companies_by_role(role_id):
            return (
                session.query(Company)
                .join(MovieAndCompany)
                .filter(MovieAndCompany.movie_id == movie.id)
                .filter(Role.id == role_id)
                .all()
            )
     
        
        roles = session.query(Role).all()

        list_for_each_role = {}

        for role in roles:
            people = get_people_by_role(role.id)
            companies = get_companies_by_role(role.id)

            person_list = [{"id": person.id, "name": person.name, "picture_url": person.picture_url} for person in people]
            company_list = [{"id": company.id, "name": company.name, "logo_url": company.logo_url} for company in companies]

            role_name = role.name.replace(' ','_').lower()

            list_for_each_role.update({role_name: person_list + company_list})

        movie = {
            "id": movie.id,
            "title": movie.title,
            "poster_url": movie.poster_url,
            "running_time": movie.running_time,
            "budget": movie.budget,
            "box_office": movie.box_office,
        }

        return {**movie, **list_for_each_role}

def movies_presentation(movies: List[Movie]) -> dict:
   return {
       "movies": [movie_presentation(movie) for movie in movies]
   }