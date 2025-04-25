# src/flask_api_sqlalchemy/api.py
# Core API extension class
import logging
from http import HTTPStatus
from typing import Any, Optional

import inflection
from flask import Blueprint, Flask
from flask_restx import Api as RestxApi
from flask_restx import Namespace, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

# Configure logger
logger = logging.getLogger(__name__)


class Api:
    """flask-api-sqlalchemy extension class.

    This extension automatically generates RESTful APIs for SQLAlchemy models.
    It maps SQLAlchemy model attributes to Flask-RESTX fields and creates
    appropriate CRUD endpoints for each model.
    """

    def __init__(
        self,
        app: Optional[Flask] = None,
        db: Optional[SQLAlchemy] = None,
        doc: Optional[str] = "/docs",
        title: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        prefix: Optional[str] = "/api",
        default: Optional[str] = "default",
        default_label: Optional[str] = "Default namespace",
        default_id: Optional[str] = None,
        default_swagger_filename: Optional[str] = "swagger.json",
        # Optional parameters for API customization
        terms_url: Optional[str] = None,
        license: Optional[str] = None,
        license_url: Optional[str] = None,
        contact: Optional[str] = None,
        contact_url: Optional[str] = None,
        contact_email: Optional[str] = None,
        authorizations: Optional[dict] = None,
        security: Optional[dict] = None,
        validate: Optional[bool] = None,
        tags: Optional[list] = None,
        decorators: Optional[list] = None,
        catch_all_404s: Optional[bool] = False,
        serve_challenge_on_401: Optional[bool] = False,
        format_checker: Optional[Any] = None,
        url_scheme: Optional[str] = None,
        want_logs: bool = False,
        **kwargs,
    ) -> None:
        """Initialize the API extension.

        Args:
            app (Optional[Flask]): Flask application instance
            db (Optional[SQLAlchemy]): SQLAlchemy instance
        """
        self.app = app
        self.db = db
        self.blueprint = None
        self.api = None
        self.models = {}  # SQLAlchemy models
        self.api_models = {}  # Flask-RESTX API models
        self.namespaces = {}  # API namespaces
        self.title = title
        self.description = description
        self.version = version
        self.doc = doc
        self.prefix = prefix
        self.default = default
        self.default_label = default_label
        self.default_id = default_id
        self.default_swagger_filename = default_swagger_filename
        self.terms_url = terms_url
        self.license = license
        self.license_url = license_url
        self.contact = contact
        self.contact_url = contact_url
        self.contact_email = contact_email
        self.authorizations = authorizations
        self.security = security
        self.validate = validate
        self.tags = tags
        self.decorators = decorators
        self.catch_all_404s = catch_all_404s
        self.serve_challenge_on_401 = serve_challenge_on_401
        self.format_checker = format_checker
        self.url_scheme = url_scheme
        self.want_logs = want_logs
        self.kwargs = kwargs

        self._api = None  # Flask-RESTX API instance

        # If app and db are provided, initialize the extension
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app: Flask, db: SQLAlchemy) -> None:
        """Initialize the extension with Flask app and SQLAlchemy instance.

        This method follows the Flask extension pattern, allowing for
        deferred initialization.

        Args:
            app (Flask): Flask application instance
            db (SQLAlchemy): SQLAlchemy instance
        """
        self.app = app
        self.db = db

        # Create API blueprint
        self.blueprint = Blueprint("SQLAlchemy API", __name__, url_prefix=self.prefix)

        # Create Flask-RESTX API
        self.api = RestxApi(
            self.blueprint,
            version=self.version or app.config.get("API_VERSION", "1.0"),
            title=self.title or app.config.get("API_TITLE", "Flask-SQLAlchemy API"),
            description=self.description
            or app.config.get(
                "API_DESCRIPTION", "Automatically generated API from SQLAlchemy models"
            ),
            doc=self.doc,
            default=self.default,
            terms_url=self.terms_url,
            license=self.license,
            license_url=self.license_url,
            contact=self.contact,
            contact_url=self.contact_url,
            contact_email=self.contact_email,
            authorizations=self.authorizations,
            security=self.security,
            validate=self.validate,
            tags=self.tags,
            prefix=self.prefix,
            default_label=self.default_label,
            default_id=self.default_id,
            default_swagger_filename=self.default_swagger_filename,
            decorators=self.decorators,
            catch_all_404s=self.catch_all_404s,
            serve_challenge_on_401=self.serve_challenge_on_401,
            format_checker=self.format_checker,
            url_scheme=self.url_scheme,
            **self.kwargs,
        )

        # Register the blueprint with the Flask app
        app.register_blueprint(self.blueprint)

        # Register models and create APIs
        with app.app_context():
            self._discover_models()
            self._generate_api_models()
            self._create_endpoints()

    def _discover_models(self) -> None:
        """Discover all SQLAlchemy models in the application."""
        # Find all models defined in the SQLAlchemy instance
        models = {}

        # Use Python's built-in __subclasses__ to find all model classes
        for cls in self.db.Model.__subclasses__():
            model_name = cls.__name__
            if model_name != "Base" and not model_name.startswith("_"):
                if self.want_logs:
                    logger.info(f"Discovered model: {model_name}")
                models[model_name] = cls

        # Store discovered models
        self.models = models

        # If no models were found, log a warning
        if not models:
            logger.warning(
                "No SQLAlchemy models were discovered."
                + "Make sure your models are properly defined."
            )

    def _map_sqlalchemy_type_to_restx_field(
        self, column_type: Any, column_nullable: bool
    ) -> fields.Raw:
        """Map SQLAlchemy column types to Flask-RESTX field types.

        Args:
            column_type (Any): SQLAlchemy column type
            column_nullable (bool): Whether the column is nullable

        Returns:
            fields.Raw: Appropriate Flask-RESTX field type
        """
        # Map SQLAlchemy types to Flask-RESTX field types
        type_name = column_type.__class__.__name__.lower()

        # Special handling for ARRAY types
        if type_name == "array":
            # Get the SQLAlchemy type of array elements
            item_type = column_type.item_type
            # Recursively map the item type to a Flask-RESTX field
            item_field = self._map_sqlalchemy_type_to_restx_field(item_type, True)
            # Create a List field with the appropriate item field
            return fields.List(item_field, required=not column_nullable)

        # Define mappings from SQLAlchemy types to Flask-RESTX fields
        type_map = {
            "integer": fields.Integer,
            "biginteger": fields.Integer,
            "smallinteger": fields.Integer,
            "string": fields.String,
            "text": fields.String,
            "unicode": fields.String,
            "unicodetext": fields.String,
            "boolean": fields.Boolean,
            "date": fields.Date,
            "datetime": fields.DateTime,
            "float": fields.Float,
            "numeric": fields.Float,
            "decimal": fields.Float,
            "enum": fields.String,
            "json": fields.Raw,
            "jsonb": fields.Raw,
            "largebinary": fields.String,
            "blob": fields.String,
            "binary": fields.String,
            "uuid": fields.String,
        }

        # Get appropriate field type
        field_type = type_map.get(type_name, fields.Raw)

        # Create field with appropriate required setting
        return field_type(required=not column_nullable)

    def _generate_api_models(self) -> None:
        """Generate Flask-RESTX API models from SQLAlchemy models.

        For each discovered SQLAlchemy model, this method creates a corresponding
        Flask-RESTX model with appropriately mapped fields.
        """
        for model_name, model in self.models.items():
            # Create a namespace for the model
            namespace_name = inflection.pluralize(model_name.lower())
            namespace = Namespace(
                namespace_name, description=f"{model_name} operations"
            )

            # Get model columns
            mapper = inspect(model)
            model_fields = {}

            # Add primary key fields
            for column in mapper.primary_key:
                model_fields[column.name] = fields.Integer(
                    readonly=True, description=f"{column.name} identifier"
                )

            # Add regular fields
            for column in mapper.columns:
                # Skip primary key columns, already added
                if column.primary_key:
                    continue

                # Map SQLAlchemy type to Flask-RESTX field
                field = self._map_sqlalchemy_type_to_restx_field(
                    column.type, column.nullable
                )

                # Add description
                field.description = f"{column.name} field"

                # Add to model fields
                model_fields[column.name] = field

            # Create the API model
            api_model = namespace.model(model_name, model_fields)

            # Store namespace and API model
            self.namespaces[model_name] = namespace
            self.api_models[model_name] = api_model

            # Add namespace to API
            self.api.add_namespace(namespace)

            if self.want_logs:
                logger.info(f"Created API model for {model_name}")

    def _create_endpoints(self) -> None:
        """Create API endpoints for each model."""
        for model_name, model in self.models.items():
            # Get namespace and API model
            namespace = self.namespaces[model_name]
            api_model = self.api_models[model_name]

            # Create resource name (pluralized)
            resource_name = inflection.pluralize(model_name.lower())

            # Store db reference for use in inner classes
            db = self.db

            # Create a factory function to ensure each class has its own bound model
            def create_collection_resource(model, model_name):
                """Create a collection resource for the model."""

                @namespace.route("/")
                @namespace.response(HTTPStatus.NOT_FOUND, f"{model_name} not found")
                @namespace.response(HTTPStatus.BAD_REQUEST, "Invalid request")
                @namespace.response(
                    HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error"
                )  # noqa: E501
                @namespace.doc(f"get_{resource_name}")
                class Collection(Resource):
                    """Collection resource for the model."""

                    # Store model references securely
                    _model = model
                    _model_name = model_name
                    want_logs = self.want_logs

                    @namespace.doc(f"list_{resource_name}")
                    @namespace.marshal_list_with(api_model)
                    def get(self):
                        """Get all resources."""
                        # Use direct query with the bound model
                        return db.session.query(self._model).all()

                    @namespace.doc(f"create_{inflection.singularize(resource_name)}")
                    @namespace.expect(api_model)
                    @namespace.marshal_with(api_model, code=HTTPStatus.CREATED)
                    def post(self):
                        """Create a new resource."""
                        if self.want_logs:
                            logger.info(f"Creating a new {self._model_name} instance")

                        # Get request data
                        data = namespace.payload

                        # Validate required fields
                        for column in inspect(self._model).columns:
                            if not column.nullable and not column.primary_key:
                                if column.name not in data or data[column.name] is None:
                                    namespace.abort(
                                        400, f"Missing required field: {column.name}"
                                    )

                        # Create new instance using the class's model
                        instance = self._model()

                        # Update instance with request data
                        for key, value in data.items():
                            if hasattr(instance, key):
                                setattr(instance, key, value)

                        # Save to database
                        db.session.add(instance)
                        try:
                            db.session.commit()
                        except IntegrityError as e:
                            db.session.rollback()
                            logger.error(
                                f"Integrity error creating {self._model_name}: {e}"
                            )  # noqa: E501
                            namespace.abort(
                                HTTPStatus.BAD_REQUEST,
                                f"Integrity error creating {self._model_name}",
                            )
                        except Exception as e:
                            db.session.rollback()
                            logger.error(f"Error creating {self._model_name}: {e}")
                            namespace.abort(
                                HTTPStatus.INTERNAL_SERVER_ERROR,
                                f"Error creating {self._model_name}",
                            )

                        return instance, HTTPStatus.CREATED

                return Collection

            # Similar factory for Item resource...
            def create_item_resource(model, model_name):
                @namespace.route("/<int:id>")
                @namespace.param("id", f"The {model_name} identifier")
                @namespace.response(HTTPStatus.NOT_FOUND, f"{model_name} not found")
                @namespace.response(HTTPStatus.BAD_REQUEST, "Invalid request")
                @namespace.response(
                    HTTPStatus.INTERNAL_SERVER_ERROR, "Internal server error"
                )  # noqa: E501
                class Item(Resource):
                    """Resource for a specific item."""

                    # Store model references securely
                    _model = model
                    _model_name = model_name
                    want_logs = self.want_logs

                    @namespace.doc(f"get_{inflection.singularize(resource_name)}")
                    @namespace.marshal_with(api_model)
                    def get(self, id):
                        """Get a specific resource."""
                        instance = db.session.query(self._model).get(id)
                        if not instance:
                            namespace.abort(
                                HTTPStatus.NOT_FOUND,
                                f"{self._model_name} with id {id} not found",  # noqa: E501
                            )
                        return instance

                    @namespace.doc(f"update_{inflection.singularize(resource_name)}")
                    @namespace.expect(api_model)
                    @namespace.marshal_with(api_model)
                    def put(self, id):
                        """Update a specific resource."""
                        if self.want_logs:
                            logger.debug(f"Updating {self._model_name} with id {id}")

                        instance = db.session.query(self._model).get(id)

                        if not instance:
                            logger.warning(f"{self._model_name} with id {id} not found")
                            namespace.abort(
                                HTTPStatus.NOT_FOUND,
                                f"{self._model_name} with id {id} not found",
                            )

                        # Get request data
                        data = namespace.payload

                        # Update instance with request data
                        for key, value in data.items():
                            if hasattr(instance, key):
                                setattr(instance, key, value)

                        # Save to database
                        db.session.commit()

                        return instance

                    @namespace.doc(f"delete_{inflection.singularize(resource_name)}")
                    @namespace.response(HTTPStatus.NO_CONTENT, f"{model_name} deleted")
                    def delete(self, id):
                        """Delete a specific resource."""
                        # Use session query instead of model.query
                        instance = db.session.query(self._model).get(id)
                        if not instance:
                            namespace.abort(
                                HTTPStatus.NOT_FOUND,
                                f"{self._model_name} with id {id} not found",  # noqa: E501
                            )

                        # Delete from database
                        db.session.delete(instance)
                        db.session.commit()

                        return "", HTTPStatus.NO_CONTENT

                return Item

            # Create the resources using our factory functions
            create_collection_resource(model, model_name)
            create_item_resource(model, model_name)

            if self.want_logs:
                logger.info(f"Created endpoints for {model_name}")
