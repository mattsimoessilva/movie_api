from pydantic import BaseModel
from typing import List
from model import Session, Company, Role, CompanyAndRole, CompanyAndMovie, Movie

class CompanySchema(BaseModel):
    id: int
    name: str
    logo_url: str

class CompanySearchSchema(BaseModel):
    name: str

class CompanyDeletionSchema(BaseModel):
    message: str
    name: str

def company_presentation(company: Company) -> dict:
    with Session() as session:
        roles = (
            session.query(Role.name)
            .join(CompanyAndRole)
            .filter(CompanyAndRole.company_id == company.id)
            .all()
        )

        role_list = [role.name for role in roles]

        movies = (
            session.query(Movie.title)
            .join(CompanyAndMovie)
            .filter(CompanyAndMovie.company_id == company.id)
            .all()
        )

        movie_list = [movie.title for movie in movies]

        return {
            "id": company.id,
            "name": company.name,
            "logo_url": company.logo_url,
            "roles": role_list,
            "movies": movie_list,
        }

def companies_presentation(companies: List[Company]) -> dict:
    return {
        "companies": [company_presentation(company) for company in companies]
    }