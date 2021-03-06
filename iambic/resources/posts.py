from flask_restful import Resource, reqparse, marshal_with, fields
from ..models import db, Post
from ..logic import validator
from ..exceptions import InvalidPoemError

import logging

logger = logging.getLogger(__name__)

post_parser = reqparse.RequestParser()
post_parser.add_argument('body')

post_marshal = {
    'body': fields.String,
    'created_at': fields.DateTime
}


class PostsListResource(Resource):

    @marshal_with(post_marshal)
    def get(self):
        logger.info("Fetching list of posts.")
        return Post.query.order_by(Post.created_at.desc()).all(), 200

    @marshal_with(post_marshal)
    def post(self):
        args = post_parser.parse_args()

        if not validator.is_stanza_iambic(args['body']):
            raise InvalidPoemError()

        p = Post(body=args['body'])
        db.session.add(p)
        db.session.commit()

        logger.info(f"Created post with id {p.id}")
        return p, 201
