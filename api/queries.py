from .models import Movie, CastMember, takes_part, CastType
from ariadne import convert_kwargs_to_snake_case


def listMovies_resolver(obj, info):
    try:
        movies = [_.to_dict() for _ in Movie.query.all()]
        print(movies)
        payload = {
            "success": True,
            "movies": movies
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def getMovie_resolver(obj, info, id):
    try:
        movie = Movie.query.get(id)
        castMembers = movie.takes_partField
        payload = {
            "success": True,
            "movie": movie.to_dict() | {"dokimi": castMembers[0]},
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo item matching id {id} not found"]
        }
    except Exception as e:
        payload = {
            "success": False,
            "errors": e
        }

    return payload
