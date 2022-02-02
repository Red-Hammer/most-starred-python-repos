from typing import Dict

from app import db


class StarredReposModel(db.Model):
    """Data Model for the Most Starred Repos Table"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_id = db.Column(db.Integer, unique=True)
    created_datetime = db.Column(db.DateTime)
    name = db.Column(db.Unicode)
    description = db.Column(db.Unicode)
    url = db.Column(db.Unicode)
    last_push_datetime = db.Column(db.DateTime)
    number_of_stars = db.Column(db.Integer)


    def to_dict(self) -> Dict:
        """
        Pulls an instance's table row into a dictionary
        :return: Dictionary representing one table record
        """
        return {
            'repo_id': self.repo_id,
            'created_datetime': self.created_datetime,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'last_push_datetime': self.last_push_datetime,
            'number_of_stars': self.number_of_stars
        }
