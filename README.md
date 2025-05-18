# 🍳 SmileCook Recipe API

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/Flask-green)
![Status](https://img.shields.io/badge/status-active-success)

A modern, RESTful API for managing and sharing recipes. Built with FastAPI and designed for scalability and ease of use.

[Features](#features) • [Installation](#installation) • [API Documentation](#api-documentation) • [Contributing](#contributing) • [License](#license)

</div>

## ✨ Features

-   🔍 **Recipe Management**

    -   Get all recipes with pagination and filtering
    -   Search recipes by name, ingredients, or tags
    -   Get detailed recipe information
    -   Add new recipes with validation
    -   Update existing recipes
    -   Delete recipes

-   🛠️ **Technical Features**
    -   RESTful API design
    -   JSON response format
    -   Input validation
    -   Error handling
    -   Rate limiting
    -   CORS support
    -   Swagger/OpenAPI documentation

## 🚀 Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/Just2Deep/recipe_api.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd recipe_api/smilecook
    ```

3. **Set up virtual environment**

    ```bash
    # Create virtual environment
    python -m venv venv

    # Activate virtual environment
    # On Windows
    venv\Scripts\activate
    # On Unix or MacOS
    source venv/bin/activate
    ```

4. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application**
    ```bash
    python main.py
    ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

For detailed API documentation, visit our [API Documentation](https://just2deep.github.io/recipe_api/)

### Example API Usage

```python
import requests

# Get all recipes
response = requests.get('http://localhost:8000/api/recipes')

# Get a specific recipe
response = requests.get('http://localhost:8000/api/recipes/1')

# Add a new recipe
new_recipe = {
    "name": "Chocolate Cake",
    "ingredients": ["flour", "sugar", "cocoa powder"],
    "instructions": "Mix ingredients and bake"
}
response = requests.post('http://localhost:8000/api/recipes', json=new_recipe)
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 📞 Support

If you encounter any issues or have questions, please:

-   Open an issue in the GitHub repository
-   Contact the maintainers

---

<div align="center">
Made with ❤️ by Deep
</div>
