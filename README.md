# MakeOfficeHours

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

# api

A simple flask api server that handels students enqueue and dequeue

### how to run

#### Debug
```bash
flask --app api run --debug
```

### pylint

Project uses pylint to keep the code style concurrent
<!-- TODO: ask if we should use google's pylint setting -->

You can run the pylint on the api folder by doing the following
```bash
pylint api/
```

#### Formatter
Currently using the black formatter https://github.com/psf/black