run-bot:
	python -m src

shell:
	ipython

test:
	pytest tests -v

up:
	docker compose up -d

stop:
	docker compose stop
