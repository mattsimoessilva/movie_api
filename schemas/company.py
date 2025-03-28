from pydantic import BaseModel
from typing import List
from models import Session, Company, Role, CompanyAndRole, MovieAndCompany, Movie

class CompanySchema(BaseModel):
    name: str = "A Company Name"
    logo_url: str = "https://images.com/resources/logo.png"
    roles: List[int] = [1]

class CompanySearchSchema(BaseModel):
    id: int

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
            .join(MovieAndCompany)
            .filter(MovieAndCompany.company_id == company.id)
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