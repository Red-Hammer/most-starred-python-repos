from app.github import bp
import http
import requests
from app.github.functions import request_interface


@bp.route('/update-database', methods=['GET', 'POST'])
def update_database():

    # get all repos sorted by star rating
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
    response = requests.get(url)
    response_dict = response.json()

    status = await request_interface(response_dict)

    if status == 200:
        return http.HTTPStatus.OK
    else:
        return http.HTTPStatus.INTERNAL_SERVER_ERROR

