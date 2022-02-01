from flask import Blueprint

bp = Blueprint('github', __name__)

from app.github import routes