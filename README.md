# SmileCook Recipe API

SmileCook Recipe API is a RESTful API designed to provide access to a collection of recipes. It allows users to perform various operations such as fetching recipes, adding new recipes, updating existing recipes, and deleting recipes.

## Features

- **Get Recipes**: Retrieve a list of recipes with details such as name, ingredients, instructions, and more.
- **Add Recipe**: Add a new recipe to the database.
- **Update Recipe**: Modify an existing recipe.
- **Delete Recipe**: Remove a recipe from the database.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/Just2Deep/recipe_api.git
   ```

2. Navigate to the project directory:

   ```
   cd recipe_api/smilecook
   ```

3. Create Virtual env & Install dependencies:

   ```
   python -m venv venv
   source venv/Scripts/activate
   pip install -r requirements.txt
   ```

4. Run the app:

   ```
   python main.py
   ```

## API Endpoints

### User Management
 - POST /users/: Register a new user.
 - POST /api/auth/login/: Log in and obtain a JWT token.
 - POST /api/auth/logout/: Log out and invalidate the JWT token.
  
### Recipes
 - GET /recipes/: Retrieve all recipes.
 - POST /recipes/: Add a new recipe.
 - GET /recipes/{id}/: Retrieve a specific recipe by ID.
 - PUT /recipes/{id}/: Update a specific recipe by ID.
 - DELETE /recipes/{id}/: Delete a specific recipe by ID.

## Usage

### Example Requests

- **GET /recipes/**

  ```
  GET http://localhost:8000/recipes/
  ```

- **POST /recipes/**

  ```
  POST http://localhost:8000/recipes/
  Content-Type: application/json

  {
      "name": "Spaghetti Carbonara",
      "ingredients": ["spaghetti", "eggs", "bacon", "parmesan cheese"],
      "instructions": "Cook spaghetti according to package instructions. In a separate pan, fry bacon until crispy. In a bowl, mix eggs and parmesan cheese. Drain spaghetti and toss with egg mixture. Add crispy bacon. Serve hot."
  }
  ```

- **GET /recipes/{id}/**

  ```
  GET http://localhost:8000/recipes/1/
  ```

- **PUT /recipes/{id}/**

  ```
  PUT http://localhost:8000/recipes/1/
  Content-Type: application/json

  {
      "name": "Updated Spaghetti Carbonara",
      "ingredients": ["spaghetti", "eggs", "bacon", "parmesan cheese", "black pepper"],
      "instructions": "Cook spaghetti according to package instructions. In a separate pan, fry bacon until crispy. In a bowl, mix eggs, parmesan cheese, and black pepper. Drain spaghetti and toss with egg mixture. Add crispy bacon. Serve hot."
  }
  ```

- **DELETE /recipes/{id}/**

  ```
  DELETE http://localhost:8000/recipes/1/
  ```

### Response Format

The API returns JSON-formatted responses with appropriate status codes.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to adjust and expand it as needed!