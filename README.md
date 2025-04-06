# MakeOfficeHours

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

# api
A Flask API server that handles enqueuing and dequeuing students from the office hours queue.

# Quick Started
1. You will first need to install all the development packages mainly use for 


##### Development
```bash
docker compose up api-development--build
```


### Pylint
Project uses pylint to keep the code style concurrent

[//]: # (TODO: ask if we should use google's pylint setting)

You can run the Pylint on the api folder by doing the following

```bash
pylint api/
```

#### Formatter
Using the Black formatter https://github.com/psf/black

### Project structure
[//]: # (TODO: Going to do a markdown of a file structure here so that you can see the project structure)


### Resource
Good resources to look at:
- https://flask.palletsprojects.com/en/stable/blueprints/
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure