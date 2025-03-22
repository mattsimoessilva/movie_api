from flask_openapi3 import OpenAPI, Tag, Info
import json
from flask import Flask, jsonify, redirect
from flask_cors import CORS

info = Info(title="Movie API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc or RapiDoc")

@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')


@app.post('/movie', tags=[movie_tag],
          responses={"200": MovieViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_movie(form: MovieSchema):

    movie = Movie(
        name = form.name,
        
    )