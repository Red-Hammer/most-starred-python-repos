from app.api import bp
from app.models import StarredReposModel


@bp.route('/get-data')
def get_data(repo_id=None):
    if not repo_id:
        return [repo.to_dict() for repo in StarredReposModel.query]
    else:
        repo = StarredReposModel.query.filter_by(repo_id=repo_id).first()
        return repo.to_dict()
