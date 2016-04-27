fixtures: fixtures/base.app.json


bootstrap:
	#$(MAKE) launch_pg
	$(MAKE) migrate
	$(MAKE) load_fixtures


migrate:
	python manage.py migrate
	python manage.py createsuperuser

launch_pg:
	docker run -d -p 5432:5432 mdillon/postgis

kill_pg:
	docker ps | grep postgis | awk '{print $1}' | xargs docker kill

fixtures/%.json:
	python manage.py dumpdata $(notdir $(basename $@)) | json_pp > fixtures/$(notdir $(basename $@)).json

clean_migrations:
	rm -f base/migrations/0*
	rm -f directory/migrations/0*
	rm -f lims/migrations/0*
	rm -f project/migrations/0*
	rm -f search/migrations/0*
	rm -f web/migrations/0*

load_fixtures:
	cd fixtures && python ../manage.py loaddata *

.PHONY: fixtures
