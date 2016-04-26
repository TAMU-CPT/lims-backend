

fixtures: fixtures/base.app.json

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
	cd fixtures && python ../migrate.py loaddata *

.PHONY: fixtures
