from .models import Movie, CastMember, TakesPart, CastType
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
        payload = {
            "success": True,
            "movie": movie.to_dict()
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

def listCastMembers_resolver(obj, info):
    try:
        castMembers = [_.to_dict() for _ in CastMember.query.all()]

        payload = {
            "success": True,
            "cast_members": castMembers
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
