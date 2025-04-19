Simple Django REST Framework project for Blog application
It covers CRUD operations, ORM, ViewSets, Router, Models, Migrations, SQL database, JWT authentication, unittests. There's also a script provided to test endpoints using Python requests module. There's no front end, it's pure REST API. The database used is Postgres, and credentials are hardcoded in code. Code has been developed and tested on Windows, the database has been tested as standalone application as well as a docker container.

Database model: title, content, created_at, modified_at, author

API can do the following things:
 - Get a list of all blogs
 - Get blog by id,
 - Create, update, and delete blog
 - Get the blog by date, created_before date, created_after date, by author, within the date range

This project serves the purpose of learning basic DRF principles and implementation

## Getting Started

### Setting up PostgreSQL with Docker OR Install Postgres

1. Make sure you have Docker installed on your machine.

2. Open a terminal and run the following command to start a PostgreSQL Docker container:

   ```cmd
   docker run -d --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mydb -p 5432:5432 postgres:latest
   ```

    Create database
    ```cmd
    docker exec -it postgres psql -U postgres

    CREATE DATABASE mydb;

    \q
    ```

3. Clone the repo
    ```cmd
    git clone https://github.com/adityarj-pazuzu/drf-project.git
    ```

4. Create a virtual environment:
    ```cmd
    python -m venv venv
    ```

5. Activate the virtual environment:
    ```cmd
    .\venv\Scripts\activate

    ```

6. Install dependencies:
    ```cmd
    pip install -r requirements.txt
    ```

7. Apply migrations:
    ```cmd
    python manage.py migrate
    ```

8. Create a superuser:
    ```cmd
    python manage.py createsuperuser
    ```

9. Run the development server:
    ```cmd
    python manage.py runserver
    ```

10. Run tests
    ```cmd
    python manage.py test myapp.tests
    ```

11. Test APIs using requests
    ```cmd
    python api-requests-script.py
    ```


## Blog Endpoints

### Authentication

The API uses JSON Web Tokens (JWT) for authentication. Include the JWT token in the Authorization header of your requests.

- **Endpoint:** `/token/`
- **Method:** `POST`
- **Description:** Obtain an access token by providing valid credentials.
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://localhost:8000/token/
    ```

### Get a List of Blogs

- **Endpoint:** `/api/blogs/`
- **Method:** `GET`
- **Description:** Retrieve a list of all blogs.
    ```cmd
    curl -X GET -H "Authorization: Bearer <your_jwt_token_here>" http://localhost:8000/api/blogs/
    ```

### Get a Single Blog

- **Endpoint:** `/api/blogs/{blog_id}/`
- **Method:** `GET`
- **Description:** Retrieve details of a specific blog.
    ```bash
    curl -X GET -H "Authorization: Bearer <your_jwt_token_here>" http://localhost:8000/api/blogs/{blog_id}/
    ```

### Create a Blog

- **Endpoint:** `/api/blogs/`
- **Method:** `POST`
- **Description:** Create a new blog. Requires authentication.

   ```bash
   curl -X POST -H "Authorization: Bearer <your_jwt_token_here>" -H "Content-Type: application/json" -d '{"title": "Blog Title" "content": "Blog Content"}' http://localhost:8000/api/blogs/
   ```

### Update a Blog

- **Endpoint:** `/api/blogs/{blog_id}/`
- **Method:** `PUT`
- **Description:** Update an existing blog. Requires authentication and ownership of the blog.

   ```bash
   curl -X PUT -H "Authorization: Bearer <your_jwt_token_here>" -H "Content-Type: application/json" -d '{"title": "Updated Blog Title" "content": "Updated Blog Content"}' http://localhost:8000/api/blogs/{blog_id}/
   ```

### Delete a Blog

- **Endpoint:** `/api/blogs/{blog_id}/`
- **Method:** `DELETE`
- **Description:** Delete an existing blog. Requires authentication and ownership of the blog.

   ```bash
   curl -X DELETE -H "Authorization: Bearer <your_jwt_token_here>" http://localhost:8000/api/blogs/{blog_id}/
   ```
### Get blogs by Author
```bash
curl -X GET -H "Authorization: Bearer your_jwt_token_here" http://localhost:8000/api/blogs/?author={author_id}
```

### Get Blogs by date
```bash
curl -X GET -H "Authorization: Bearer your_jwt_token_here" http://localhost:8000/api/blogs/by_date/?date={yyyy-mm-dd}
```

### Get Blogs within Date Range
```bash
curl -X GET -H "Authorization: Bearer your_jwt_token_here" \
http://localhost:8000/api/blogs/by_date_range/?start_date={yyyy-mm-dd}&end_date={yyyy-mm-dd}
```

### Get Blogs Created After a Date
```bash
curl -X GET -H "Authorization: Bearer your_jwt_token_here" http://localhost:8000/api/blogs/created_after_date/?date={yyyy-mm-dd}
```

### Get Blogs Created Before a Date
```bash
curl -X GET -H "Authorization: Bearer <your_jwt_token_here>" http://localhost:8000/api/blogs/created_before_date/?date={yyyy-mm-dd}
```
