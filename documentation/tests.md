# VideoPath API Tests

## Running all tests
	python manage.py test

## Running individual tests
	python manage.py test videopath.apps.videos.tests.api

## Running all tests within a folder
	#run all model tests in video app
	python manage.py test videopath/apps/videos/tests/models/*.py
	# run all tests in video app
	python manage.py test videopath/apps/videos/tests/**/*.py