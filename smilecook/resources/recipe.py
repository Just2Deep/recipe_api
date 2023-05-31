from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required


class RecipeListResource(Resource):
    def get(self):
        if recipes := Recipe.get_all_published():
            data = [recipe.data() for recipe in recipes]
            return {"data": data}, HTTPStatus.OK

        return {"data": []}, HTTPStatus.OK

    @jwt_required(optional=False)
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()

        recipe = Recipe(
            name=data["name"],
            description=data["description"],
            num_of_servings=data["num_of_servings"],
            cook_time=data["cook_time"],
            directions=data["directions"],
            user_id=current_user,
        )
        recipe.save()

        return recipe.data(), HTTPStatus.CREATED


class RecipeResource(Resource):
    @jwt_required(optional=True)
    def get(self, recipe_id):
        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            current_user = get_jwt_identity()
            if recipe.is_publish == False and recipe.user_id != current_user:
                return {"message": "Access not allowed"}, HTTPStatus.FORBIDDEN
            return recipe.data(), HTTPStatus.OK

        return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

    @jwt_required()
    def put(self, recipe_id):
        print("recipe_id", recipe_id)
        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            data = request.get_json()
            current_user = get_jwt_identity()

            if current_user != recipe.user_id:
                return {"message": "Access not allowed"}, HTTPStatus.FORBIDDEN

            recipe.name = data["name"]
            recipe.description = data["description"]
            recipe.num_of_servings = data["num_of_servings"]
            recipe.cook_time = data["cook_time"]
            recipe.directions = data["directions"]

            recipe.save()
            return recipe.data(), HTTPStatus.OK

        return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

    @jwt_required()
    def delete(self, recipe_id):
        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            data = request.get_json()
            current_user = get_jwt_identity()

            if current_user != recipe.user_id:
                return {{"message": "Access not allowed"}}, HTTPStatus.FORBIDDEN

            recipe.delete()
            return {}, HTTPStatus.NO_CONTENT

        return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND


class RecipePublishResource(Resource):
    @jwt_required()
    def put(self, recipe_id):
        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            current_user = get_jwt_identity()
            if current_user != recipe.user_id:
                return {{"message": "Access not allowed"}}, HTTPStatus.FORBIDDEN

            recipe.is_publish = True
            recipe.save()

            return {}, HTTPStatus.NO_CONTENT

        return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

    @jwt_required()
    def delete(self, recipe_id):
        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            current_user = get_jwt_identity()
            if current_user != recipe.user_id:
                return {{"message": "Access not allowed"}}, HTTPStatus.FORBIDDEN

            recipe.is_publish = False
            return {}, HTTPStatus.NO_CONTENT

        return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
