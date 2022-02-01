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

    def from_dict(self, row_dict):
        for key in row_dict.keys():
            setattr(self, key, row_dict[key])

    # I could probably write an update method here too using setattr
