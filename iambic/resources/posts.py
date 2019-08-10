from flask_restful import Resource, reqparse, marshal_with, fields
from ..models import db, Post

import logging

logger = logging.getLogger(__name__)

post_parser = reqparse.RequestParser()
post_parser.add_argument('body')

post_marshal = {
    'body': fields.String,
}


class PostsListResource(Resource):

    @marshal_with(post_marshal)
    def get(self):
        logger.info("Fetching list of posts.")
        return Post.query.all(), 200

    @marshal_with(post_marshal)
    def post(self):
        args = post_parser.parse_args()
        p = Post(body=args['body'])
        db.session.add(p)
        db.session.commit()

        logger.info(f"Created post with id {p.id}")
        return p, 201
