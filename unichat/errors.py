import falcon
import json
import logging
import sys
import traceback


def set_mappings(app):
    """
    Configure error handlers for exceptions that might be raised. Unhandled
    errors trigger an HTTP 500.
    """

    # Most generic handler must come first
    app.add_error_handler(Exception, _unknown_error)
    app.add_error_handler(NotImplementedError, _not_implemented)
    app.add_error_handler(ServiceError, _service_error)
    app.add_error_handler(AuthenticationError, _auth_error)
    app.add_error_handler(UnauthorizedError, _forbidden_error)

    logging.info('Set error maps.')


#
# Error Handling Methods
#

def _not_implemented(exception, request, response, params):
    logging.error(exception)
    response.status = falcon.HTTP_501 # HTTP Not Implemented

def _unknown_error(exception, request, response, params):
    logging.error(traceback.format_exc())
    response.status = falcon.HTTP_500 # HTTP Server Error

def _service_error(exception, request, response, params):
    logging.error(traceback.format_exc())
    response.body = json.dumps({'error': str(exception)})
    response.status = falcon.HTTP_502 # HTTP Bad Gateway

def _auth_error(exception, request, response, params):
    logging.info(
            'Unauthorized {} request for {} from {} with token \'{}\''.format(
                request.method,
                request.path,
                request.remote_addr,
                request.params.get('token', '')))
    response.status = falcon.HTTP_401 # HTTP Unauthorized

def _forbidden_error(exception, request, response, params):
    logging.info( '{} request for {} from {} with token \'{}\' failed due to'
            'insufficient permissions.'.format(
                request.method,
                request.path,
                request.remote_addr,
                request.params.get('token', '')))
    response.status = falcon.HTTP_403 # HTTP Forbidden


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

class UnauthorizedError(ServiceError):
    """
    Raised when the client is authenticated correctly, but does not have
    sufficient permissions to perform the operation.
    """
    pass


