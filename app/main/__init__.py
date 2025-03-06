""" main initializer for the flask routes """
from flask import Blueprint

BP = Blueprint('main', __name__)

from app.main import \
    routes  # noqa: F401  # pylint:disable=wrong-import-position
