# Movie-Rate
This an API that allows users to list movies, view listed movies, rate them, and add comments. This API Uses FastAPI framework, JWT (JSON Web Tokens) for authentication and authorization and postgres QL for database. 

## Table of Contents

1. [Installation](#installation)
2. [API Endpoints](#api-endpoints)
3. [Configuration](#configuration)

## Installation

### Prerequisites

- Docker
- Docker Compose
- Python 3.10

### Steps

1. **Clone the repository:**

    ```terminal
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build and run the Docker container:**

    ```terminal
    docker-compose up --build
    ```

3. **The application will be available at:**

    ```
    http://localhost:8000 
    ```
4. **The swagger documentation will be available at:**

    ```
    http://localhost:8000/docs
    ```

## API Endpoints

### Database Setup
The database is configured using SQLAlchemy with support for PostgreSQL, MySQL, or SQLite. The environment variables for the database URL are loaded from a .env file.

- Base: Declarative base for SQLAlchemy models.
- SessionLocal: Database session generator.
- get_db: Dependency that provides a database session to request handlers.


### Authentication
Authentication is handled using JWT tokens. The authentication process involves verifying user credentials, generating a JWT token for the authenticated user, and using that token to authorize subsequent requests.

- verify_password: Verifies the plain password against the hashed password stored in the database.
- authenticate_user: Authenticates a user by username and password.
- create_access_token: Creates a JWT token for a user.
- get_current_user: Retrieves the currently authenticated user from the JWT token

### CRUD Operations
CRUD operations are implemented to handle database interactions for users, movies, ratings, and comments.

- get_user_by_username: Retrieves a user by their username.
- create_user: Creates a new user in the database.
- get_movie_by_id: Retrieves a movie by its ID.
- create_movie: Creates a new movie in the database.
- update_movie: Updates an existing movie.
- delete_movie: Deletes a movie.
- create_rating: Creates a new rating for a movie.
- create_comment: Creates a new comment on a movie.
- create_nested_comment: Creates a nested comment.

### Routers
The routers define the API endpoints and link them to the corresponding CRUD operations.

#### auth_router.py
Handles user authentication endpoints:

- POST /auth/login: Authenticates a user and returns a JWT token.
- GET /auth/me: Retrieves the current authenticated user's details.

#### movie_router.py
Handles movie-related endpoints:

- GET /movies/{movie_id}: Retrieves details of a specific movie.
- POST /movies: Creates a new movie.
- PUT /movies/{movie_id}: Updates an existing movie.
- DELETE /movies/{movie_id}: Deletes a movie.

#### rating_router.py
Handles rating-related endpoints:

- POST /ratings: Creates a new rating for a movie.
- GET /movies/{movie_id}/ratings: Retrieves all ratings for a specific movie.

##### comment_router.py
Handles comment-related endpoints:

- POST /comments: Creates a new comment on a movie.
- POST /comments/{parent_id}: Creates a nested comment under a specific parent comment.
- GET /movies/{movie_id}/comments: Retrieves all comments for a specific movie.

## Configuration

Create a `.env` file in the root directory and add your environment variables:

```env
SECRET_KEY=your_secret_key
HASHING_ALGORITHM=your_hashing_algorithm
```