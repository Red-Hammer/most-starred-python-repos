import requests

from app.github import bp
from app.github.functions import request_interface


@bp.route('/update-database', methods=['GET', 'POST'])
async def update_database():
    # get all repos sorted by star rating
    # The max number of items per page is 100
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars&per_page=100'
    response = requests.get(url)
    response_dict = response.json()

    status = await request_interface(response_dict)

    if status == 200:
        return 'It worked!'
    else:
        return 'Oh no! Something is amiss!'
