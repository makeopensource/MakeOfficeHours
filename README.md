# MakeOfficeHours

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

# api

A Flask API server that handles enqueuing and dequeuing students from the office hours queue.

### How to run

#### Debug
```bash
flask --app api run --debug
```

### Pylint

Project uses pylint to keep the code style concurrent
<!-- TODO: ask if we should use google's pylint setting -->

You can run the Pylint on the api folder by doing the following

```bash
pylint api/
```

#### Formatter
Using the Black formatter https://github.com/psf/black

### Project structure




### Resource
Good resources to look at:
- https://flask.palletsprojects.com/en/stable/blueprints/
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure