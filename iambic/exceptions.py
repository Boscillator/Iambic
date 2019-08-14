import werkzeug.exceptions
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


class InvalidPoemError(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Your poem does not contain iambic pentameter'


def register_handlers(app):
    def handle_error(e):
        logger.exception(e)
        code = 500
        description = "Something went wrong!"
        if isinstance(e, werkzeug.exceptions.HTTPException):
            code = e.code
            description = e.description

        return jsonify({
            'code': code,
            'description': description,
            'error': str(e)
        }), code
