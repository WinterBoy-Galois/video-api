from django import http

#
# Make sure cross origin requests are accepted by the app
#
class CorsHeaderMiddleware(object):

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE"
        response[
            'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRFToken"
        return response

    def process_request(self, request):
        if (request.method == 'OPTIONS' and 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META):
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = "*"
            response['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE"
            response[
                'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Authorization, X-CSRFToken"
            return response
        return None
