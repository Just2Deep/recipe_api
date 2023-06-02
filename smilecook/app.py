from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db, jwt, image_set
from flask_uploads import configure_uploads  # patch_request_class

from resources.recipe import RecipeResource, RecipeListResource, RecipePublishResource
from resources.user import (
    UserListResource,
    UserResource,
    MeResource,
    UserRecipeListResource,
    UserActivateResource,
    UserAvatarUploadResource,
)
from resources.token import TokenResource, RefreshResource, RevokeResource, blacklist


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    configure_uploads(app, image_set)
    # patch_request_class(app, 5 * 1024 * 1024)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]

        return jti in blacklist


def register_resources(app):
    api = Api(app)

    api.add_resource(RecipeListResource, "/recipes")
    api.add_resource(RecipeResource, "/recipes/<int:recipe_id>")
    api.add_resource(RecipePublishResource, "/recipes/<int:recipe_id>/publish")
    api.add_resource(UserListResource, "/users")
    api.add_resource(UserResource, "/users/<string:username>")
    api.add_resource(UserRecipeListResource, "/users/<string:username>/recipes")
    api.add_resource(UserActivateResource, "/users/activate/<string:token>")
    api.add_resource(UserAvatarUploadResource, "/users/avatar")
    api.add_resource(TokenResource, "/token")
    api.add_resource(MeResource, "/me")
    api.add_resource(RefreshResource, "/refresh")
    api.add_resource(RevokeResource, "/revoke")


if __name__ == "__main__":
    app = create_app()
    app.run()
