import requests

from flask import redirect, url_for, flash

from app.github import bp
from app.github.functions import request_interface


@bp.route('/update-database', methods=['GET', 'POST'])
async def update_database():
    # get all repos sorted by star rating
    # The max number of items per page is 100
    url = 'https://api.github.com/search/repositories?q=language:python&sort=stars&per_page=100'
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        flash('Rate Limit Exceeded, please wait a little while and try again')
        return redirect(url_for('main.home'))

    response_dict = response.json()

    status = await request_interface(response_dict)

    if status == 200:
        return redirect(url_for('main.home'))
    else:
        return 'Oh no! Something is amiss!'
