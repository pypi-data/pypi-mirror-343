
# flask-api-sqlalchemy

A Flask extension that automatically generates RESTful APIs from SQLAlchemy models.

## Features

- Simple integration with existing Flask and SQLAlchemy applications
- Automatic discovery of SQLAlchemy models
- Automatic mapping of SQLAlchemy types to Flask-RESTX API model types
- Fully generated REST endpoints for all models
- Comprehensive test suite
- Modern Python packaging

## Installation for Your Project

```bash
pip install flask-api-sqlalchemy
```

## Installation for Development

```bash
pip install -e .

## Usage

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_api import Api

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

## License

MIT

# LICENSE
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