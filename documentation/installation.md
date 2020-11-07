# VideoPath API Installation
===



[ ![Codeship Status for videopath/api](https://codeship.io/projects/8ca66760-1ccf-0132-376b-6e4899336ea0/status)](https://codeship.io/projects/35297)

## Installation

#### Prerequisites
You will need these things to start

	python 2.7.+
	pip
	virtualenv
	git
	heroku (only for running on heroku)
	libmemcached (brew install libmemcached)
	postgres (brew install postgresql)

### Recommended 

	Use pyflakes for linting your python code

See the internet on how to install these for your OS.

You then need to create a virtualenv to run in. See internet also.
Start it with ``source dir-to-your-venv/bin/activate``.

#### Installation

	git clone https://github.com/huesforalice/vp-api
	cd vp-api
	pip install -r requirements.txt

	# Create the core database tables
	python manage.py syncdb --noinput

	# Run the database migrations
	python manage.py migrate

	# Create your first superuser
	python manage.py createsuperuser

	# Fix permissions for the newly created user (because we backdoored the user creation)
	# You will need to run this everytime you do a south migration or create a user in the admin
	python manage.py check_permissions

	# create environment variables or create a local settings file
	# this file will allow you to change
	vi videopath/settings/env_local.py
	cp videopath/settings/env_local_sample.py videopath/settings/env_local.py

	# create a "static" folder
	mkdir videopath/static

	# Run the development server / make sure the python instance of the venv is used
	python manage.py runserver

	# or use the heroku dev server
	foreman start

#### Pip Help
Install cryptography on mac:
run this before installing with pip
	brew install openssl
	env ARCHFLAGS="-arch x86_64" LDFLAGS="-L/usr/local/opt/openssl/lib" CFLAGS="-I/usr/local/opt/openssl/include"

#### Heroku

	# Create app
	heroku create
	git push heroku master

	# Do this for all the commands above
	heroku run <commands>

	# Set the environment variables
	# See videopath/settings_local_sample.py for variables needed
	heroku config:set

	# If you want to enable debugging temporarily use
	heroku config:set DJANGO_DEBUG=TRUE

	# To reset the database for testing
	heroku pg:reset DATABASE_URL

	# To view the logs
	heroku logs

## Authorization

### Get the auth token
	curl -X POST http://127.0.0.1:8000/videopath/api/auth-token/ -H "Content-Type: application/json" -d '{"username":"","password":""}'

### Use the auth token
	curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token <token>'


## Database migration

### add new migration
	python manage.py schemamigration (appname) --auto

### run migrations of all apps
	python manage.py migrate

## Site Name

Django uses a site row in the database to identify the install to the world in things such as emails. Change this to the domain you installed in on.

	Go to http://127.0.0.1:8000/admin/
	Use the superuser password you created
	Go to "Sites"
	Change the "Domain name" and "Display name"

## Amazon

To use S3 and Elastic Transcoder

TODO


## Tests

	# Run all tests for the api app
	python manage.py test api

	# Run tests for a specific class in the api app
	python manage.py test api.AuthTest

	# Run a single test in the api app AuthTest class
	python manage.py test api.AuthTest.test_user_creation


