import enum
from app import db


class CastType(enum.Enum):
    ACTOR = 1
    DIRECTOR = 2
    WRITER = 3


class TakesPart(db.Model):
    __tablename__ = 'associationTakesPart'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    castMember_id = db.Column(db.Integer, db.ForeignKey('castMember.id'))
    type = db.Column(db.Enum(CastType))
    child = db.relationship("CastMember", back_populates="parents")
    parent = db.relationship("Movie", back_populates="children")

    def to_dict(self):
        return {
            "id": self.id,
            "movie_id": self.movie_id,
            "castMember_id": self.castMember_id,
            "type": self.type,
        }


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    year = db.Column(db.String)
    created_at = db.Column(db.Date)
    children = db.relationship("TakesPart", back_populates="parent")

    def to_dict(self):
        x = []
        _: TakesPart
        for _ in self.children:
            x.append({
                "idOfCastMember": _.castMember_id,
                "name": CastMember.query.get(_.castMember_id).name,
                "type": _.type.name
                })

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "year": self.year,
            "created_at": self.created_at,
            "cast_members": x
        }


class CastMember(db.Model):
    __tablename__ = 'castMember'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    parents = db.relationship("TakesPart", back_populates="child")


    def to_dict(self):
        x = []
        _: TakesPart
        for _ in self.parents:
            x.append({
                "": _.castMember_id,
                "movie": Movie.query.get(_.movie_id).to_dict(),
                "type": _.type.name
                })

        return {
            "id": self.id,
            "name": self.name,
            "movies_catalog": x
        }

# takes_part = db.Table('takes_part',
#                       db.Column('id', db.Integer, primary_key=True),
#                       db.Column('castMember_id', db.Integer, db.ForeignKey('castMember.id')),
#                       db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
#                       db.Column('type', db.Enum(CastType))  # director or actor
#                       )
