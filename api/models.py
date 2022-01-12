from app import db

takes_part = db.Table('takes_part',
                      db.Column('movieMember_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                      db.Column('movie_id', db.Integer, db.ForeignKey('movieMember.id'), primary_key=True),
                      db.Column('type', db.String)  # director or actor
                      )


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    year = db.Column(db.String)

    tags = db.relationship('Tag', secondary=takes_part, lazy='subquery',
                           backref=db.backref('movie', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
        }


class MovieMember(db.Model):  # An actor or a director
    __tablename__ = 'movieMember'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
