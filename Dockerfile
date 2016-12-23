# https://github.com/TAMU-CPT/docker-recipes/blob/master/django/Dockerfile.inherit
FROM quay.io/tamu_cpt/django

# Add our project to the /app/ folder
ADD . /app/
# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
# Set current working directory to /app
WORKDIR /app/

# GeoDjango
RUN apt-get install binutils libproj-dev gdal-bin python-gdal
# Fix permissions on folder while still root, and collect static files for use
# if need be.
RUN chown -R django /app && \
	python manage.py collectstatic --noinput

# Drop permissions
USER django
