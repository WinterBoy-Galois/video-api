from django.core.management.base import BaseCommand


from videopath.apps.common.services.cloudfront_custom.CloudFrontConnection import CloudFrontConnection

class Command(BaseCommand):

    def handle(self, *args, **options):
    	connection = CloudFrontConnection()
        connection.create_invalidation_request("EWJTLXRZSWYB1", ["/test/*"])
