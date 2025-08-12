extract:
	pybabel extract --input-dirs=. -o locales/messages.pot

init:
	pybabel init -i locales/messages.pot -d locales -D messages -l en
	pybabel init -i locales/messages.pot -d locales -D messages -l uz
	pybabel init -i locales/messages.pot -d locales -D messages -l ru

compile:
	pybabel compile -d locales -D messages\

update:
	pybabel update -d locales -D messages -i locales/messages.pot

alembic_init:
	alembic init migrations

migration:
	alembic revision --autogenerate -m "Create a baseline migrations"

head:
	alembic upgrade head

manual_migration:
	alembic revision -m "Create trigger on students table"

webadmin:
	uvicorn web.app:app --reload