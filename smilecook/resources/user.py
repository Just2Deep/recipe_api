from flask import request, url_for, render_template
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from webargs import fields
from webargs.flaskparser import use_kwargs

from marshmallow import ValidationError
from utils import verify_token, generate_token
from models.user import User
from models.recipe import Recipe

from schemas.user import UserSchema
from schemas.recipe import RecipeSchema

from mailgun import MailgunApi
from config import Config

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=("email",))

recipe_list_schema = RecipeSchema(many=True)

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
        {"visibility": fields.Str(missing="public", required=False)}, location="query"
    )
    def get(self, username, visibility):
        if user := User.get_by_username(username=username):
            current_user = get_jwt_identity()
            if current_user != user.id or visibility not in ["all", "private"]:
                visibility = "public"

            recipes = Recipe.get_all_by_user(user_id=user.id, visibility=visibility)

            return recipe_list_schema.dump(recipes), HTTPStatus.OK

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
