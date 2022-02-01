from app.api import bp
from app.models import StarredReposModel


@bp.route('/get-data')
def get_data():
    return {'data': [repo.to_dict() for repo in StarredReposModel.query]}
