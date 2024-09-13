python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
# python manage.py crontab remove
# python manage.py crontab add
# python manage.py crontab show
gunicorn eCommerce_Django_Project.wsgi:application --bind 0.0.0.0:5000
# python manage.py runserver 0.0.0.0:5000