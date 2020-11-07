#!/bin/bash
if [ "$1" == "setup" ]; then
	# setup basic thigs
	python manage.py syncdb --noinput
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py check_permissions
elif [ "$1" == "run" ]; then
    echo "Starting app"
    # gunicorn -b 127.0.0.1:5000  --access-logfile - --certfile certs/server.crt --keyfile certs/server.key --do-handshake-on-connect videopath.wsgi 
    python manage.py runserver 5000
elif [ "$1" == "run_worker" ]; then
    # start redis server in background
	redis-server & 
	python worker.py
elif [ "$1" == "test" ]; then
	python manage.py test videopath/apps/**/tests/**/*.py --with-id
elif [ "$1" == "test_failed" ]; then
	python manage.py test videopath/apps/**/tests/**/*.py --failed
elif [ "$1" == "deploy" ]; then
	#capture db state
	heroku pg:backups capture --app videopath-api
	# deploy
	git push heroku master
	# run migrations
	heroku run python manage.py migrate --app videopath-api
elif [ "$1" == "import_heroku_db" ]; then
	# capture remote db and import to local postgres instance
	heroku pg:backups capture --app videopath-api
	backup_url=$(heroku pg:backups public-url --app videopath-api)
	curl -o latest.dump $backup_url
	psql -h 127.0.0.1 -p 5432 -c "drop database videopath_import"
	psql -h 127.0.0.1 -p 5432 -c "create database videopath_import"
	pg_restore --verbose --clean --no-acl --no-owner -h localhost -U david -d videopath_import latest.dump
	rm latest.dump
elif [ "$1" == "heroku_login" ]; then
	#capture db state
	spawn heroku login 
	expect "*?mail:*"
	send -- "dscharf@gmx.net\r"
	expect "*?assword:*"
	send -- "password"
elif [ "$1" == "reset_local_db" ]; then
    rm test.db
	python manage.py syncdb --noinput
	python manage.py migrate
	python manage.py createsuperuser
	python manage.py check_permissions
elif [ "$1" == "clear_cache" ]; then
    find . -name \*.pyc -delete
else 
	echo "Command not found"
fi
