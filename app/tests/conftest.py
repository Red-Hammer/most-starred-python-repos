import datetime

import pytest_asyncio

from app import create_app, db
from app.models import StarredReposModel
from test_config import TestConfig


@pytest_asyncio.fixture(scope='session', autouse=True)
def test_client():
    flask_app = create_app(TestConfig)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest_asyncio.fixture(scope='function', autouse=True)
def init_db(test_client):
    db.create_all()

    # insert some fake data
    x = StarredReposModel(
            repo_id=2, created_datetime=datetime.datetime(2022, 1, 1, 12, 0, 0, 0), name='Test',
            description='A test', url='test.test.test',
            last_push_datetime=datetime.datetime(2022, 1, 1, 12, 0, 0, 0), number_of_stars=521
    )
    db.session.add(x)
    db.session.commit()
    y = StarredReposModel(
            repo_id=3, created_datetime=datetime.datetime(2022, 1, 1, 12, 0, 0, 0), name='Test2',
            description='A test', url='test.test.test2',
            last_push_datetime=datetime.datetime(2022, 1, 1, 12, 0, 0, 0), number_of_stars=562
    )

    db.session.add(y)
    db.session.commit()

    yield

    db.drop_all()
