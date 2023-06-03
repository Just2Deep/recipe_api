import os
from flask import request, url_for, render_template
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from webargs import fields
from webargs.flaskparser import use_kwargs

from marshmallow import ValidationError
from utils import verify_token, generate_token, save_image
from models.user import User
from models.recipe import Recipe

from schemas.user import UserSchema
from schemas.recipe import RecipeSchema, RecipePaginationSchema

from mailgun import MailgunApi
from config import Config

from extensions import image_set

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=("email",))
user_avatar_schema = UserSchema(only=("avatar_url",))

recipe_list_schema = RecipeSchema(many=True)
recipe_pagination_schema = RecipePaginationSchema()

mailgun = MailgunApi(
    domain=Config.MAILGUN_DOMAIN,
    api_key=Config.MAILGUN_API_KEY,
)


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data=json_data)
        except ValidationError as errors:
            return {
                "message": "Validation errors",
                "errors": errors.messages,
            }, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get("username")):
            return {"message": "username already used"}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get("email")):
            return {"message": "email already used"}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        token = generate_token(user.email, salt="activate")
        subject = "Please Confirm Your Registration."

        link = url_for("useractivateresource", token=token, _external=True)
        text = f"Hi, Thanks for using SmileCook! Please confirm your registration by clicking on the link: {link}"

        mailgun.send_email(
            to=user.email,
            subject=subject,
            text=text,
            html=render_template("email.html", token_url=link),
        )

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        if user := User.get_by_username(username=username):
            current_user = get_jwt_identity()

            if current_user == user.id:
                data = user_schema.dump(user)
            else:
                data = user_public_schema.dump(user)

            return data, HTTPStatus.OK

        return {"message": "user not found"}, HTTPStatus.NOT_FOUND


class MeResource(Resource):
    @jwt_required(optional=False)
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        data = user_schema.dump(user)

        return data, HTTPStatus.OK


class UserRecipeListResource(Resource):
    @jwt_required(optional=True)
    @use_kwargs(
        {
            "visibility": fields.Str(missing="public", required=False),
            "page": fields.Int(missing=1),
            "per_page": fields.Int(missing=10),
        },
        location="query",
    )
    def get(self, username, visibility, page, per_page):
        if user := User.get_by_username(username=username):
            current_user = get_jwt_identity()
            if current_user != user.id or visibility not in ["all", "private"]:
                visibility = "public"

            recipes = Recipe.get_all_by_user(
                user_id=user.id,
                page=page,
                per_page=per_page,
                visibility=visibility,
            )

            return recipe_pagination_schema.dump(recipes), HTTPStatus.OK

        return {"message": "User Not Found"}, HTTPStatus.NOT_FOUND


class UserActivateResource(Resource):
    def get(self, token):
        email = verify_token(token=token, salt="activate")

        if email is False:
            return {"message": "Invalid token or token expired"}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)

        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if user.is_active == True:
            return {"message": "user already activated"}, HTTPStatus.BAD_REQUEST

        user.is_active = True
        user.save()

        return {}, HTTPStatus.NO_CONTENT


class UserAvatarUploadResource(Resource):
    @jwt_required()
    def put(self):
        file = request.files.get("avatar")

        if not file:
            return {"message": "Not a valid image"}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {"message": "File type not allowed"}, HTTPStatus.BAD_REQUEST

        user = User.get_by_id(id=get_jwt_identity())

        if user.avatar_image:
            avatar_path = image_set.path(folder="avatars", filename=user.avatar_image)

            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file, folder="avatars")
        user.avatar_image = filename
        user.save()

        return user_avatar_schema.dump(user), HTTPStatus.OK
