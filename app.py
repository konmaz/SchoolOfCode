from api import app, db

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.queries import listMovies_resolver, getMovie_resolver
from api.mutations import create_movie_resolver, update_movie_resolver, delete_movie_resolver, create_movie_cast_member_resolver, addCastMemberInMovie

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field("listMovies", listMovies_resolver)
query.set_field("getMovie", getMovie_resolver)

mutation.set_field("createMovie", create_movie_resolver)
mutation.set_field("updateMovie", update_movie_resolver)
mutation.set_field("deleteMovie", delete_movie_resolver)
mutation.set_field("createCastMember", create_movie_cast_member_resolver)
mutation.set_field("addCastMemberInMovie", addCastMemberInMovie)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

# from datetime import datetime
# db.create_all()
# newMovieObj = Movie(title="Pulp Fiction",
#                     description="The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
#                     year="1994",
#                     created_at=datetime.today().date(),
#                     )
# db.session.add(newMovieObj)
# db.session.commit()


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
