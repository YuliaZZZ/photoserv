start:
	python3 manage.py runserver

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

install:
	pip3 install -r requirements.txt

test:
	python3 manage.py test

test1:
	pytest serv/tests/ --disable-warnings

shell:
	python3 manage.py shell

user:
	python3 manage.py createsuperuser

static:
	python3 manage.py collectstatic

celery-start:
	celery -A app worker -l info -Q app_queue --autoscale 4,2

celery-beat:
	celery -A app beat -l info -S django

test2:
	coverage run --source='.' --omit=*/migrations/* manage.py test serv






.PHONY : start migrate install celery-start test shell static celery-beat