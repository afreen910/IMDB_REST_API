import os
import toml
import psycopg2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = toml.load("./config.toml")

# DB_NAME = os.environ['DB_NAME']
# DB_HOST = os.environ['DB_HOST']
# DB_USER = os.environ['DB_USER']
# DB_PASSWORD = os.environ['DB_PASSWORD']

DB_NAME = config['postgres']['DB_NAME']
DB_HOST = config['postgres']['HOST']
DB_USER = config['postgres']['USER']
DB_PASSWORD = config['postgres']['PASSWORD']

CONNECTION_STRING = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

connection = psycopg2.connect(CONNECTION_STRING)
cursor = connection.cursor()


class Imdb_Queries:

    def director_to_movie(self, director_name):
        logger.info("Called director_to_movie method")
        movie_data = {}
        try:
            if isinstance(director_name, str):
                condition_query = """ SELECT DISTINCT m.movie_name
                FROM movies m
                JOIN directortomovies dm ON m.movie_id = dm.movie_id
                JOIN directors d ON dm.director_id = d.director_id
                WHERE d.director_name = %s
                """
                cursor.execute(condition_query, (director_name,))
                result = cursor.fetchall()
                movies = []
                for mov in result:
                    movies.append(mov[0])
                movie_data["movie_name"] = movies
                return movie_data
            else:
                print(director_name)
                condition_query = f"""
                SELECT DISTINCT m.movie_name,d.director_name
                FROM movies m
                JOIN directortomovies dm ON m.movie_id = dm.movie_id
                JOIN directors d ON dm.director_id = d.director_id
                WHERE d.director_name in {tuple(director_name)}
                """
                cursor.execute(condition_query)
                result = cursor.fetchall()
                # print(result)
                directors_result = {"movies_names": {q_director: [] for q_director in director_name}}
                for q_director in director_name:
                    for mov, r_director in result:
                        # print(mov,r_director)
                        if r_director == q_director:
                            directors_result["movies_names"][q_director].append(mov)
                return directors_result
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in director_to_movie ", ERROR)

    def movie_details(self, movie_name):
        logger.info("Called movie_details method")
        try:
            if isinstance(movie_name, str):
                condition_query = """
                SELECT movie_id,movie_name,movie_url,
                user_reviews,awards_nominees 
                FROM Movies 
                WHERE movie_name = %s
                """
                cursor.execute(condition_query, (movie_name,))
                result = cursor.fetchall()
                movies = {}
                for row in result:
                    movies['movie_id'] = row[0]
                    movies['movie_name'] = row[1]
                    movies['movie_url'] = row[2]
                    movies['user_reviews'] = row[3]
                    movies['awards_nominees'] = row[4]
                return movies
            else:
                condition_query = f"""
                                SELECT movie_id,movie_name,movie_url,
                                user_reviews,awards_nominees
                                FROM Movies
                                WHERE movie_name in {tuple(movie_name)}
                                """
                cursor.execute(condition_query, (movie_name,))
                result = cursor.fetchall()
                movies_list = {"movie_data": []}
                for mov in movie_name:
                    movie_sub_list = {}
                    for mov_data in result:
                        if mov_data[1] == mov:
                            movie_sub_list['movie_id'] = mov_data[0]
                            movie_sub_list['movie_name'] = mov_data[1]
                            movie_sub_list['movie_url'] = mov_data[2]
                            movie_sub_list['user_reviews'] = mov_data[3]
                            movie_sub_list['awards_nominees'] = mov_data[4]
                    movies_list["movie_data"].append(movie_sub_list)
                return movies_list
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in movie_details ", ERROR)

    def roles_to_movies(self, role_name):
        logger.info("Called roles_to_movies method")
        try:
            if isinstance(role_name, str):
                condition_query = """
                SELECT m.movie_name from movies m 
                JOIN rolestomovies rm ON m.movie_id = rm.movie_id
                JOIN roles r ON rm.role_id = r.role_id
                WHERE roles = %s
                """
                cursor.execute(condition_query, (role_name,))
                result = cursor.fetchall()
                movie_details = {}
                movie_details = {'movie_name': {role_name: []}}
                for mov in result:
                    movie_details["movie_name"][role_name].append(mov[0])
                return movie_details
            else:
                condition_query = f"""
                SELECT r.roles,m.movie_name from movies m 
                JOIN rolestomovies rm ON m.movie_id = rm.movie_id
                JOIN roles r ON rm.role_id = r.role_id
                WHERE roles in {tuple(role_name)}
                """
                cursor.execute(condition_query, (role_name,))
                result = cursor.fetchall()
                movie_list = {"movie_names": {q_role: [] for q_role in role_name}}
                for q_role in role_name:
                    for role, mov in result:
                        if role == q_role:
                            movie_list["movie_names"][q_role].append(mov)
                return movie_list
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in roles_to_movies ", ERROR)

    def actors_movies_roles(self, actor_name):
        logger.info("Called actors_movies_roles method")
        try:
            if isinstance(actor_name, str):
                condition_query = """
                SELECT DISTINCT m.movie_name,r.roles
                FROM movies m
                JOIN rolestomovies rm ON m.movie_id = rm.movie_id
                JOIN roles r ON rm.role_id = r.role_id
                JOIN rolestoactor ra ON r.role_id = ra.role_id
                JOIN actors a ON ra.actor_id = a.actor_id
                WHERE a.actor_name = %s;
                """
                cursor.execute(condition_query, (actor_name,))
                result = cursor.fetchall()
                movie_details = {"movies": [],
                                 "roles": []}
                for i, v in result:
                    movie_list = []
                    role_list = []
                    movie_list.append(i)
                    role_list.append(v)
                    movie_details["movies"].extend(movie_list)
                    movie_details["roles"].extend(role_list)
                return movie_details
            else:
                condition_query = f"""
                SELECT DISTINCT m.movie_name,r.roles,a.actor_name
                FROM movies m
                JOIN rolestomovies rm ON m.movie_id = rm.movie_id
                JOIN roles r ON rm.role_id = r.role_id
                JOIN rolestoactor ra ON r.role_id = ra.role_id
                JOIN actors a ON ra.actor_id = a.actor_id
                WHERE a.actor_name in {tuple(actor_name)};
                """
                cursor.execute(condition_query, (actor_name,))
                result = cursor.fetchall()
                movies = {}
                movie_details = {actor: {"movie_name": [],
                                         "roles": []} for actor in actor_name}
                for actor in actor_name:
                    for mov, role, act in result:
                        movie_list = []
                        roles_list = []
                        if act == actor:
                            # print(act)
                            movie_list.append(mov)
                            roles_list.append(role)
                            movie_details[actor]["movie_name"].extend(movie_list)
                            movie_details[actor]["roles"].extend(roles_list)
                return movie_details
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in actors_movies_roles ", ERROR)

    def movies_cast(self, movie_name):
        logger.info("Called movies_cast method")
        try:
            if isinstance(movie_name, str):
                condition_query = """
                SELECT a.actor_name, m.movie_name
                FROM actors a 
                JOIN actorstomovies am ON a.actor_id = am.actor_id
                JOIN movies m ON am.movie_id = m.movie_id
                where movie_name = %s
                """
                cursor.execute(condition_query, (movie_name,))
                result = cursor.fetchall()
                movie_cast = {"cast": {movie_name: []}}
                for actor, mov in result:
                    actors_list = []
                    actors_list.append(actor)
                    movie_cast['cast'][mov].extend(actors_list)
                return movie_cast
            else:
                condition_query = f"""
                SELECT a.actor_name,m.movie_name
                FROM actors a 
                JOIN actorstomovies am ON a.actor_id = am.actor_id
                JOIN movies m ON am.movie_id = m.movie_id
                where movie_name in {tuple(movie_name)}
                """
                cursor.execute(condition_query, (movie_name,))
                result = cursor.fetchall()
                logger.info(f'{len(result)} objects obtained')
                movie_cast = {"cast": {movie: [] for movie in movie_name}}
                for mov in movie_name:
                    actor_list = []
                    for cast, movie in result:
                        if movie == mov:
                            actor_list.append(cast)
                    movie_cast["cast"][mov].extend(actor_list)
                return movie_cast
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in movies_cast ", ERROR)

    def movie_reviews(self, movie_name):
        logger.info("Called movie_reviews method")
        try:
            if isinstance(movie_name, str):
                condition_query = """
                SELECT user_reviews, critic_reviews
                FROM movies
                where movie_name = %s
                """
                cursor.execute(condition_query, (movie_name,))
                result = cursor.fetchall()
                reviews = {}
                for row in result:
                    reviews['user_reviews'] = row[0]
                    reviews['critic_reviews'] = row[1]
                return reviews
            else:
                condition_query = f"""
                SELECT user_reviews, critic_reviews,movie_name
                FROM movies
                where movie_name in {tuple(movie_name)}
                """
                cursor.execute(condition_query, (movie_name,))
                result = cursor.fetchall()
                review = {"movie_name": {movie: {} for movie in movie_name}}
                for mov in movie_name:
                    for user_rev, crit_rev, mov_name in result:
                        if mov_name == mov:
                            review["movie_name"][mov]["user_reviews"] = user_rev
                            review["movie_name"][mov]["critic_reviews"] = crit_rev
                return review
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in movie_details ", ERROR)

