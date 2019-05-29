from flask import Response, request, Blueprint, jsonify, send_from_directory
from flask_restful import Api
from flask_jwt_extended import get_jwt_identity, jwt_required
from uuid import uuid4
from flasgger import swag_from

from app.views import BaseResource, json_required
from app.models.post import *
from app.docs.post.post import UPLOAD_POST, POSTCONTENT

api = Api(Blueprint(__name__, __name__))


@api.resource('/<name>')
class Img(BaseResource):
    def get(self, name):
        print(name)
        return send_from_directory('/root/blog-Back-End/Server/static/img', name)


@api.resource('/post')
class Post(BaseResource):
    @swag_from(UPLOAD_POST)
    def post(self):
        '''
        게시물 작성
        '''
        content = request.json['content']
        title = request.json['title']
        category = request.json['category']
        category = CategoryModel.objects(name=category).first()
        post = PostModel(title=title, content=content, category=category.id).save()
        return jsonify({'post_id': str(post.id)})

    def get(self):
        # page = int(request.args['page'])
        category = request.args['category']
        if category == 'All':
            return jsonify([{
                'post_id': str(postContent.id),
                'creation_time': str(postContent.creation_time),
                'content': postContent.content[:50],
                'title': postContent.title,
                'category': str(postContent.category.name),
                'reaction': len(postContent.reaction),
                'commentCount': CommentModel.objects(post=postContent.id).count(),
                'image': postContent.image_name[0] if postContent.image_name else None
            } for postContent in PostModel.objects()])

        return jsonify([{
            'post_id': str(postContent.id),
            'creation_time': str(postContent.creation_time),
            'content': postContent.content[:50],
            'title': postContent.title,
            'category': str(postContent.category.name),
            'reaction': len(postContent.reaction),
            'commentCount': CommentModel.objects(post=postContent.id).count(),
            'image': postContent.image_name[0] if postContent.image_name else None
        } for postContent in PostModel.objects(category=CategoryModel.objects(name=category).first())])
        # for postContent in PostModel.objects(category=category).skip((page - 1) * 20).limit(20)])



@api.resource('/post/<post_id>')
class PostContent(BaseResource):
    @swag_from(POSTCONTENT)
    def get(self, post_id):
        """
        게시물 상세 정보
        :return:
        """
        print("asdf")
        post = PostModel.objects(id=post_id).first()
        if not post:
            return Response('', 204)

        comments = CommentModel.objects(post=post)

        return jsonify({
	  'creation_time': str(post.creation_time),
	  'title': post.title,
	  'content': post.content,
	  'category': post.category.name,
	  'reaction': len(post.reaction),
	  'images': post.image_name
	})

    @jwt_required
    def delete(self, post_id: str) -> Response:
        """
        게시물 삭제
        """
        post = PostModel.objects(id=post_id).first()
        if not post:
            return Response('', 410)

        if post.delete():
            return Response('success', 200)
        return Response('fail', 401)

    @jwt_required
    def patch(self, post_id):
        """
        게시물 수정
        """
        post = PostModel.objects(id=post_id).first()

        if not post:
            return Response('', 204)

        new_title = request.form['title']
        new_content = request.form['content']
        new_category_int = request.form['category']
        new_images = request.files.getlist("files")

        names = []

        if new_images:
            post.update(image_name=None)
            for image in new_images:
                extension = image.filename.split('.')[-1]
                image_name = '{}.{}'.format(str(uuid4()), extension)

                image.save('./static/img/{0}'.format(image_name))
                names.append(image_name)

        category = CategoryModel.objects(id=new_category_int).first()

        post.update(title=new_title, content=new_content, category=category, image_name=names)

        return Response('success', 200)
