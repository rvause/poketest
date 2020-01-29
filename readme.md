Run database

```
docker run --rm -l poke-postgres -e POSTGRES_USER=poketest -e POSTGRES_DB=poketest -p 5432:5432 postgres:12.1-alpine
```

Make virtualenv and install requirements

```
$ venv poketest
$ pip install -r requirements
```

Run migrations

```
./manage.py migrate
```

Run Server

```
./manage.py runserver
```

Run Tests

```
pytest
```
