import pandas as pd
from app import db

from app.exceptions import DataWriterException
from app.models import StarredReposModel


async def request_interface(request_dict):  # rename this to the puller and have it pass to the writer
    """Takes a request dict and calls puller and writer functions"""
    clean_data = _data_puller(request_dict['items'])
    try:
        _data_writer(clean_data)
        return 200
    except Exception as e:
        raise DataWriterException("There was issue writing the data")  # Move this to the writer


def _data_puller(lst_of_dicts):
    """Pulls and re-formats data from the github api"""
    data = pd.DataFrame(lst_of_dicts)
    trimmed_data = data['name', 'id', 'url', 'created_at', 'pushed_at', 'description', 'stargazers_count']
    trimmed_data.rename(columns={'id': 'repo_id', 'created_at': 'created_date', 'pushed_at': 'last_push_date',
                                 'stargazers_count': 'number_of_stars'}, inplace=True)
    # Select only the top 1000 based on star count
    top_1000_df = trimmed_data.nlargest(1000, 'number_of_stars')
    return top_1000_df


def _data_writer(df_to_write):
    """Updates a target table using a source dataframe"""
    # Gonna do this with straight sqlalchemy
    record_list = df_to_write.to_dict('records')
    # Because this only ever has 1000 iterations, a for loop is fine
    for record in record_list:
        # Assuming here that repo_id is unique
        if StarredReposModel.query.filter_by(repo_id=record['repo_id']).first() is not None:
            srm_inst_update = StarredReposModel()
            target_row = srm_inst_update.query.filter_by(repo_id=record['repo_id']).first()

            target_row.name = record['name']
            target_row.description = record['description']
            target_row.url = record['url']
            target_row.last_push_datetime = record['last_push_datetime']
            target_row.number_of_stars = record['number_of_stars']

            db.session.commit()

        else:
            srm_inst_insert = StarredReposModel()
            srm_inst_insert.from_dict(record)

            db.session.add(srm_inst_insert)
            db.session.commit()
