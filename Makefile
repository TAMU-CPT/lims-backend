.PHONY: help

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

bootstrap: ## Migrate and load fixures
	python manage.py migrate
	$(MAKE) dj_load_fixtures

dj_fixtures:  ## Load fixtures for base set of apps
	python manage.py loaddata 00_auth.json
	python manage.py loaddata 00_directory.json
	python manage.py shell < fixtures/drop.py
	python manage.py loaddata 01_account.json

dj_clean_migrations: ## Remove migrations
	rm -f \
		account/migrations/0*py* \
		bioproject/migrations/0*py* \
		directory/migrations/0*py* \
		lims/migrations/0*py*

dj_sync: ## Make migrations
	python manage.py makemigrations
	python manage.py migrate

dj_run: ## Run the server
	python manage.py migrate
	python manage.py runserver

pg_launch: ## launch postgres container
	@docker run -d -p 5432:5432 -v $(shell pwd)/.pgdata:/var/lib/postgresql/data/ mdillon/postgis

pg_kill: ## kill postgres container
	@docker ps | grep postgis | awk '{print $$1}' | xargs docker kill

pg_logs: ## Tail the logs from postgres
	@docker ps | grep postgis | awk '{print $$1}' | xargs docker logs -f

pg_rm: ## Wipe out postgres database
	sudo rm -rf .pgdata

restart:
	$(MAKE) pg_kill
	$(MAKE) pg_rm
	$(MAKE) pg_launch
	sleep 5
	$(MAKE) dj_sync

.PHONY: help fixtures bootstrap clean_migrations pg_launch pg_kill pg_logs
