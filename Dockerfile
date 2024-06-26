FROM python:3.9-slim
# FROM python:3.9-alpine3.13
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
# Update and install dependencies using apt-get for Debian/Ubuntu
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y postgresql-client libjpeg-dev && \
    apt-get install -y --no-install-recommends build-essential libpq-dev zlib1g-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements-dev.txt ; \
    fi && \
    apt-get remove -y build-essential libpq-dev zlib1g-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* && \
    useradd -m scrum-api && \
    if [ "$DEV" = "true" ]; then \
        mkdir -p /home/scrum-api && \
        chown scrum-api:scrum-api /home/scrum-api; \
    fi && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R scrum-api:scrum-api /vol && \
    chmod -R 755 /vol
# ENV updates the environment variable inside the image
ENV PATH="/py/bin:$PATH"
# USER line should be last line of Dockerfile, specifies the user to switch to.
# Before this line everything is done as ROOT user, after this line everything is done as what the USER was set to.
USER scrum-api