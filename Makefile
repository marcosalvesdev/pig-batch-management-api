run:
	python manage.py runserver 0.0.0.0:8000

up:
	docker compose up

up-d:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build

logs:
	docker compose logs

persistlogs:
	docker compose logs -f

migrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

fmigrate: migrations migrate

superuser:
	docker compose exec web python manage.py createsuperuser --username admin --email=admin@example.com

shell:
	docker compose exec web python manage.py shell

testkf:
	docker compose exec web python manage.py test --keepdb --failfast

rediscli:
	docker compose exec redis redis-cli

redisclear:
	docker compose exec redis redis-cli flushall

test:
	docker compose exec web python manage.py test --keepdb --failfast

web-bash:
	docker compose exec web bash