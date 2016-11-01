# CPT LIMS

Consists of:

- directory (people, organisations)
- project (project management, access to apollo / galaxy / chado)
- LIMS (web LIMS, barcoding, etc sol'n)

## Development Setup

You will need to have GDAL stuff available. (On debian, `apt-get install gdal-bin`)

Docker is a pre-requisite for this.

```
$ pip install -r requirements.txt
$ make pg_launch
# should print some ID number, you can ignore this
$ make pg_logs
# Lots of logging output, wait until you see "CREATE_EXTENSION" ~8 times, and
# then it says "database system is shut down" and then finally says "autovacuum
# launcher started"
$ make dj_fixtures
# This will load some default data into the databases
$ make dj_run
# Actually run the server, finally
```

## Database Schema

![](./models.png)
