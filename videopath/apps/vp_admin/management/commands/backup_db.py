import requests
from requests.auth import HTTPBasicAuth

from django.core.management.base import BaseCommand
from django.conf import settings

from videopath.apps.common.services import service_provider

# constants
DUMPFILE = "./db_dump"
#LATEST_BACKUP_URL = settings.PGBACKUPS_URL + "/latest_backup"

class Command(BaseCommand):

    def handle(self, *args, **options):

        # this is disabled for now
        # rely on heroku backups
        return None

        # test new backup strategy
        print "backup"


        token = "667ec1d6-421a-4e49-8c8d-107fa8db51f8"
        headers = {
            'Accept': 'application/vnd.heroku+json; version=3',
            #'Authorization': 'Bearer ' + token,
            'x_heroku_gem_version': '3.36.5'
        }

        # test regular access
        r = requests.get("https://api.heroku.com/apps", headers=headers)
        print r.text
        print "==="

        #
        r = requests.get("https://postgres-api.heroku.com/client/v11/databases/advising-softly-7947/metrics", auth=HTTPBasicAuth('dscharf@gmx.net', 'b4FGz1wjvUk6'))
        #r = requests.get("https://postgres.heroku.com/api/dbs.json", headers=headers)

        print r
        print r.json()



        # get latest backup info
        r = requests.get(LATEST_BACKUP_URL)
        dump_url = r.json()["public_url"]
        dump_timestamp = r.json()["finished_at"].replace("/", "-")
        dump_name = "videopath-api/" + dump_timestamp

        # write dump to file
        r = requests.get(dump_url, stream=True)
        if r.status_code == 200:
            with open(DUMPFILE, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

        # upload to s3
        s3_service = service_provider.get_service("s3")
        s3_service.upload(DUMPFILE, settings.AWS_DB_DUMPS_BUCKET, dump_name)
