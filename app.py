from flask_openapi3 import OpenAPI, Tag, Info
import json
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from schemas import *
from models import *
from sqlalchemy.exc import IntegrityError
import datetime

info = Info(title="Movie API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc or RapiDoc")
movie_tag = Tag(name="Movie", description="Adding, viewing, updating, and removing movies")
role_tag = Tag(name="Role", description="Adding, viewing, updating, and removing roles")
person_tag = Tag(name="Person", description="Adding, viewing, updating, and removing people")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

# MOVIE

@app.post('/movie', tags=[movie_tag],
          responses={"200": MovieSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_movie(form: MovieSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in vars(form) if field not in optional_fields and not getattr(form, field)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        movie = Movie(
            title = form.title,
            image_url = form.image_url,
            running_time = form.running_time,
            budget = form.budget,
            box_office = form.box_office,
            release_year = form.release_year,
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

        for person_id in form.people:
            movie_and_person = MovieAndPerson(
                person_id = person_id,
                movie_id = movie.id
            )
            movie_and_person_list.append(movie_and_person)

        try:
            session.bulk_save_objects(movie_and_person_list)
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to add people to the movie"

            return {"message": error_msg}, 400
        
        return movie_presentation(movie), 200


@app.get('/movies', tags=[movie_tag],
         responses={"200": MovieSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_movies():
    with Session() as session:
       movies = session.query(Movie).all()

       if not movies:
           return {"movies": []}, 200
       else:
           return movies_presentation(movies), 200


@app.get('/movie', tags=[movie_tag],
         responses={"200": MovieSchema, "404": ErrorSchema})
def get_movie(query: MovieSearchSchema):
    with Session() as session:
        movie_id = query.id

        movie = session.query(Movie).filter(Movie.id == movie_id).first()

        if not movie:
            error_msg = "Movie not found"
            return {"message": error_msg}, 404
        else:
            return movie_presentation(movie), 200
        
@app.put('/movie', tags=[movie_tag],
         responses={"200": MovieUpdateSchema, "404": ErrorSchema})
def update_movie(form: MovieUpdateSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in vars(form) if field not in optional_fields and not getattr(form, field)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        movie = session.query(Movie).filter(Movie.id == form.id).first()

        movie.title = form.title
        movie.image_url = form.image_url
        movie.running_time = form.running_time
        movie.budget = form.budget
        movie.box_office = form.box_office
        movie.release_year = form.release_year

        try:
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to update the movie"

            return {"message": error_msg}, 400
        
        movie_with_people = movie_presentation(movie)
        
        existing_people = set()

        for field_name, values in movie_with_people.items():
            if isinstance(values, list):  
                existing_people.update(person["id"] for person in values if isinstance(person["id"], int))

        new_people = set(form.people)

        to_add = new_people - existing_people
        to_remove = existing_people - new_people

        try:
            if to_remove:
                session.query(MovieAndPerson).filter(
                    MovieAndPerson.person_id.in_(to_remove),
                    MovieAndPerson.movie_id == movie.id
                ).delete(synchronize_session=False)

            movie_and_person_list = [MovieAndPerson(person_id=person_id, movie_id=movie.id) for person_id in to_add]
            if movie_and_person_list:
                session.bulk_save_objects(movie_and_person_list)

            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to update the people who worked on the movie"

            return {"message": error_msg}, 400

        return movie_presentation(movie), 200
    

@app.delete('/movie', tags=[movie_tag],
            responses={"200": MovieDeletionSchema, "404": ErrorSchema})
def delete_movie(query: MovieSearchSchema):
    with Session() as session:
        movie_id = query.id

        movie = session.query(Movie).filter(Movie.id == movie_id).delete()
        session.commit()

        if movie:
            return {"message": "Movie deleted", "id": movie_id}
        else:
            error_msg = "Movie not found"
            return {"message": error_msg}, 404

# ROLE

@app.post('/role', tags=[role_tag],
          responses={"200": RoleSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_role(form: RoleSchema):
    optional_fields = {}
    missing_fields = [field for field in vars(form) if field not in optional_fields and not getattr(form, field)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        role = Role(
            name = form.name,
            description = form.description,
        )

        try:
            session.add(role)
            session.commit()
        
        except IntegrityError as e:
            error_msg = "Role already registered in the database"

            return {"message": error_msg}, 409
        
        except Exception as e:
            error_msg = "It wasn't possible to register a new role"

            return {"message": error_msg}, 400
        
        return role_presentation(role), 200


@app.get('/roles', tags=[role_tag],
         responses={"200": RoleSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_roles():
    with Session() as session:
       roles = session.query(Role).all()

       if not roles:
           return {"roles": []}, 200
       else:
           return roles_presentation(roles), 200


@app.get('/role', tags=[role_tag],
         responses={"200": RoleSchema, "404": ErrorSchema})
def get_role(query: RoleSearchSchema):
    with Session() as session:
        role_id = query.id

        role = session.query(Role).filter(Role.id == role_id).first()

        if not role:
            error_msg = "Role not found"
            return {"message": error_msg}, 404
        else:
            return role_presentation(role), 200
      

@app.put('/role', tags=[role_tag],
         responses={"200": RoleUpdateSchema, "404": ErrorSchema})
def update_role(form: RoleUpdateSchema):
    optional_fields = {}
    missing_fields = [field for field in vars(form) if field not in optional_fields and not getattr(form, field)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        role = session.query(Role).filter(Role.id == form.id).first()

        role.name = form.name
        role.description = form.description

        try:
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to update the role"

            return {"message": error_msg}, 400

        return role_presentation(role), 200

        
@app.delete('/role', tags=[role_tag],
            responses={"200": RoleDeletionSchema, "404": ErrorSchema})
def delete_role(query: RoleSearchSchema):
    with Session() as session:
        role_id = query.id

        role = session.query(Role).filter(Role.id == role_id).delete()
        session.commit()

        if role:
            return {"message": "Role deleted", "id": role_id}
        else:
            error_msg = "Role not found"
            return {"message": error_msg}, 404

# PERSON
            
@app.post('/person', tags=[person_tag],
          responses={"200": PersonSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_person(form: PersonSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in vars(form) if field not in optional_fields and not getattr(form, field)]

    if missing_fields:
        error_msg = f"Missing required fields [{', '.join(missing_fields)}]";
        return jsonify({"message": error_msg}), 400
    
    with Session() as session:
        person = Person(
            name = form.name,
            image_url = form.image_url,
        )

        try:
            session.add(person)
            session.commit()
        
        except IntegrityError as e:
            error_msg = "Person already registered in the database"

            return {"message": error_msg}, 409
        
        except Exception as e:
            error_msg = "It wasn't possible to register a new person"

            return {"message": error_msg}, 400
        
        person_and_role_list = []

        for role_id in form.roles:
            person_and_role = PersonAndRole(
                person_id = person.id,
                role_id = role_id
            )
            person_and_role_list.append(person_and_role)

        try:
            session.bulk_save_objects(person_and_role_list)
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to add roles to the person"

            return {"message": error_msg}, 400
        

        return person_presentation(person), 200


@app.get('/people', tags=[person_tag],
         responses={"200": PersonSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_people():
    with Session() as session:
       people = session.query(Person).all()

       if not people:
           return {"people": []}, 200
       else:
           return people_presentation(people), 200


@app.get('/person', tags=[person_tag],
         responses={"200": PersonSchema, "404": ErrorSchema})
def get_person(query: PersonSearchSchema):
    with Session() as session:
        person_id = query.id

        person = session.query(Person).filter(Person.id == person_id).first()

        if not person:
            error_msg = "Person not found"
            return {"message": error_msg}, 404
        else:
            return person_presentation(person), 200
      

@app.put('/person', tags=[person_tag],
         responses={"200": PersonUpdateSchema, "404": ErrorSchema})
def update_person(form: PersonUpdateSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in vars(form) if field not in optional_fields and not getattr(form, field)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        person = session.query(Person).filter(Person.id == form.id).first()

        person.name = form.name
        person.image_url = form.image_url

        try:
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to update the person"

            return {"message": error_msg}, 400

        return person_presentation(person), 200


@app.delete('/person', tags=[person_tag],
            responses={"200": PersonDeletionSchema, "404": ErrorSchema})
def delete_person(query: PersonSearchSchema):
    with Session() as session:
        person_id = query.id

        person = session.query(Person).filter(Person.id == person_id).delete()
        session.commit()

        if person:
            return {"message": "Person deleted", "id": person_id}
        else:
            error_msg = "Person not found"
            return {"message": error_msg}, 404

