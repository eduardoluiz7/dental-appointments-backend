.PHONY: run makemigrations makemigrations-all migrate shell superuser clean help

help:
	@echo "Available commands:"
	@echo "  make run              - Run Django development server"
	@echo "  make makemigrations   - Create database migrations"
	@echo "  make migrate          - Apply database migrations"
	@echo "  make shell            - Open Django shell"
	@echo "  make superuser        - Create a superuser"
	@echo "  make clean            - Remove Python file artifacts"

run:
	python manage.py runserver

makemigrations:
	python manage.py makemigrations

makemigrations-all: makemigrations


migrate:
	python manage.py migrate

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +