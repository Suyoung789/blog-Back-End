from flask_restful import Api
from flask import Blueprint, Response, request, jsonify

from app.views import BaseResource
from app.models.post import CategoryModel

api = Api(Blueprint(__name__, __name__))


@api.resource('/category')
class Category(BaseResource):
    def get(self):
        return jsonify([{'category_name': Category.name}
                        for Category in CategoryModel.objects()])
    def post(self):
        '''
        카테고리 추가
        '''

        category_name = request.json['category_name']

        CategoryModel(name=category_name).save()
        return Response('', 201)

@api.resource('/category/<category_name>')
class CategoryContent(BaseResource):
    def delete(self, category_name):
        print("asdf")

        category = CategoryModel.objects(name=category_name).first()
        print("asdf")

        category.delete()
        return Response('', 200)

@api.resource('/option')
class Option(BaseResource):
    def get(self):
        name = []
        category = CategoryModel.objects().all()
        for i in range(len(category)):
            name.append(category[i]['name'])
        return name
