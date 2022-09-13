FROM python:3.9-alpine3.13
# What is defined in the Dockerfile ?
# Operation system level dependencies.
# The Dockerfile is used to build our image,
# which contains a mini Linux Operating System with all the dependencies needed to run our project.
LABEL maintainer="mihai@developerakademie.com"
# Unbuffer Python (does not buffer the output, the output from python will be printed directly to the console)
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt
COPY ./app /app
# this is the default directory commands are going to be run from when running commands on Docker Image
WORKDIR /app
# exposing Port from our container to our machine on container run,
# allowing to access that port on the container that's running from Docker image.
EXPOSE 8000
# Configure dockerfile if dev build to install Dev Requirements
ARG DEV=false
# for each RUN in Dockerfile a image layer is created,
#  avoid this to keep images lightweight as possible by breaking the commands in multiple line
#  by using "&& \" syntax
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements-dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
# ENV updates the environment variable inside the image
ENV PATH="/py/bin:$PATH"
# USER line should be last line of DOckerfile, specifies the user to switch to.
# Before this line everything is done as ROOT user, after this line everything is done as what the USER was set to.
USER django-user