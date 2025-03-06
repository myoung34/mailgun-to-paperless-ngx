setup:
	poetry install

gen_requirements:
	poetry export --without-hashes -f requirements.txt >requirements.txt

gen_requirements_dev:
	poetry export --without-hashes --with dev -f requirements.txt >requirements-dev.txt

test:
	poetry run tox

run:
	docker build -t mailgun_to_paperless_ngx .
	docker run -e "BIND_PORT=3000" -p 3000:3000 mailgun_to_paperless_ngx
