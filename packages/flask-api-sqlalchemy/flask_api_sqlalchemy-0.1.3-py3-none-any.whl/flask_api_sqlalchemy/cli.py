# src/flask_api_sqlalchemy/cli.py
# Command-line interface for the extension
import argparse
import importlib
import os
import sys
from typing import List, Optional

from . import __version__


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args (Optional[List[str]]): Command-line arguments

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description=(
            "flask-api-sqlalchemy - Automatically generate RESTful APIs "
            "from SQLAlchemy models"
        )
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Scaffold command to generate a basic app
    scaffold_parser = subparsers.add_parser(
        "scaffold", help="Generate a basic Flask application with the extension"
    )
    scaffold_parser.add_argument(
        "--dir",
        default=".",
        help="Directory to create the app in (default: current directory)",
    )
    scaffold_parser.add_argument(
        "--name", default="app", help="Name of the application module (default: app)"
    )

    # Info command to show detected models
    info_parser = subparsers.add_parser(
        "info", help="Show information about detected models"
    )
    info_parser.add_argument(
        "app_module", help="Path to the app module (e.g., app:app)"
    )

    return parser.parse_args(args)


def generate_scaffold(directory: str, name: str) -> None:
    """Generate a basic Flask application scaffold with the extension.

    Args:
        directory (str): Directory to create the app in
        name (str): Name of the application module
    """
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create app.py file
    app_path = os.path.join(directory, f"{name}.py")
    with open(app_path, "w") as f:
        f.write("""from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_api_sqlalchemy import Api

# Create Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your SQLAlchemy models
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

# Initialize the API extension
api = Api()
api.init_app(app, db)

if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True)
""")

    # Create requirements.txt file
    req_path = os.path.join(directory, "requirements.txt")
    with open(req_path, "w") as f:
        f.write("""flask>=2.0.0
flask-sqlalchemy>=3.0.0
flask-api-sqlalchemy>=0.1.3
""")

    print(f"Scaffold created in {os.path.abspath(directory)}")
    print(f"  - {name}.py: Main application file")
    print("  - requirements.txt: Dependencies")
    print("\nTo run the application:")
    print(f"  cd {directory}")
    print("  pip install -r requirements.txt")
    print(f"  python {name}.py")


def show_app_info(app_module: str) -> None:
    """Show information about detected models in an application.

    Args:
        app_module (str): Path to the app module (e.g., app:app)
    """
    try:
        module_path, app_var = app_module.split(":")
        sys.path.insert(0, os.getcwd())

        # Import the module
        module = importlib.import_module(module_path)
        app = getattr(module, app_var)

        # Check if our extension is initialized
        for extension in getattr(app, "extensions", {}).values():
            if hasattr(extension, "_discover_models"):
                # Found our extension
                print(f"Found flask-api-sqlalchemy extension in {app_module}")
                print("\nDetected models:")
                for model_name in extension.models:
                    print(f"  - {model_name}")
                print("\nAPI endpoints:")
                for model_name in extension.models:
                    resource_name = model_name.lower() + "s"  # Simple pluralization
                    print(f"  - GET    /api/{resource_name}/")
                    print(f"  - POST   /api/{resource_name}/")
                    print(f"  - GET    /api/{resource_name}/<id>")
                    print(f"  - PUT    /api/{resource_name}/<id>")
                    print(f"  - DELETE /api/{resource_name}/<id>")
                print("\nSwagger documentation available at:")
                print("  http://localhost:5000/api/docs")
                return

        print(f"flask-api-sqlalchemy extension not found in {app_module}")
    except ImportError:
        print(f"Could not import module {module_path}")
    except AttributeError:
        print(f"Could not find app variable {app_var} in module {module_path}")
    except ValueError:
        print("Invalid app module format. Use 'module:app_variable'")


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args (Optional[List[str]]): Command-line arguments

    Returns:
        int: Exit code
    """
    parsed_args = parse_args(args)

    if not parsed_args.command:
        print("Error: No command specified. Use --help for more information.")
        return 1

    if parsed_args.command == "scaffold":
        generate_scaffold(parsed_args.dir, parsed_args.name)
        return 0

    elif parsed_args.command == "info":
        show_app_info(parsed_args.app_module)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
