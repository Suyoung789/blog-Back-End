from flask_restful import Api
from flask import Blueprint, Response, request

from app.views import BaseResource
from app.models.post import CategoryModel

api = Api(Blueprint(__name__, __name__))


@api.resource('/category')
class Category(BaseResource):
    def post(self):
        '''
        카테고리 추가
        '''

        category_name = request.json['category_name']

        CategoryModel(name=category_name).save()
        return Response('', 201)

    def delete(self):

        category_name = request.json['category_name']

        category = CategoryModel.objects(name=category_name).first()

        category.delete()
        return Response('', 200)
