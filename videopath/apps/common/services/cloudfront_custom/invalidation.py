from boto.cloudfront.invalidation import InvalidationBatch as _InvalidationBatch
from boto.compat import urllib

class InvalidationBatch(_InvalidationBatch):
    """A simple invalidation request.
        :see: http://docs.amazonwebservices.com/AmazonCloudFront/2010-08-01/APIReference/index.html?InvalidationBatchDatatype.html
    """
    # fix this
    def escape(self, p):
        """Escape a path, make sure it begins with a slash and contains no invalid characters"""
        if not p[0] == "/":
            p = "/%s" % p
        if p[-1] == "*":
            return "%s*" % urllib.parse.quote(p[:-1])
        else:
            return urllib.parse.quote(p)
