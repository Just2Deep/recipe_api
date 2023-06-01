from flask import request
from flask_restful import Resource
from http import HTTPStatus

from marshmallow import ValidationError
from models.recipe import Recipe
from models.user import User
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.recipe import RecipeSchema

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)


class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()

        return recipe_list_schema.dump(recipes), HTTPStatus.OK

    @jwt_required()
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()

        try:
            data = recipe_schema.load(data=json_data)
        except ValidationError as errors:
            return {
                "message": "Validation Errors",
                "errors": errors.messages,
            }, HTTPStatus.BAD_REQUEST

        recipe = Recipe(**data, user_id=current_user)
        recipe.save()

        return recipe_schema.dump(recipe), HTTPStatus.CREATED


class RecipeResource(Resource):
    @jwt_required(optional=True)
    def get(self, recipe_id):
        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            current_user = get_jwt_identity()
            if recipe.is_publish == False and recipe.user_id != current_user:
                return {"message": "Access not allowed"}, HTTPStatus.FORBIDDEN
            return recipe_schema.dump(recipe), HTTPStatus.OK

        return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND

    @jwt_required()
    def put(self, recipe_id):
        if not (recipe := Recipe.get_by_id(recipe_id=recipe_id)):
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        json_data = request.get_json()
        current_user = get_jwt_identity()

        try:
            data = recipe_schema.load(data=json_data)
        except ValidationError as errors:
            return {
                "message": "Validation Errors",
                "errors": errors.messages,
            }, HTTPStatus.BAD_REQUEST

        if current_user != recipe.user_id:
            return {"message": "Access not allowed"}, HTTPStatus.FORBIDDEN

        recipe.name = data["name"]
        recipe.description = data["description"]
        recipe.num_of_servings = data["num_of_servings"]
        recipe.cook_time = data["cook_time"]
        recipe.directions = data["directions"]

        recipe.save()
        return recipe_schema.dump(recipe), HTTPStatus.OK

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

    @jwt_required()
    def patch(self, recipe_id):
        json_data = request.get_json()

        try:
            data = recipe_schema.load(data=json_data, partial=("name",))
        except ValidationError as error:
            return {
                "message": "Validation Errors",
                "errors": error.messages,
            }, HTTPStatus.BAD_REQUEST

        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            current_user = get_jwt_identity()
            if current_user != recipe.user_id:
                return {"message": "Access is not allowed"}, HTTPStatus.FORBIDDEN

            recipe.name = data.get("name") or recipe.name
            recipe.description = data.get("description") or recipe.description
            recipe.num_of_servings = (
                data.get("num_of_servings") or recipe.num_of_servings
            )
            recipe.cook_time = data.get("cook_time") or recipe.cook_time
            recipe.directions = data.get("directions") or recipe.directions

            recipe.save()

            return recipe_schema.dump(recipe), HTTPStatus.OK

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