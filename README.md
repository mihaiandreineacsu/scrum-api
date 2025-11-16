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
- Test classes
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
  - ```Error response from daemon: remove task-app-api_dev-db-data: volume is in use - [volume-hash]```
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

## Debugging a Containerized Django App in VS Code

### Create a VS Code run configuration to attach to a Docker container

- Create a Run Configuration
If you haven't already set up a [run configuration](https://code.visualstudio.com/docs/python/debugging) for your project add a <i>.vscode/launch.json</i> file:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Django",
      "type": "python",
      "request": "attach",
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/app",
          "remoteRoot": "/usr/src/app"
        }
      ],
      "port": 3000,
      "host": "127.0.0.1",
    }
  ]
}
```

Make sure to update the ```localRoot``` and ```remoteRoot``` values, which VS Code uses to map the source files between your [workspace](https://stackoverflow.com/questions/44629890/what-is-a-workspace-in-visual-studio-code/57134632#57134632) and the filesystem of the remote host. Although these values will differ based on how your project is set up, you can generally get this information from your Docker volume config.

For example, say you have the following config in your Docker Compose file:

```yml
volumes:
  - ./app/:/usr/src/app/
```

The local folder path, ```./app/```, is what ```localRoot``` should be set to (e.g., ```"${workspaceFolder}/app"```) while ```remoteRoot``` should be set to the folder inside the container (e.g., ```"/usr/src/app"```). It's worth noting that this folder inside the container is likely to be your working directory as well:

```Dockerfile
WORKDIR /usr/src/app
```

```"request": "attach"``` indicates that we want to connect VS Code's debugger to a process that's already running. In the above config, we tell it to attach to port 3000 on 127.0.0.1. We'll configure debugpy to run on ```127.0.0.1:3000``` shortly.

When done, click the "Run" icon in the activity bar on the far left. You should now see the ```Run Django``` configuration besides the play button in the side bar:

- Modify manage.py to start a [debugpy](https://github.com/microsoft/debugpy/) (Python Tools for Visual Studio Debug Server) debug server

To begin with, add the debugpy package to your requirements file:

```txt
debugpy==1.5.1
```

Since debugpy runs alongside the Django app, we'll need to configure it to run inside our <i>manage.py</i> file:

```py
from django.conf import settings

if settings.DEBUG:
    if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
        import debugpy
        debugpy.listen(("0.0.0.0", 3000))
        print('Attached!')
```

Your file will look something similar to:

```py
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    # start new section
    from django.conf import settings

    if settings.DEBUG:
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            import debugpy
            debugpy.listen(("0.0.0.0", 3000))
            print('Attached!')
    # end new section

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

Here, we first determine if the project is running in ```DEBUG``` mode. If so, we then make sure that the debugger is not attached if it's a reload of Django (if you change some code while the server is running).

The ```debugpy.listen()``` method starts the debug server. You can also block execution until the debugger is attached with ```wait_for_client()```:

```py
from django.conf import settings

if settings.DEBUG:
    if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
        import debugpy
        debugpy.listen(("0.0.0.0", 3000))
        debugpy.wait_for_client()
        print('Attached!')
```

Since debugpy will run on port 3000, you need to expose that port to the host. If you're using Docker Compose, you can expose the port like so:

```yml
version: '3.8'

services:
  web:
    build: ./app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./app/:/usr/src/app/
    ports:
      - 8000:8000
      - 3000:3000
```

If you're not using Compose, make sure to expose the ports when you run the container:

```cmd
docker run -d -p 8000:8000 -p 3000:3000 web
```

- Debug a containerized Django Project in VS Code

After you build the new image to install debugpy, spin up the new container.

Set a breakpoint somewhere in your code. Then in VS Code open the "Run" view again and make sure the ```Run Django``` configuration that we previously created is selected. Click the play button to start the debugging session.

You should now be able to get to the breakpoint and start debugging the Django app running inside the Docker container.

---

TIP: If you're using Python 3.7 or later, debugpy also supports Python's ```breakpoint()``` function.

## Testing

- To run tests inside the container, use the following command:

```cmd
docker exec -it <container_name> pytest
```

Replace `<container_name>` with the name or ID of your running Django container. This command will execute `pytest` within the specified container, allowing you to run your test suite in the same environment as your application.

Make sure that `pytest` is installed in your Docker image. You can add it to your `requirements.txt` or install it manually inside the container if needed.

- To run coverage report inside the container, use the following command:

```cmd
docker exec -it <container_name> coverage run -m pytest
docker exec -it <container_name> coverage report
docker exec -it <container_name> coverage html
```
