from django.core.management.base import BaseCommand

from videopath.apps.vp_admin.signals import daily_jobs, JOB_PRIORITY_DEFAULT

class Command(BaseCommand):

    def handle(self, *args, **options):
        daily_jobs.send_robust(JOB_PRIORITY_DEFAULT)
