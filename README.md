# scrum-api

## Django project structure
- Django Projects are split into various apps.
    1. app/ - Django project
    2. app/core/ - Code shared between multiple apps (database definition using Django models)
    3. app/user/ - User related code (user registration & authentication tokens)
    4. app/task/ - Task related coe (handling, updating and managing tasks, contacts)

## Creating Github project
1. Create Github Account
2. Create Docker Account
3. Create Repository (public, .gitignore for Python, Readme.md)
4. Clone Repository Locally
5. Set the project up with the credentials needed to authenticate with Docker Hub:
   1. Docker -> Username -> Settings -> Create new Access Token -> Give a description to Token (!Do not close the Window)
   2. Github -> Settings -> Secrets -> New repository secret -> Name -> DOCKERHUB_USER -> Value <dockerhub-username> -> Add Secret
   3. New repository secret -> Name -> DOCKERHUB_TOKEN -> Value -> <dockerhub-access-token> (You can close the Window on point 6) -> Add Secret
- To revoke access to the project, delete Dockerhub Access Token from Docker.

---

## Get Started

---

Build Docker image

- With Docker
```cmd
docker build .
```
- With docker-compose
```cmd
docker-compose build
```
---

## Linting and Testing

1. Linting
- Run it through Docker Compose
- Fix linting errors from the bottom-up
    ```cmd
    docker-compose run --rm app sh -c "flake8"
    ```
- Temporarily Suppress Linting for unused imports
    - add after unused import ```## noqa``` (tells flake8 to ignore line error)
2. Testing
- Run test through Docker Compose
  ```cmd
  docker-compose run --rm app sh -c "python manage.py test"
  ```
- Where do you put test?
    - Placeholder tests.py added to each app
    - Or, create tests/ subdirectory to split tests up
    - Keep in mind:
        - Only use ```tests.py``` or ```tests/``` directory (not both)
        - Test modules must start with ```test_```
        - Test directories must contain ```__init__.py```
-  Test classes
    - ```SimpleTestCase```
        - No database integration
        - Useful if no database is required for your test
        - Save time executing tests
    - ```TestCase```
        - Database integration
        - Useful for testing code that uses the database

---

## Create Django Project

Create a django project named app in the current directory
```cmd
docker-compose run --rm app sh -c "django-admin startproject app ."
```
Because Django is install in Docker Image, run the CLI command just as were on our local machine.
- Sync was made by the volumes we defined in Docker compose.
- Because of that, everything that we create in our local machine, gets mapped to Docker image and vice versa.

---

## Run project with Docker Compose
- Command to start docker services
    ```cmd
    docker-compose up
    ```
- Open browser at : [127.0.0.1:8000](127.0.0.1:8000)
- Stop the development server with ctrl + c

---

## Create Django app

Create a django app named app
```cmd
docker-compose run --rm app sh -c "python manage.py startapp core"
```

---

## Database migrations

- Creating migrations
    - Ensure app is enabled in settings.py
    - Use Django CLI command:
    ```cmd
    python manage.py makemigrations
    ```
- Applying migrations
    - Use Django CLI command:
    ```cmd
    python manage.py migration
    ```
- Run it after waiting for database and after any new Model (best practice)


- Common issues
  - ```jango.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency core.0001_initial on database 'default'.```
    - clear the volume (refreshes our database, clear all data in our development database)
      - List all Volumes: ```docker volume ls```
      - Remove volume: ```docker volume rm <volume-name>```
  - ```Error response from daemon: remove recipe-app-api_dev-db-data: volume is in use - [volume-hash]```
    - Clear any containers using the volume: ```docker-compose down```
    - Remove Volume again: ```docker volume rm <volume-name>```

---

## Create Superuser
- Create ```superuser``` credentials using CLI
```cmd
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

---

## Swager UI
 - Start server : ```docker-compose up```
 - Navigate to [127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

---