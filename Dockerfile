# Dockerfile
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        musl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#install pipenv
RUN pip install pipenv  
RUN pip install django  
    
# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python dependencies
COPY Pipfile Pipfile.lock /usr/src/app/
RUN pipenv install --deploy --system

# Install django-storages
RUN pip install google-cloud-storage

# Copy the JSON key file into the container
COPY key.json /usr/src/app/key.json

# Set Google Cloud credentials environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/key.json"

# Copy the Django project code into the container
COPY . /usr/src/app/

#collect static files
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8080

# Run Gunicorn with appropriate settings
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "server.wsgi:application"]
