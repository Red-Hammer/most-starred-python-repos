import dateutil.parser
from typing import List, Dict

import pandas as pd

from app import db
from app.exceptions import DataWriterException
from app.models import StarredReposModel


async def request_interface(request_dict: List[Dict]) -> int:
    """
    Takes a request dict and calls puller and writer functions
    :param request_dict: list of dictionaries from a request
    :return: int
    """
    clean_data = _data_cleaner(request_dict['items'])
    try:
        await _data_writer(clean_data)
        return 200
    except Exception as e:
        raise DataWriterException("There was issue writing the data")


def _data_cleaner(lst_of_dicts: List[Dict]) -> pd.DataFrame:
    """
    Pulls and re-formats data from the GitHub api
    :param lst_of_dicts: list of dictionaries
    :return: pd.DataFrame
    """
    data = pd.DataFrame(lst_of_dicts)
    trimmed_data = data[['name', 'id', 'html_url', 'created_at', 'pushed_at', 'description', 'stargazers_count']]
    renamed_data = trimmed_data.rename(
            columns={'id': 'repo_id', 'html_url': 'url', 'created_at': 'created_date', 'pushed_at': 'last_push_date',
                     'stargazers_count': 'number_of_stars'}, inplace=False)

    return renamed_data


async def _data_writer(df_to_write: pd.DataFrame) -> None:
    """
    Updates the StarredReposModel table using a source dataframe
    :param df_to_write: DataFrame to use as source
    :return: None
    """
    record_list = df_to_write.to_dict('records')
    # Because this only ever has 100 iterations, a for loop is fine
    for record in record_list:
        # Assuming here that repo_id is unique
        if StarredReposModel.query.filter_by(repo_id=record['repo_id']).first() is not None:
            srm_inst_update = StarredReposModel()
            target_row = srm_inst_update.query.filter_by(repo_id=record['repo_id']).first()

            target_row.name = record['name']
            target_row.description = record['description']
            target_row.url = record['url']
            target_row.last_push_datetime = dateutil.parser.isoparse(record['last_push_date'])
            target_row.number_of_stars = record['number_of_stars']

            db.session.commit()

        else:
            srm_inst_insert = StarredReposModel(
                    repo_id=record['repo_id'],
                    created_datetime=dateutil.parser.isoparse(record['created_date']),
                    name=record['name'],
                    description=record['description'],
                    url=record['url'],
                    last_push_datetime=dateutil.parser.isoparse(record['last_push_date']),
                    number_of_stars=record['number_of_stars']
            )

            db.session.add(srm_inst_insert)
            db.session.commit()
