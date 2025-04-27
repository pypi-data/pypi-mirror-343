
class JJSystemException(Exception):

    status = 500
    message = ''

    def __init__(self, message=None):
        if message is not None:
            self.message = message


class NotFound(JJSystemException):

    status = 404
    message = 'Entity not found'


class DuplicatedEntity(JJSystemException):

    status = 404
    message = 'Entity already exists'


class BadRequest(JJSystemException):

    status = 400
    message = 'Provided body does not represent a valid entity'


class OperationBadRequest(JJSystemException):

    status = 400
    message = 'Provided body does not provide ' + \
        'valid info for performing operation'


class BadRequestContentType(BadRequest):

    message = 'Content-Type header must be application/json'


class PreconditionFailed(BadRequest):

    message = 'One or more preconditions failed'


class FatalError(JJSystemException):

    message = 'FATAL ERROR'
