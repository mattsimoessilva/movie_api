from pydantic import BaseModel
from typing import List, Optional
from models import Session, Person, Role, Movie, MoviePersonRole
import datetime

class PersonSchema(BaseModel):
    name: str = "A Person Name"
    image_url: str = "https://images.com/resources/picture.png"

class PersonSearchSchema(BaseModel):
    id: int

class PersonUpdateSchema(BaseModel):
    id: int
    name: str
    image_url: str

class PersonDeletionSchema(BaseModel):
    message: str
    name: str

def person_presentation(person: Person) -> dict:
    with Session() as session:
        roles = (
            session.query(Role)
            .join(MoviePersonRole, MoviePersonRole.role_id == Role.id)
            .filter(MoviePersonRole.person_id == person.id)
            .all()
        )

        role_list = [{"id": role.id, "name": role.name} for role in roles]

        movies = (
            session.query(Movie)
            .join(MoviePersonRole)
            .filter(MoviePersonRole.person_id == person.id)
            .all()
        )

        movie_list = [{"id": movie.id, "title": movie.title, "image_url": movie.image_url} for movie in movies]

        return {
            "id": person.id,
            "name": person.name,
            "image_url": person.image_url,
            "role": role_list, 
            "movie": movie_list,
        }
    
def people_presentation(people: List[Person]) -> dict:
    return {
        "people": [person_presentation(person) for person in people]
    }