from pydantic import BaseModel
from typing import List, Optional
from models import Session, Person, Role, PersonAndRole, Movie, MovieAndPerson

class PersonSchema(BaseModel):
    id: int
    name: str
    birthday: str

class PersonSearchSchema(BaseModel):
    name: str

class PersonDeletionSchema(BaseModel):
    message: str
    name: str

def person_presentation(person: Person) -> dict:
    with Session() as session:
        roles = (
            session.query(Role.name)
            .join(PersonAndRole)
            .filter(PersonAndRole.person_id == person.id)
            .all()
        )

        role_list = [role.name for role in roles]

        movies = (
            session.query(Movie.title)
            .join(MovieAndPerson)
            .filter(MovieAndPerson.person_id == person.id)
            .all()
        )

        movie_list = [movie.title for movie in movies]

        return {
            "id": person.id,
            "name": person.name,
            "birthday": person.birthday,
            "roles": role_list, 
            "movies": movie_list,
        }
    
def persons_presentation(persons: List[Person]) -> dict:
    return {
        "persons": [person_presentation(person) for person in persons]
    }