from pydantic import BaseModel
from typing import List, Optional
from models import Session, Person, Role, PersonAndRole, Movie, MovieAndPerson
import datetime

class PersonSchema(BaseModel):
    name: str = "A Person Name"
    picture_url: str = "https://images.com/resources/picture.png"
    roles: List[int] = [1]

class PersonSearchSchema(BaseModel):
    id: int

class PersonUpdateSchema(BaseModel):
    id: int
    name: str
    picture_url: str

class PersonDeletionSchema(BaseModel):
    message: str
    name: str

def person_presentation(person: Person) -> dict:
    with Session() as session:
        roles = (
            session.query(Role)
            .join(PersonAndRole)
            .filter(PersonAndRole.person_id == person.id)
            .all()
        )

        role_list = [{"id": role.id, "name": role.name} for role in roles]

        movies = (
            session.query(Movie)
            .join(MovieAndPerson)
            .filter(MovieAndPerson.person_id == person.id)
            .all()
        )

        movie_list = [{"id": movie.id, "title": movie.title, "poster_url": movie.poster_url} for movie in movies]

        return {
            "id": person.id,
            "name": person.name,
            "picture_url": person.picture_url,
            "roles": role_list, 
            "movies": movie_list,
        }
    
def people_presentation(persons: List[Person]) -> dict:
    return {
        "persons": [person_presentation(person) for person in persons]
    }