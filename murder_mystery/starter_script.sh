python3 manage.py makemigrations
python3 manage.py migrate --noinput
python3 manage.py createcachetable

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

python3 manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000
