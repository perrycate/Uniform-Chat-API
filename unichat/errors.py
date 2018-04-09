import falcon

def set_mappings(app):
    """
    Configure error handlers for exceptions that might be raised. Unhandled
    errors trigger an HTTP 500.
    """
    app.add_error_handler(NotImplementedError, _not_implemented)


def _not_implemented(exception, request, response, params):
    response.status = falcon.HTTP_501
