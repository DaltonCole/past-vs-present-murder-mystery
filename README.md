# past-vs-present-murder-mystery

## Run

`docker-compose up --build`

## Django

* To make a new app: `python manage.py startapp <app>`
    * Note: App name should be plural while table names are singular

* When the schema for the database changes the following commands must be ran:
    1) To create the code to perform the migration: `python manage.py makemigrations`
    2) To actually update the database: `python manage.py migrate`

## Docker

* Restart a single container (ex backend): `docker-compose restart backend`

### Trouble-shooting

* If you run into a "Error response from daemon: network * not found" error try: `docker-compose up --force-recreate`
