install:
	@poetry install

run:
	@poetry run uvicorn app.main:app --reload

lint:
	@poetry run flake8 --config flake8.cfg

test:
	@poetry run pytest #-s -vv

migrations:
ifdef m
	@poetry run alembic revision -m "$(m)"
else
	@echo "add m='message'"
endif

migrate:
	@poetry run alembic upgrade head
