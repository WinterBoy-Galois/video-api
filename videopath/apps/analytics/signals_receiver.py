from django.dispatch import receiver
from django.core.management import call_command

from videopath.apps.vp_admin.signals import daily_jobs

@receiver(daily_jobs)
def run_import_analytics(sender, **kwargs):
    call_command("import_analytics")
