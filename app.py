from flask_openapi3 import OpenAPI, Tag, Info
import json
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from schemas import *
from models import *
from sqlalchemy.exc import IntegrityError

info = Info(title="Movie API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc or RapiDoc")
movie_tag = Tag(name="Movie", description="Adding, viewing, updating, and removing movies")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


@app.post('/movie', tags=[movie_tag],
          responses={"200": MovieViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_movie(form: MovieSchema):
    with Session() as session:
        movie = Movie(
            title = form.title,
            poster_url = form.poster_url,
            running_time = form.running_time,
            budget = form.budget,
            box_office = form.box_office,
        )

        try:
            session.add(movie)
            session.commit()
        
        except IntegrityError as e:
            error_msg = "Movie already registered in the database"

            return {"message": error_msg}, 409
        
        except Exception as e:
            error_msg = "It wasn't possible to register a new movie"

            return {"message": error_msg}, 400
        
        movie_and_person_list = []

        for person in form.persons:
            movie_and_person = MovieAndPerson(
                person_id = person.id,
                movie_id = movie.id
            )
            movie_and_person_list.append(movie_and_person)

        try:
            session.bulk_save_objects(movie_and_person_list)
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to register add people to the movie"

            return {"message": error_msg}, 400
        
        movie_and_company_list = []

        for company in form.companies:
            movie_and_company = MovieAndCompany(
                company_id = company.id,
                movie_id = movie.id
            )
            movie_and_company_list.append(movie_and_company)

        try:
            session.bulk_save_objects(movie_and_company_list)
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to register add companies to the movie"

            return {"message": error_msg}, 400
        
        return movie_presentation(movie), 200








        

            

