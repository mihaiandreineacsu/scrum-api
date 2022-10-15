# Section 1:Introduction
## Technical Requirements
1. Machine : Windows / macOS / Linux (Capable of running Docker)
2. GitHub account with the free 2000 actions minutes
3. If using Windows
    - install chocolatey package manager

## API details & Upgrades
1. Features :
    - User Authentication
    - Creating Objects
    - Filtering & Sorting Object
    - Uploading and View Images
2. Software Upgrades
    - Django 3.2 (app will need to be upgraded as newer versions are available)

# Section 2:App Design
## App Overview
1. App Design
    - Ticket API - Backend Component of a Ticket App
    - Focus is on the backend and the database of the app.
    - Features :
        - 19 API Endpoints : Managing users, tickets, tags, assignees, status, boards,
        - User Authentication
        - Browsable Admin Interface (Django Admin)
        - Browsable API (Swagger)

    - API Endpoints Overview :
        1. health-check API (Check that our API is healthy, online)
        2. ticket-assignees API (Get, a list of assignees using HTTP GET, Put, Patch, Delete a specific ingredient)
        3. ticket API (Get, a list of ticket, Post a new Ticket and specific id endpoints that allow to get a particular ticket, or update using put and patch and delete using a id)
        4. upload API (uploading images to user profile)
    - Keep different data types in different API endpoints because it is easier to use it that way in frontend.

5. tags API (Allow to create and manage tags in the system)
6. schema API (allows to get a schema document which basically defines our API and that is how swagger creates this page an automatically generated API that is added with the Django Framework)
7. users API (creates an user and an authentication token)

## Technologies
1. Python Programming Language used to build our API. Foundation of our API
2. Django Python Web Framework
- Handles :
    - URL Mappings of APIs
    - Object Relational Mapper (Create and manage objects in our database using Python and the admin site.)
    - Admin Site
3. Django REST Framework
    - Django add-on (Adds features for building rest APIs)
4. PostgreSQL
    - Database stores API Data
5. Docker
    - Containerization software. Runs services for each of different applications.
    - Run a Dockerize service of the API and of the Database.
    - Allows to create a development environment used to Build the application.
    - Allows to easily deploy our application to the server.
6. Swagger UI. Generate Automated documentation for API.
    - Use in Browser to view and test different endpoints.
7. Github Actions. Handles the automation of the application.
    - Run testings and linting every time changes are make in the code and push the code on Github.

## Django project structure
- Django Projects are split into various apps.
    1. app/ - Django project
    2. app/core/ - Code shared between multiple apps (database definition using Django models)
    3. app/user/ - User related code (user registration & authentication tokens)
    4. app/ticket/ - Recipe related code (handling, updating and managing recipes, ingredients and tags)

# Section 3:Test Driven Development
## Test Driven Development
- A development practice.
    1. Write Test
    2. Write code that passes the test code.
    3. Refactor
    4. Rerun Test.
- Unit test is code that tests code.
    - sets up conditions / inputs
    - runs a piece of code
    - check outputs using "assertions"
    - Many benefits
        - Ensures code runs as expected
        - Catches / reduces bugs
        - Improves reliability
        - Provide confidence (Good test coverage)
        - better understanding of code

# Section 4:System Setup
## What to install
- VSCode
- Docker Desktop / Docker for Linux
- Git-SCM

# Section 5:Project Setup
## New Project Overview
- Why use Docker?
    1. Consistent dev and prod environment
        - Docker Image can be use for development as for production.
        - Easier collaboration. (all dependencies are  inside Docker Image )
        - Capture all dependencies as code
            -  Python requirements
            - Operation system dependencies
        - Easier cleanup
- How to use Docker
    - Define Dockerfile (contains all the operating system level dependencies that our project needs)
    - Create Docker Compose configuration (instruct Docker how to run the images that are created from our Docker file configuration)
    - Run all commands via Docker Compose
- Docker on Github Actions
    - Docker Hub introduced rate limit:
        - 100 pulls/ 6hr for unauthenticated users
        - 200 pulls/ 6hr for authenticated users
    - Github Actions is a shared service
        - 100 pulls/ 6hr applied for all users
    - Authenticate with Docker Hub
        - Create account
        - Setup credentials
        - Login before running job
        - Get 200 pulls/ 6hr for free!

## Creating Github project
1. Create Github Account
2. Create Docker Account
3. Create Repository (public, .gitignore for Python, Readme.md)
4. Clone Repository Locally
5. Set the project up with the credentials needed to authenticate with Docker Hub
6. Docker -> Username -> Settings -> Create new Access Token -> Give a description to Token (!Do not close the Window)
7. Github -> Settings -> Secrets -> New repository secret -> Name -> DOCKERHUB_USER -> Value <dockerhub-username> -> Add Secret
8. New repository secret -> Name -> DOCKERHUB_TOKEN -> Value -> <dockerhub-access-token> (You can close the Window on point 6) -> Add Secret
- To revoke access to the project, delete Dockerhub Access Token from Docker.