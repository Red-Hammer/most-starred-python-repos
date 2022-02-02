from flask import render_template

from app.main import bp
from app.main.functions import get_data


@bp.route('/')
@bp.route('/home')
async def home():
    repos = await get_data()
    return render_template(
            'main_view.html',
            title='Top Starred Python Repos on Github',
            repos=repos
    )


@bp.route('/detail-view/<int:repo_id>', methods=['GET', 'POST'])
async def detail_view(repo_id: int):
    repo = await get_data(repo_id)  # singular repo is still passed via a list to maintain consistency
    return render_template(
            'detail_view.html',
            title='Repo Detail',
            repo=repo[0]
    )
