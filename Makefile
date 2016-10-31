.PHONY: help

help:
	@egrep '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dj_fixtures:  ## Load fixtures for base set of apps
	python manage.py migrate
	python manage.py loaddata fixtures/00_auth.json
	python manage.py loaddata fixtures/00_directory.json
	python manage.py shell < fixtures/drop.py
	python manage.py loaddata fixtures/01_account.json

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

models.png: account/models.py bioproject/models.py directory/models.py lims/models.py ## Build PNG file of database models
	python manage.py graph_models -a -o models.png

restart:
	$(MAKE) pg_kill
	$(MAKE) pg_rm
	$(MAKE) pg_launch
	sleep 5
	$(MAKE) dj_sync

.PHONY: help fixtures bootstrap clean_migrations pg_launch pg_kill pg_logs
