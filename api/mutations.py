from datetime import date

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Movie


@convert_kwargs_to_snake_case
def create_movie_resolver(obj, info, title, description):
    try:
        today = date.today()
        movie = Movie(
            title=title, description=description, created_at=today.strftime("%b-%d-%Y")
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