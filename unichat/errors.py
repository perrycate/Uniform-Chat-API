import falcon


def set_mappings(app):
    """
    Configure error handlers for exceptions that might be raised. Unhandled
    errors trigger an HTTP 500.
    """
    app.add_error_handler(NotImplementedError, _not_implemented)
    # Most generic handler must come first
    #app.add_error_handler(ServiceError, _service_error)
    #app.add_error_handler(AuthenticationError, _auth_error)


#
# Error Definitions
#

class ServiceError(Exception):
    """
    Generic error raised for any error returned from an external service.
    """
    pass

class AuthenticationError(ServiceError):
    """
    Raised when a translator cannot authenticate with its service with the
    given auth token.
    """
    pass

#
# Error Handling Methods
#

def _not_implemented(exception, request, response, params):
    response.status = falcon.HTTP_501 # HTTP Not Implemented


def _service_error(exception, request, response, params):
    response.status = falcon.HTTP_502 # HTTP Bad Gateway

def _auth_error(exception, request, response, params):
    response.status = falcon.HTTP_401
