import enum

from app import db


class CastType(enum.Enum):
    ACTOR = 1
    DIRECTOR = 2
    WRITER = 3


takes_part = db.Table('takes_part',
                      db.Column('castMember_id', db.Integer, db.ForeignKey('castMember.id'), primary_key=True),
                      db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
                      db.Column('type', db.Enum(CastType))  # director or actor
                      )


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    year = db.Column(db.String)
    created_at = db.Column(db.Date)
    takes_partField = db.relationship('CastMember', secondary=takes_part, lazy='subquery',
                           backref=db.backref('movie', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "created_at": self.created_at
        }


class CastMember(db.Model):
    __tablename__ = 'castMember'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
