import datetime

import pytest
import pandas as pd

from app.github.functions import _data_writer, _data_cleaner
from app.main.functions import get_data
from app.models import StarredReposModel

FAKE_RESPONSE_JSON = [
    {
        'name': 'test_name',
        'id': 321,
        'html_url': 'test.test.test',
        'created_at': '2022-02-02T15:42:25Z',
        'pushed_at': '2022-02-02T15:42:25Z',
        'description': 'This description',
        'stargazers_count': 23,
        'extra': 'An extra column'
    },
    {
        'name': 'test_name2',
        'id': 328,
        'html_url': 'test.test.test',
        'created_at': '2022-02-02T15:42:25Z',
        'pushed_at': '2022-02-02T15:42:25Z',
        'description': 'This description',
        'stargazers_count': 255,
        'extra': 'Another extra column',
        'extraextra': 'Another other extra column'
    }
]

EXPECTED_SUCCESS_DATAFRAME = pd.DataFrame({
    'name': ['test_name', 'test_name2'],
    'repo_id': [321, 328],
    'url': ['test.test.test', 'test.test.test'],
    'created_date': ['2022-02-02T15:42:25Z', '2022-02-02T15:42:25Z'],
    'last_push_date': ['2022-02-02T15:42:25Z', '2022-02-02T15:42:25Z'],
    'description': ['This description', 'This description'],
    'number_of_stars': [23, 255]
})

EXPECTED_FAILURE_DATAFRAME = pd.DataFrame({
    'name': ['test_name', 'test_name2'],
    'repo_id': [321, 0],
    'url': ['test.test.test', 'test.test.test'],
    'created_date': ['2022-02-02T15:42:25Z', '2022-02-02T15:42:25Z'],
    'last_push_date': ['2022-02-02T15:42:25Z', '2022-02-02T15:42:25Z'],
    'description': ['This description', 'This description'],
    'number_of_stars': [23, 25]
})


@pytest.mark.parametrize(
        'expected',
        [
            (pytest.param(EXPECTED_SUCCESS_DATAFRAME,
                          id='success')),
            (pytest.param(EXPECTED_FAILURE_DATAFRAME,
                          marks=pytest.mark.xfail,
                          id='failure'))

        ]
)
def test_cleaner_success(expected):
    actual = _data_cleaner(FAKE_RESPONSE_JSON)

    assert actual.equals(expected)


@pytest.mark.parametrize(
        'repo_id',
        [
            (
                    321
            )
        ]
)
@pytest.mark.asyncio
async def test_writer_insert(repo_id):
    await _data_writer(EXPECTED_SUCCESS_DATAFRAME)

    actual = StarredReposModel.query.filter_by(repo_id=repo_id).first()

    assert actual
    assert actual.name == 'test_name'


@pytest.mark.parametrize(
        'update_df, expected_name, expected_star_count, repo_id',
        [
            (
                    pd.DataFrame({
                        'name': ['new_name'],
                        'repo_id': [321],
                        'url': ['test.test.test'],
                        'created_date': ['2022-02-02T15:42:25Z'],
                        'last_push_date': ['2022-02-02T15:42:25Z'],
                        'description': ['This description'],
                        'number_of_stars': [105]
                    }),
                    'new_name',
                    105,
                    321
            )
        ]
)
@pytest.mark.asyncio
async def test_writer_update(update_df, expected_name, expected_star_count, repo_id):
    # insert the records
    await _data_writer(EXPECTED_SUCCESS_DATAFRAME)

    # update with new data
    await _data_writer(update_df)

    actual = StarredReposModel.query.filter_by(repo_id=repo_id).first()

    assert actual
    assert actual.name == expected_name
    assert actual.number_of_stars == expected_star_count


@pytest.mark.parametrize(
        'repo_id, expected',
        [
            (2, [{
                'repo_id': 2, 'created_datetime': datetime.datetime(2022, 1, 1, 12, 0, 0, 0), 'name': 'Test',
                'description': 'A test', 'url': 'test.test.test',
                'last_push_datetime': datetime.datetime(2022, 1, 1, 12, 0, 0, 0), 'number_of_stars': 521
            }]),
            (None, [{
                'repo_id': 3, 'created_datetime': datetime.datetime(2022, 1, 1, 12, 0, 0, 0), 'name': 'Test2',
                'description': 'A test', 'url': 'test.test.test2',
                'last_push_datetime': datetime.datetime(2022, 1, 1, 12, 0, 0, 0), 'number_of_stars': 562
            }, {
                'repo_id': 2, 'created_datetime': datetime.datetime(2022, 1, 1, 12, 0, 0, 0), 'name': 'Test',
                'description': 'A test', 'url': 'test.test.test',
                'last_push_datetime': datetime.datetime(2022, 1, 1, 12, 0, 0, 0), 'number_of_stars': 521
            }])
        ]
)
@pytest.mark.asyncio
async def test_get_data(repo_id, expected):
    actual = await get_data(repo_id)

    assert actual == expected
