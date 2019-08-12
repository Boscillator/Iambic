from flask_restful import Resource, reqparse, marshal_with, fields
from ..logic import validator, ValidationResult

import logging

logger = logging.getLogger(__name__)


class EnumField(fields.Raw):
    def format(self, value):
        return value.value


validation_parser = reqparse.RequestParser()
validation_parser.add_argument('body')

result_marshal = {
    'ok': fields.Boolean,
    'at': fields.Integer,
    'reason': EnumField()
}


class ValidationResource(Resource):

    @marshal_with(result_marshal)
    def post(self):
        args = validation_parser.parse_args()

        results = []
        for line in args['body'].strip().splitlines():
            results.append(validator.is_iambic(line))
        return results
