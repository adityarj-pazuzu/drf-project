Simple Django REST Framework project for Blog application

## Getting Started

### Setting up PostgreSQL with Docker OR Install Postgres 

1. Make sure you have Docker installed on your machine.

2. Open a terminal and run the following command to start a PostgreSQL Docker container:

   ```cmd
   docker run -d --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mydb -p 5432:5432 postgres:latest

    ```

    Create database
    ```cmd
    docker exec -it postgres psql -U myuser

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