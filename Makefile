

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
	cd fixtures && python ../manage.py loaddata *

download_borders: world/data/TM_WORLD_BORDERS-0.3.shp

world/data/:
	mkdir -p world/data/

world/data/TM_WORLD_BORDERS-0.3.zip: world/data/
	wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip

world/data/TM_WORLD_BORDERS-0.3.shp:
	cd world/data && unzip -f TM_WORLD_BORDERS-0.3.zip

.PHONY: fixtures
