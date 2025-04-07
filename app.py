from flask_openapi3 import OpenAPI, Tag, Info
import json
from flask import Flask, jsonify, redirect, request
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
def add_movie(body: MovieSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in MovieSchema.__annotations__ if field not in optional_fields and not getattr(body, field, None)]

    if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
    with Session() as session:
        movie = Movie(
            title=body.title,
            image_url=body.image_url or "",
            running_time=body.running_time,
            budget=body.budget,
            box_office=body.box_office,
            release_year=body.release_year
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
        
        movie_person_role_list = []

        role_fields_exist = any(isinstance(person_list, list) and person_list for person_list in body.dict().values())

        if role_fields_exist:
            for role_name, person_list in body.dict().items():  
                if isinstance(person_list, list) and person_list:  
                    role = session.query(Role).filter(Role.name.ilike(role_name)).first()

                    if role:
                        for person_id in person_list:
                            movie_person_role = MoviePersonRole(
                                movie_id=movie.id,  
                                person_id=person_id,
                                role_id=role.id
                            )
                            movie_person_role_list.append(movie_person_role)


        try:
            if movie_person_role_list:
                session.bulk_save_objects(movie_person_role_list)
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
def update_movie(body: MovieUpdateSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in MovieSchema.__annotations__ if field not in optional_fields and not getattr(body, field, None)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        movie = session.query(Movie).filter(Movie.id == body.id).first()

        movie.title = body.title
        movie.image_url = body.image_url
        movie.running_time = body.running_time
        movie.budget = body.budget
        movie.box_office = body.box_office
        movie.release_year = body.release_year

        try:
            session.commit()
        
        except Exception as e:
            error_msg = "It wasn't possible to update the movie"

            return {"message": error_msg}, 400
        
        existing_roles_on_movie = {
            (mpr.movie_id, mpr.person_id, mpr.role_id)
            for mpr in session.query(MoviePersonRole).filter(MoviePersonRole.movie_id == movie.id).all()
        }

        new_roles_on_movie = set()

        movie_person_role_list = []

        role_fields_exist = any(isinstance(person_list, list) and person_list for person_list in body.dict().values())

        if role_fields_exist:
            for role_name, person_list in body.dict().items():
                if isinstance(person_list, list) and person_list:
                    role = session.query(Role).filter(Role.name.ilike(role_name)).first()

                    if role:
                        for person_id in person_list:
                            role_entry = (movie.id, person_id, role.id)
                            new_roles_on_movie.add(role_entry)
                            
                            movie_person_role_list.append(MoviePersonRole(
                                movie_id=movie.id, person_id=person_id, role_id=role.id
                            ))

            to_add = new_roles_on_movie - existing_roles_on_movie
            to_remove = existing_roles_on_movie - new_roles_on_movie

        try:
            if movie_person_role_list:
                if to_remove:
                    session.query(MoviePersonRole).filter(
                        MoviePersonRole.movie_id.in_([m_id for m_id, _, _ in to_remove]),
                        MoviePersonRole.person_id.in_([p_id for _, p_id, _ in to_remove]),
                        MoviePersonRole.role_id.in_([r_id for _, _, r_id in to_remove])
                    ).delete(synchronize_session=False)

                if to_add:
                    session.bulk_save_objects([MoviePersonRole(movie_id=m_id, person_id=p_id, role_id=r_id) for m_id, p_id, r_id in to_add])

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

        movie = session.query(Movie).filter(Movie.id == movie_id).first()
        session.delete(movie)
        session.commit()

        if movie:
            return {"message": "Movie deleted", "id": movie_id}
        else:
            error_msg = "Movie not found"
            return {"message": error_msg}, 404

# ROLE

@app.post('/role', tags=[role_tag],
          responses={"200": RoleSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_role(body: RoleSchema):
    optional_fields = {}
    missing_fields = [field for field in RoleSchema.__annotations__ if field not in optional_fields and not getattr(body, field, None)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        role = Role(
            name = body.name,
            description = body.description,
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
def update_role(body: RoleUpdateSchema):
    optional_fields = {}
    missing_fields = [field for field in RoleSchema.__annotations__ if field not in optional_fields and not getattr(body, field, None)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        role = session.query(Role).filter(Role.id == body.id).first()

        role.name = body.name
        role.description = body.description

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

        role = session.query(Role).filter(Role.id == role_id).first()
        session.delete(role)
        session.commit()

        if role:
            return {"message": "Role deleted", "id": role_id}
        else:
            error_msg = "Role not found"
            return {"message": error_msg}, 404

# PERSON
            
@app.post('/person', tags=[person_tag],
          responses={"200": PersonSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_person(body: PersonSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in PersonSchema.__annotations__ if field not in optional_fields and not getattr(body, field, None)]

    if missing_fields:
        error_msg = f"Missing required fields [{', '.join(missing_fields)}]";
        return jsonify({"message": error_msg}), 400
    
    with Session() as session:
        person = Person(
            name = body.name,
            image_url = body.image_url,
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
def update_person(body: PersonUpdateSchema):
    optional_fields = {"image_url"}
    missing_fields = [field for field in Person.__annotations__ if field not in optional_fields and not getattr(body, field, None)]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    with Session() as session:
        person = session.query(Person).filter(Person.id == body.id).first()

        person.name = body.name
        person.image_url = body.image_url

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

        person = session.query(Person).filter(Person.id == person_id).first()
        
        session.delete(person)
        session.commit()

        if person:
            return {"message": "Person deleted", "id": person_id}
        else:
            error_msg = "Person not found"
            return {"message": error_msg}, 404

