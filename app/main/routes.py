from flask import render_template
from app.main import bp
from app.models import StarredReposModel


@bp.route('/')
@bp.route('/home')
def home():
    repos = StarredReposModel.query
    return render_template(
            'main_view.html',
            title='Main Table',
            repos=repos
    )
