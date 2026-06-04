# MakeOfficeHours API

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

A Flask API server that handles enqueuing and dequeuing students from the office hours queue.

# Project Structure

### [/auth](./auth):

Routes and functions related to authentication. Authentication is independent of the roster; a user can be in the roster
but not have a sign-in. This just handles authenticating with Autolab, or password authentication in testing.

### [/config](./config):

Configuration for the Flask server.

### [/database](./database):

Home of the database interface and implementation. [`db.py`](./database/db.py) selects the implementation based on the
`DB` environment variable. This should probably always be set to "relational", as this is the only complete
implementation. If completed "mock" and "testing" may be useful for testing without a database, but the application is
fleshed out enough where this may not be necessary.

Anything outside this folder should import `db` from `db.py` and use the interface to interact with the database. If the
current functionality is not sufficient, it should be added to the database interface.

### [/queue](./queue):

Routes and functions related to the queue. This includes all endpoints relevant to enqueuing/dequeuing students as well
as in-progress visits.

Visits are created whenever a student is dequeued. Until one of the endpoints are hit that end a visit, TAs are
prevented from dequeuing and students are prevented from enqueuing.

Endpoints related to visits that are not in-progress can be found in [/roster](./roster), mainly to be retrieved for
review.

### [/roster](./roster):

Routes and functions related to course management, mainly enrollments and visit records.

Visit records are sensitive information and should not be freely accessible to TAs. However, TAs can currently see
visits that they were
personally involved with for their own review.

TAs can manage the roster but to ensure sensitive information is kept secret, they can only add students who only have
access to the queue endpoints. This is to ensure course instructors don't need to be concerned with the day-to-day
operations of the site (e.g. a student adds the course and comes to TA office hours but can't use the site, the TA
can just add them without having to go through the professor.)

The [controller](./roster/controller.py) defines two decorators that are used pretty extensively through the project
for permission checking: `@exact_level` and `@min_level`. It is **very** important that these decorators are below 
`@blueprint.route`, as they are otherwise ignored.

### [/student_data_lookups](./student_data_lookups):

Currently, nothing. As this app grows to interact with other services, these interactions should live here.

### [/utils](./utils)

Mainly debug utilities. The `@debug_access_only` decorator is defined here. As with the roster decorators, these **must**
go below `@blueprint.route`. If used properly, it effectively disables this route in production. This is used for the
password authentication routes to ensure that in production only Autolab can be used to verify UBITs.


# Development

If you want to run the project locally, make sure you install the dependencies.

```bash
pip install -r requirements.txt
```

For this project please use python 3.14.

To run the API server locally, run 
```bash
python -m api.run_local
```
from the **root directory** of the project. This will start the server in debug mode on port 5050.

# Utilities

You can install these utilities locally with:

```bash
pip install -r utils.txt
```

## Pylint

Project uses pylint to keep the code style organized.

You can run the Pylint on the api folder by doing the following

```bash
pylint $(git ls-files '*.py')
```

This hasn't been adhered to for most of development, but it's best
that you ensure your code is neat and organized.

## Formatter

Using the Black formatter https://github.com/psf/black

```bash
black $(git ls-files '*.py') 
```

# Resources

Good resources to look at:

- https://flask.palletsprojects.com/en/stable/blueprints/
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
