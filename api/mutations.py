from datetime import date

import graphql.error.graphql_error
from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Movie, CastMember, takes_part, CastType


@convert_kwargs_to_snake_case
def create_movie_resolver(obj, info, title, description, year):
    try:
        today = date.today()
        movie = Movie(
            title=title,
            description=description,
            year=year,
            created_at=date.today()
        )
        db.session.add(movie)
        db.session.commit()
        payload = {
            "success": True,
            "movie": movie.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload


@convert_kwargs_to_snake_case
def update_movie_resolver(obj, info, id, title, description):
    try:
        movie = Movie.query.get(id)
        if movie:
            movie.title = title
            movie.description = description
        db.session.add(movie)
        db.session.commit()
        payload = {
            "success": True,
            "movie": movie.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": ["item matching id {id} not found"]
        }

    return payload


@convert_kwargs_to_snake_case
def delete_movie_resolver(obj, info, id):
    try:
        movie = Movie.query.get(id)
        db.session.delete(movie)
        db.session.commit()
        payload = {"success": True, "movie": movie.to_dict()}

    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }

    return payload


@convert_kwargs_to_snake_case
def create_movie_cast_member_resolver(obj, info, name):
    try:
        castMember = CastMember(
            name=name
        )
        db.session.add(castMember)
        db.session.commit()
        payload = {
            "success": True,
            "castMember": castMember.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": [e]
        }

    return payload


@convert_kwargs_to_snake_case
def addCastMemberInMovie(obj, info, cast_id, movie_id, category):
    try:
        print(category)
        movieObj = Movie.query.get(movie_id)
        castMemberObj = CastMember.query.get(cast_id)

        statement = takes_part.insert().values(castMember_id=castMemberObj.id, movie_id=movieObj.id,
                                               type=CastType[category])
        db.session.execute(statement)
        db.session.commit()
        payload = {
            "success": True,
            "errors": []
        }

    except graphql.error.graphql_error.GraphQLError:
        payload = {
            "success": False,
            "errors": ["Already exists"]
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": ["Not found"]
        }

    return payload
