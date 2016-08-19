.PHONY: help

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fixtures: fixtures/base.app.json  ## Load fixtures for base set of apps

bootstrap: ## Migrate and load fixures
	python manage.py migrate
	python manage.py createsuperuser
	$(MAKE) load_fixtures

fixtures/%.json:
	python manage.py dumpdata $(notdir $(basename $@)) | json_pp > fixtures/$(notdir $(basename $@)).json

clean_migrations: ## Remove migrations
	rm -f base/migrations/0*
	rm -f directory/migrations/0*
	rm -f lims/migrations/0*
	rm -f project/migrations/0*
	rm -f search/migrations/0*
	rm -f web/migrations/0*

load_fixtures: ## Load all fixture data
	cd fixtures && python ../manage.py loaddata *

dj_run: ## Run the server
	python manage.py migrate
	python manage.py runserver


pg_launch: ## launch postgres container
	docker run -d -p 5432:5432 -v $(shell pwd)/.pgdata:/var/lib/postgresql/data/ mdillon/postgis

pg_kill: ## kill postgres container
	docker ps | grep postgis | awk '{print $$1}' | xargs docker kill

pg_logs: ## Tail the logs from psotgres
	docker ps | grep postgis | awk '{print $$1}' | xargs docker logs

.PHONY: help fixtures bootstrap clean_migrations load_fixtures pg_launch pg_kill pg_logs
