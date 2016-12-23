# https://github.com/TAMU-CPT/docker-recipes/blob/master/django/Dockerfile.inherit
FROM quay.io/tamu_cpt/django

# Add our project to the /app/ folder
ADD . /app/
# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
# Set current working directory to /app
WORKDIR /app/

ENV DJANGO_SETTINGS_MODULE=guanine.production \
	DJANGO_WSGI_MODULE=guanine.wsgi

# Fix permissions on folder while still root, and collect static files for use
# if need be.
RUN chown -R django /app && \
	python manage.py collectstatic --noinput

# Drop permissions
USER django
