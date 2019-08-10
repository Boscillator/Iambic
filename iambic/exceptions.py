import werkzeug.exceptions
from flask import jsonify


class InvalidPoemError(werkzeug.exceptions.HTTPException):
    code = 400
    description = 'Your poem does not contain iambic pentameter'


def register_handlers(app):
    @app.errorhandler(Exception)
    def handle_error(e):
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
