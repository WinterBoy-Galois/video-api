from django.core.management.base import BaseCommand

from videopath.apps.vp_admin.signals import hourly_jobs, JOB_PRIORITY_DEFAULT

class Command(BaseCommand):

    def handle(self, *args, **options):
        hourly_jobs.send_robust(JOB_PRIORITY_DEFAULT)
