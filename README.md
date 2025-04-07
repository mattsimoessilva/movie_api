# 🗂️ Movie Application API

This is the RESTful API for **Movie Application**, developed as the MVP for the *Basic Full Stack Development* sprint of the postgraduate course in Full Stack Development at **PUC-Rio**. It allows for managing movies, people, and their roles in a movie production, using Python with Flask and SQLAlchemy.

## 🛠️ Basics
### 🌐 Base URL

All endpoints assume the server is running locally:

```
http://localhost:5000
```

### 📄 API Documentation

Swagger, Redoc, and RapiDoc interfaces are available at:

```
http://localhost:5000/
```

---

## 📚 Resources

### 📽️ Movie

#### POST `/movie`

Registers a new movie in the database. Optionally, associates people with specific roles (e.g., Director, Actor).

**📜 Important Rules for Role Association**:

- You must create the roles first using the `/role` endpoint.
- When associating people to a movie, you must provide:
  - A list of people IDs.
  - A corresponding list of roles.
- **Each role name must be written in lowercase and in the singular form (e.g., `"actor"`, not `"Actor"` or `"actors"`).**

Example request body:
```json
{
  "title": "Interstellar",
  "release_year": 2014,
  "running_time": 169,
  "budget": 165000000,
  "box_office": 677000000,
  "image_url": "https://exampleimagewebsite.com/resources/example-image.png"
  "actor": [1, 2]
}
```

#### GET `/movies`

Retrieves a list of all registered movies.

#### GET `/movie?id={id}`

Retrieves details of a specific movie by its ID.

#### PUT `/movie`

Updates a movie’s information and its list of people associated through roles. Requires all movie fields, plus any roles with person IDs (as lists) to be updated.

#### DELETE `/movie?id={id}`

Deletes a movie and its related associations.

### 👱🏻‍♂️ Person

Manage individuals who can be associated with movies (e.g., actors, directors).

#### POST `/person`

Registers a new person.

#### GET `/people`

Lists all registered people.

#### GET `/person?id={id}`

Fetches details about a specific person.

#### PUT `/person`

Updates the data of a person.

#### DELETE `/person?id={id}`

Removes a person and any associated movie roles.

### 🎭 Role

Roles define the type of contribution a person makes in a movie (such as *Actor*, *Director*, *Writer*).

#### POST `/role`

Registers a new role in the database. **Roles must be registered before associating people with movies.**

#### GET `/roles`

Retrieves all registered roles.

#### DELETE `/role?id={id}`

Deletes a role (only if not currently in use by a movie).


## 🧩 Data Models

- **Movie**
  - `title`: string
  - `image_url`: optional string
  - `running_time`: int
  - `budget`: float
  - `box_office`: float
  - `release_year`: int

- **Person**
  - `name`: string
  - `image_url` optional string

- **Role**
  - `name`: string (e.g., “Director”, “Actor”)
  - `description`: string


## ✅ Behavior Rules

- Movie and Person objects require all fields (except `image_url`) to be valid.
- You **have to create roles before adding people to them** in `/role` (POST).
- The same person can have multiple roles across different movies.

## ⚙️ Technologies

- Python
- Flask
- Flask OpenAPI 3
- SQLAlchemy
- SQLite (or another database depending on your config)
- CORS support for frontend integration


## 🧪 Testing the API

You can test the endpoints using tools like:

- [Postman](https://www.postman.com/)
- [curl](https://curl.se/)
- Built-in Swagger/Redoc interfaces at `/`

## 📝 Final Notes

This project was built as part of the educational experience of the Full Stack Development postgraduate program at **PUC-Rio**, emphasizing backend REST API design using modern Python web development practices.

