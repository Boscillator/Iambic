from flask_restful import Api

from .posts import PostsListResource

api = Api()
api.add_resource(PostsListResource, "/posts")