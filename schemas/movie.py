from pydantic import BaseModel
from typing import List
from models import Session, MoviePersonRole, Role, Person
from models.movie import Movie

class MovieSchema(BaseModel):
    title: str = "A Movie Title"
    image_url: str = "https://images.com/resources/poster.png"
    running_time: int = 60
    budget: float = 1000000
    box_office: float = 2000000
    release_year: int = 2000

    class Config:
        extra = "allow"

class MovieSearchSchema(BaseModel):
    id: int

class MovieUpdateSchema(BaseModel):
    id: int
    title: str
    image_url: str
    running_time: int
    budget: float
    box_office: float
    release_year: int

class MovieDeletionSchema(BaseModel):
    message: str
    title: str

def movie_presentation(movie: Movie):
    with Session() as session:
        def get_people_by_role(role_id, movie_id):
            return (
                session.query(Person)
                .join(MoviePersonRole, (Person.id == MoviePersonRole.person_id) & (MoviePersonRole.movie_id == movie_id))
                .filter(MoviePersonRole.role_id == role_id)
                .all()
            )
        
        roles = session.query(Role).all()

        list_for_each_role = {}

        for role in roles:
            people = get_people_by_role(role.id, movie.id)
    
            person_list = [{"id": person.id, "name": person.name, "image_url": person.image_url} for person in people]

            role_name = role.name.replace(' ','_').lower()

            list_for_each_role.update({role_name: person_list})

        movie = {
            "id": movie.id,
            "title": movie.title,
            "image_url": movie.image_url,
            "running_time": movie.running_time,
            "budget": movie.budget,
            "box_office": movie.box_office,
            "release_year": movie.release_year,
        }

        return {**movie, **list_for_each_role}

def movies_presentation(movies: List[Movie]) -> dict:
   return {
       "movies": [movie_presentation(movie) for movie in movies]
   }