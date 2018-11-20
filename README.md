## How to run?

### Pre-requisites

* `docker`. Tested in version `18.06.1-ce`.
* `docker-compose`. Tested in version `1.23.1`.

### Setup

We use docker to build and run our application. As a first step, clone the repo.
```
git clone git@github.com:jayakrishnandingit/tivix_test.git
cd tivix_test
```

Create a docker-compose.yml file by copying the sample file given.

*NOTE: docker-compose.yml file is never committed to repo since it has sensitive contents.*
```
cp docker-compose.yml.sample docker-compose.yml
```

Now edit the environment variables provided in the `docker-compose.yml` file you just created.
```
vim docker-compose.yml

# FYI, environment variables to edit are,
POSTGRES_USER=<your-user>
POSTGRES_PASSWORD=<your-password>
POSTGRES_DB=<your-db-name>
DJANGO_SECRET_KEY=<your-secret-key>
```
*NOTE: docker will automatically create PostgreSQL user and DB according to the values set in your environment variables.*

I have defined `django settings` under `settings/` directory with 3 files `base.py`, `dev.py`, and `production.py`. This helps us in separating concerns while running in different environments. While running the application we can specify which settings file to use by providing appropriate value for `DJANGO_SETTINGS_MODULE` environment variable in `docker-compose.yml` file. By default, it points to `dev.py`.

#### Build our docker services

Get the database up and running first.
```
docker-compose up --build tivix_db
```

Now build the django web service. Open a new tab in terminal.
```
docker-compose build tivix_web
```

Once it is built, we need to run, migrations to create required tables in the database.
```
docker-compose run --rm tivix_web python manage.py migrate
```

*NOTE: Since this is a development setup, we are not running `collectstatic`.*

#### Running tests

Once we have the docker services setup we can execute our tests.

1. Code cleanup check
```
docker-compose run --rm tivix_web flake8 .
```

2. Unittests
```
docker-compose run --rm tivix_web python manage.py test -k
```

### Run application

Now we can start the django dev server.
```
docker-compose up tivix_web
```

Now you should be able to access the website at http://localhost:8000.
