import enum

from sqlalchemy import select

from app import db


class CastType(enum.Enum):
    ACTOR = 1
    DIRECTOR = 2
    WRITER = 3


takes_part = db.Table('takes_part',
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column('castMember_id', db.Integer, db.ForeignKey('castMember.id')),
                      db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                      db.Column('type', db.Enum(CastType))  # director or actor
                      )


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    year = db.Column(db.String)
    created_at = db.Column(db.Date)
    takes_partField: db.Table = db.relationship('CastMember', secondary=takes_part, lazy='subquery',
                                                backref=db.backref('movie', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "created_at": self.created_at,
            "dokimi": ["TIPOTA AKOMA"],

        }


class CastMember(db.Model):
    __tablename__ = 'castMember'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

