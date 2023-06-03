import os
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs

from marshmallow import ValidationError
from models.recipe import Recipe
from models.user import User
from utils import save_image
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemas.recipe import RecipeSchema, RecipePaginationSchema

from extensions import image_set

recipe_schema = RecipeSchema()
recipe_list_schema = RecipeSchema(many=True)
recipe_cover_schema = RecipeSchema(only=("cover_image_url",))
recipe_pagination_schema = RecipePaginationSchema()


class RecipeListResource(Resource):
    @use_kwargs(
        {"page": fields.Integer(missing=1), "per_page": fields.Integer(missing=20)},
        location="query",
    )
    def get(self, page, per_page):
        paginated_recipes = Recipe.get_all_published(page=page, per_page=per_page)

        return recipe_pagination_schema.dump(paginated_recipes), HTTPStatus.OK

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


class RecipeCoverUploadResource(Resource):
    @jwt_required()
    def put(self, recipe_id):
        file = request.files.get("cover_image")

        if not file:
            return {"message": "Not a valid image"}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {"message": "file type not allowed"}, HTTPStatus.BAD_REQUEST

        if recipe := Recipe.get_by_id(recipe_id=recipe_id):
            if recipe.cover_image:
                cover_image_path = image_set.path(
                    filename=recipe.cover_image, folder="recipes"
                )
                if os.path.exists(cover_image_path):
                    os.remove(cover_image_path)

            file_path = save_image(image=file, folder="recipes")
            recipe.cover_image = file_path
            recipe.save()

            return recipe_cover_schema.dump(recipe), HTTPStatus.OK

        return {"message": "recipe does not exist"}, HTTPStatus.NOT_FOUND
