"""
Recipe Sharing Platform (API)
"""

from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

recipes = [
    {
        "id": 1,
        "name": "Egg Salad",
        "description": "this is a lovely egg salad recipe",
    },
    {
        "id": 2,
        "name": "Tomato Pasta",
        "description": "this is a lovely tomato pasta recipe",
    },
    {
        "id": 3,
        "name": "Sample",
        "description": "Sample Description",
    },
]


@app.route("/recipes", methods=["GET"])
def get_recipes():
    return jsonify({"data": recipes})


@app.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    if recipe := next(
        (recipe for recipe in recipes if recipe["id"] == recipe_id), None
    ):
        return jsonify({"data": recipe})

    return jsonify({"message": "recipe not found"}), HTTPStatus.NOT_FOUND


@app.route("/recipes", methods=["POST"])
def create_recipe():
    data = request.json
    name = data.get("name")
    description = data.get("description")

    recipe = {
        "id": len(recipes) + 1,
        "name": name,
        "description": description,
    }

    recipes.append(recipe)

    return jsonify({"data": recipe}), HTTPStatus.CREATED


@app.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    if recipe := next(
        (recipe for recipe in recipes if recipe["id"] == recipe_id), None
    ):
        data = request.json
        recipe.update(
            {"name": data.get("name"), "description": data.get("description")}
        )

        return jsonify(recipe)

    return jsonify({"message": "recipe not found"}), HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    app.run(debug=True)
