.PHONY: up migrate test seed

up:
	docker compose up -d

migrate:
	docker compose exec web python manage.py migrate

test:
	docker compose exec web python manage.py test

seed:
	docker compose exec web python manage.py seed_data
