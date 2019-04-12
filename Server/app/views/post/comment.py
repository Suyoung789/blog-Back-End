from flask import Response, request, Blueprint, jsonify
from flask_restful import Api
from flask_jwt_extended import get_jwt_identity, jwt_required
from uuid import uuid4
from app import BaseResource, json_required

from app.models.post import *

api = Api(Blueprint(__name__, __name__))


@api.resource('/post/<post_id>/comment')
class Comment(BaseResource):
    @jwt_required
    @json_required({'content': str})
    def post(self,  post_id):

        post = PostModel.objects(id=post_id).first()

        if not post:
            return Response('post not exist', 204)

        content = request.json['content']

        comment = CommentModel(content=content, post=post).save()

        return jsonify({'comment_id': str(comment.id)})


@api.resource(('/post/<post_id>/comment/<comment_id>'))
class CommentDetail(BaseResource):
    def delete(self, post_id, comment_id):
        """
        댓글 삭제
        """
        comment = CommentModel.objects(id=comment_id).first()

        if not comment:
            return Response('', 204)



        comment.delete()

        return Response('', 200)

    def patch(self, post_id, comment_id):

        comment = CommentModel.objects(id=comment_id).first()


        if not comment:
            return Response('', 204)


        content = request.json['content']

        comment.update(content=content)

        return Response('', 200)
