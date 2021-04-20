# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
COPY ./requirements.txt .

# Install native libraries, required for numpy
RUN apk --no-cache add musl-dev linux-headers g++

# Upgrade pip
RUN pip install --upgrade pip

# packages that we need
RUN pip install numpy==1.17.3
RUN pip install pandas==0.25.2
RUN pip install --user cython
RUN pip install -r requirements.txt
RUN apk update \
    && apk add --upgrade --no-cache \
        bash openssh curl ca-certificates openssl less htop \
		g++ make wget rsync \
        build-base libpng-dev freetype-dev libexecinfo-dev openblas-dev libgomp lapack-dev \
		libgcc libquadmath musl  \
		libgfortran \
		lapack-dev \
	&&  pip install --no-cache-dir --upgrade pip \
	&&  pip install scikit-learn


# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn djangoProject.wsgi:application --bind 0.0.0.0:$PORT