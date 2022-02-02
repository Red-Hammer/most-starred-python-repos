from operator import itemgetter
from typing import List, Dict

from app.models import StarredReposModel


async def get_data(repo_id: int = None) -> List[Dict]:
    if not repo_id:
        # Pre-sort the records
        lst_of_records = [repo.to_dict() for repo in StarredReposModel.query]
        return sorted(lst_of_records, key=itemgetter('number_of_stars'), reverse=True)
    else:
        repo = StarredReposModel.query.filter_by(repo_id=repo_id).first()
        return [repo.to_dict()]
