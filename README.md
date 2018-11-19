## How to run?

### Pre-requisites

* `docker 18.06.1-ce`.
* `docker-compose 1.23.1`.

### Setup

We use docker to build and run our application.
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
DJANGO_SETTINGS_MODULE=tivix_test.settings.dev
DJANGO_SECRET_KEY=<your-secret-key>
```
*NOTE: docker will automatically create PostgreSQL user and DB according to the values set in your environment variables.*

### Run our docker services

Get the database up and running first.
```

docker-compose up --build tivix_db
```

Now build and start our Django website. Open a new tab in terminal.
```
docker-compose up --build tivix_web
```

Now you should be able to access the website at http://localhost:8000.

### Running tests

Once we have the docker services up and running we can use the same docker containers to execute our tests.

#### Code cleanup check
```
docker-compose exec tivix_web flake8 .
```

#### Unittests
```
docker-compose exec tivix_web python manage.py test -k
```
