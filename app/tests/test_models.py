import datetime

import pytest

from app.models import StarredReposModel


@pytest.mark.parametrize(
        'repo_id, created_datetime, name, description, url, last_push_datetime, number_of_stars',
        [
            (
                    789,
                    datetime.datetime(2022, 1, 1, 12, 2, 1, 0),
                    'Test',
                    'This is a test',
                    'www.test.test',
                    datetime.datetime(2022, 1, 1, 12, 2, 1, 0),
                    393
            )]
)
def test_new_record(repo_id, created_datetime, name, description, url, last_push_datetime, number_of_stars) -> None:
    """
    Check that a new instance of StarredReposModel has its values assigned properly
    :param repo_id:
    :param created_datetime:
    :param name:
    :param description:
    :param url:
    :param last_push_datetime:
    :param number_of_stars:
    :return:
    """
    srm = StarredReposModel(
            repo_id=repo_id, created_datetime=created_datetime, name=name, description=description, url=url,
            last_push_datetime=last_push_datetime, number_of_stars=number_of_stars
    )
    assert srm.repo_id == repo_id
    assert srm.created_datetime == created_datetime
    assert srm.name == name
    assert srm.description == description
    assert srm.url == url
    assert srm.last_push_datetime == last_push_datetime
    assert srm.number_of_stars == number_of_stars


@pytest.mark.parametrize(
        'repo_id, created_datetime, name, description, url, last_push_datetime, number_of_stars, expected',
        [
            (
                    789,
                    datetime.datetime(2022, 1, 1, 12, 2, 1, 0),
                    'Test',
                    'This is a test',
                    'www.test.test',
                    datetime.datetime(2022, 1, 1, 12, 2, 1, 0),
                    393,
                    {
                        'repo_id': 789,
                        'created_datetime': datetime.datetime(2022, 1, 1, 12, 2, 1, 0),
                        'name': 'Test',
                        'description': 'This is a test',
                        'url': 'www.test.test',
                        'last_push_datetime': datetime.datetime(2022, 1, 1, 12, 2, 1, 0),
                        'number_of_stars': 393
                    }
            )]
)
def test_to_dict_method(repo_id, created_datetime, name, description, url, last_push_datetime, number_of_stars,
                        expected) -> None:
    """
    Test whether the to_dict method is outputting what we expect
    :param repo_id:
    :param created_datetime:
    :param name:
    :param description:
    :param url:
    :param last_push_datetime:
    :param number_of_stars:
    :param expected:
    :return:
    """
    srm = StarredReposModel(
            repo_id=repo_id, created_datetime=created_datetime, name=name, description=description, url=url,
            last_push_datetime=last_push_datetime, number_of_stars=number_of_stars
    )

    srm_dict = srm.to_dict()

    assert srm_dict == expected
