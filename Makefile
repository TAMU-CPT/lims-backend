


fixtures: fixtures/base.app.json

fixtures/%.json:
	python manage.py dumpdata $(notdir $(basename $@)) | json_pp > fixtures/$(notdir $(basename $@)).json

.PHONY: fixtures
