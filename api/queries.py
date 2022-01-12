from .models import Movie


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
