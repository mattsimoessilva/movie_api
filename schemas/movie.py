from pydantic import BaseModel
from typing import List
from models import Session, MovieAndPerson, Role, Person, MovieAndCompany, Company
from models.movie import Movie
from schemas.person import PersonSchema
from schemas.company import CompanySchema

class MovieSchema(BaseModel):
    title: str
    poster_url: str
    running_time: int
    budget: float
    box_office: float
    directors: List[PersonSchema]
    screenwriters: List[PersonSchema]
    producers: List[PersonSchema]
    actors: List[PersonSchema]
    production_companies: List[CompanySchema]
    distribution_companies: List[CompanySchema]


class MovieSearchSchema(BaseModel):
    title: str

class MovieDeletionSchema(BaseModel):
    message: str
    title: str

class MovieViewSchema(BaseModel):
    id: int 
    title: str
    poster_url: str
    running_time: int
    budget: float
    box_office: float
    directors: List[PersonSchema]
    screenwriters: List[PersonSchema]
    producers: List[PersonSchema]
    actors: List[PersonSchema]
    production_companies: List[CompanySchema]
    distribution_companies: List[CompanySchema]


def movie_presentation(movie: Movie):
    with Session() as session:
        def get_people_by_role(role_name):
            return (
                session.query(Person.name)
                .join(MovieAndPerson)
                .filter(MovieAndPerson.movie_id == movie.id)
                .filter(Role.name == role_name)
                .all()
            )

        directors = get_people_by_role('Director')
        screenwriters = get_people_by_role('Screenwriter')
        producers = get_people_by_role('Producer')
        actors = get_people_by_role('Actor')

        def get_companies_by_role(role_name):
            return (
                session.query(Company.name)
                .join(MovieAndCompany)
                .filter(MovieAndCompany.movie_id == movie.id)
                .filter(Role.name == role_name)
                .all()
            )

        production_companies = get_companies_by_role('Production Company')
        distribution_companies = get_companies_by_role('Distribution Company')

        return {
            "id": movie.id,
            "title": movie.title,
            "poster_url": movie.poster_url,
            "running_time": movie.running_time,
            "budget": movie.budget,
            "box_office": movie.box_office,
            "directors": [director.name for director in directors],
            "screenwriters": [writer.name for writer in screenwriters],
            "producers": [producer.name for producer in producers],
            "actors": [actor.name for actor in actors],
            "production_companies": [company.name for company in production_companies],
            "distribution_companies": [company.name for company in distribution_companies],
        }

def movies_presentation(movies: List[Movie]) -> dict:
   return {
       "movies": [movie_presentation(movie) for movie in movies]
   }