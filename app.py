import logging
from flask import Flask
from flask import request
from imdb_api_query import Imdb_Queries
import json

imdb_object = Imdb_Queries()
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def landing_page():
    logger.info(f'{request.url} has been called')
    return "This is a IMDB API. The available routes are /get_dir_to_movie , /get_movie_details" \
           ",get_role_to_movie,\n" \
           "get_actor_to_role_to_movie,\n" \
           "get_movie_to_cast,\n" \
           "get_movie_to_reviews"


@app.route('/get_dir_to_movie', methods=['GET', 'POST'])
def director_to_mov_details():
    logger.info(f'{request.url} has been called')
    if request.method == 'GET':
        director = request.args.get('director_name')
        condition = imdb_object.director_to_movie(director)
        result = json.dumps(condition)
    else:
        director_data = request.json
        directors = director_data['director_name']
        condition = imdb_object.director_to_movie(directors)
        result = json.dumps(condition)
    return result


@app.route('/get_movie_details', methods=['GET', 'POST'])
def movies():
    logger.info(f'{request.url} has been called')
    if request.method == 'GET':
        movie = request.args.get('movie_name')
        condition = imdb_object.movie_details(movie)
        result = json.dumps(condition)
    else:
        movie_data = request.json
        movie = movie_data['movie_names']
        condition = imdb_object.movie_details(movie)
        result = json.dumps(condition)

    return result


@app.route('/get_role_to_movie', methods=['GET', 'POST'])
def role_to_mov_details():
    logger.info(f'{request.url} has been called')
    if request.method == 'GET':
        role = request.args.get('role_name')
        condition = imdb_object.roles_to_movies(role)
        result = json.dumps(condition)
    else:
        role_data = request.json
        roles = role_data["roles"]
        condition = imdb_object.roles_to_movies(roles)
        result = json.dumps(condition)
    return result


@app.route('/get_actor_to_role_to_movie', methods=['GET', 'POST'])
def actor_to_role_to_mov_details():
    logger.info(f'{request.url} has been called')
    if request.method == 'GET':
        actor = request.args.get('actor_name')
        condition = imdb_object.actors_movies_roles(actor)
        result = json.dumps(condition)
    else:
        actor_data = request.json
        actors = actor_data["actor_names"]
        condition = imdb_object.actors_movies_roles(actors)
        result = json.dumps(condition)
    return result


@app.route('/get_movie_to_cast', methods=['GET', 'POST'])
def movie_cast_details():
    logger.info(f'{request.url} has been called')
    if request.method == 'GET':
        movie = request.args.get('movie_name')
        condition = imdb_object.movies_cast(movie)
        result = json.dumps(condition)
    else:
        movie_data = request.json
        mov = movie_data["movie_name"]
        condition = imdb_object.movies_cast(mov)
        result = json.dumps(condition)
    logger.info(result)
    return result

@app.route('/get_movie_to_reviews', methods=['GET', 'POST'])
def movie_review_details():
    logger.info(f'{request.url} has been called')
    if request.method == 'GET':
        movie = request.args.get('movie_name')
        condition = imdb_object.movie_reviews(movie)
        result = json.dumps(condition)
    else:
        movie_data = request.json
        mov = movie_data["movie_name"]
        condition = imdb_object.movie_reviews(mov)
        result = json.dumps(condition)
    return result


if __name__ == '__main__':
    import sys
    print(sys.argv)
    app.run(host='0.0.0.0',
            port=5000)
