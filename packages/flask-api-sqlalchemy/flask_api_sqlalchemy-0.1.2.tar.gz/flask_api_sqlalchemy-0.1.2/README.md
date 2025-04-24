# flask-api-sqlalchemy

A Flask extension that automatically generates RESTful APIs from SQLAlchemy models.

<p align="center">
<a href="https://github.com/mccarthysean/flask-api-sqlalchemy/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/mccarthysean/flask-api-sqlalchemy/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/mccarthysean/flask-api-sqlalchemy" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/mccarthysean/flask-api-sqlalchemy?color=%2334D058" alt="Coverage">
</a>
<a href="https://github.com/mccarthysean/flask-api-sqlalchemy/actions?query=workflow%3Apypi" target="_blank">
    <img src="https://github.com/mccarthysean/flask-api-sqlalchemy/workflows/Upload%20Package%20to%20PyPI/badge.svg" alt="Publish">
</a>
<a href="https://pypi.org/project/flask-api-sqlalchemy" target="_blank">
    <img src="https://img.shields.io/pypi/v/flask-api-sqlalchemy?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/flask-api-sqlalchemy/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/flask-api-sqlalchemy.svg" alt="Python Versions">
</a>
</p>


## Features

- Simple integration with existing Flask and SQLAlchemy applications
- Automatic discovery of SQLAlchemy models
- Automatic mapping of SQLAlchemy types to Flask-RESTX API model types
- Fully generated REST endpoints for all models
- Comprehensive test suite
- Interactive Swagger UI documentation
- Command-line scaffolding tool for quick setup

## Installation for Your Project

[Install from PyPI](https://pypi.org/project/flask-api-sqlalchemy/)

```bash
pip install flask-api-sqlalchemy
```

## Installation for Development

```bash
pip install -e .
```

## Quick Start

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_api_sqlalchemy import Api

# Create Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your SQLAlchemy models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Initialize the API extension
api = Api()
api.init_app(app, db)

if __name__ == '__main__':
    app.run()
```

That's it! The extension automatically:
1. Discovers all your SQLAlchemy models
2. Creates appropriate Flask-RESTX models and serializers
3. Generates full CRUD API endpoints for each model
4. Provides Swagger documentation at `/api/docs`

## How It Works

`flask-api-sqlalchemy` analyzes your SQLAlchemy models and automatically creates REST API endpoints with appropriate data validation:

1. **Model Discovery**: The extension finds all SQLAlchemy models in your application
2. **Type Mapping**: SQLAlchemy column types are mapped to appropriate Flask-RESTX field types
3. **API Generation**: CRUD endpoints are created for each model with proper validation
4. **Documentation**: Swagger UI is automatically generated for testing and exploration

## Detailed Usage

### Model Relationships

The extension supports models with relationships:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='items')
```

### Generated Endpoints

For each model, the following RESTful endpoints are automatically created:

| HTTP Method | Endpoint          | Description             | Status Codes      |
|-------------|-------------------|-------------------------| -----------------|
| GET         | /api/{models}/    | List all resources     | 200 OK           |
| POST        | /api/{models}/    | Create a new resource  | 201 Created, 400 Bad Request |
| GET         | /api/{models}/{id} | Get a specific resource | 200 OK, 404 Not Found |
| PUT         | /api/{models}/{id} | Update a specific resource | 200 OK, 404 Not Found |
| DELETE      | /api/{models}/{id} | Delete a specific resource | 204 No Content, 404 Not Found |

### Command-Line Interface

This extension includes a helpful CLI for setting up new projects:

```bash
# Create a new Flask application with flask-api-sqlalchemy
flask-api-sqlalchemy scaffold --dir myapp

# Show information about models in an existing application
flask-api-sqlalchemy info app:app
```

### Type Mapping

SQLAlchemy column types are automatically mapped to appropriate Flask-RESTX fields:

| SQLAlchemy Type | Flask-RESTX Field |
|-----------------|-------------------|
| Integer         | fields.Integer    |
| String          | fields.String     |
| Text            | fields.String     |
| Boolean         | fields.Boolean    |
| Date            | fields.Date       |
| DateTime        | fields.DateTime   |
| Float           | fields.Float      |
| ... and many more |                  |

### Configuration Options

Configure the extension through Flask application config:

```python
app.config['API_TITLE'] = "My Custom API"  # Default: "Flask-SQLAlchemy API"
app.config['API_DESCRIPTION'] = "Custom description"  # Default: "Automatically generated API from SQLAlchemy models"
app.config['API_VERSION'] = "1.0"
```

### Data Validation

The extension automatically validates incoming data:

- Required fields (non-nullable columns) are enforced
- Data types are validated according to SQLAlchemy column types
- Helpful error messages are returned for invalid data

## Troubleshooting

### No Models Found

If no models are discovered, ensure:
- Your models inherit from `db.Model`
- Models are imported before initializing the API
- The db instance passed to `api.init_app()` is the same one used to define your models

### Missing Endpoints

Check that:
- The Flask blueprint is registered correctly (happens automatically in `init_app()`)
- Your app context is active when accessing endpoints
- Names are correctly pluralized in the URL (e.g., `/api/users/` not `/api/user/`)

## License

MIT License

Copyright (c) 2025 Sean McCarthy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author Info

Sean McCarthy is Chief Data Scientist at [IJACK Technologies Inc](https://myijack.com), a leading manufacturer of fully-automated pumps to green the oil and gas industry.

<br>
<a href="https://mccarthysean.dev">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/mccarthysean.svg?sanitize=1" alt="Sean McCarthy's blog">
</a>
<a href="https://www.linkedin.com/in/seanmccarthy2/">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/linkedin.svg?sanitize=1" alt="LinkedIn">
</a>
<a href="https://github.com/mccarthysean">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/github.svg?sanitize=1" alt="GitHub">
</a>
<a href="https://twitter.com/mccarthysean">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/twitter.svg?sanitize=1" alt="Twitter">
</a>
<a href="https://www.facebook.com/sean.mccarth">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/facebook.svg?sanitize=1" alt="Facebook">
</a>
<a href="https://medium.com/@mccarthysean">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/medium.svg?sanitize=1" alt="Medium">
</a>
<a href="https://www.instagram.com/mccarthysean/">
    <img src="https://raw.githubusercontent.com/mccarthysean/flask-api-sqlalchemy/main/docs/assets/instagram.svg?sanitize=1" alt="Instagram">
</a>