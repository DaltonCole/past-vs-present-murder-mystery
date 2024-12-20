#! /bin/bash

python3 manage.py migrate --noinput
python3 manage.py loaddata fixtures/*.json
python3 manage.py createcachetable

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python3 manage.py collectstatic --noinput

exec "$@"
