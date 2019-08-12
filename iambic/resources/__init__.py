from flask_restful import Api

from .posts import PostsListResource
from .validate import ValidationResource

api = Api()
api.add_resource(PostsListResource, "/posts")
api.add_resource(ValidationResource, "/validate")
