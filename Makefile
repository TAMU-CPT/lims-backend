.PHONY: help

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

fixtures: fixtures/base.app.json  ## Load fixtures for base set of apps

bootstrap: ## Migrate and load fixures
	python manage.py migrate
	python manage.py createsuperuser
	$(MAKE) load_fixtures

launch_pg: ## launch postgres container
	docker run -d -p 5432:5432 -v $(shell pwd)/.pgdata:/var/lib/postgresql/9.4/ mdillon/postgis

kill_pg: ## kill postgres container
	docker ps | grep postgis | awk '{print $$1}' | xargs docker kill

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

.PHONY: fixtures
