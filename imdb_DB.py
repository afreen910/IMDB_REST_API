from typing import Union, Any
import toml
import psycopg2
from movie_finder import load_file, converter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = toml.load("./config.toml")

DB_NAME = config['postgres']['DB_NAME']
DB_USER = config['postgres']['USER']
DB_PASSWORD = config['postgres']['PASSWORD']
DB_HOST = config['postgres']['HOST']

CONNECTION_STRING = f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
connection = psycopg2.connect(CONNECTION_STRING)
cursor = connection.cursor()


def table_creation():
    table_create_query = """
     CREATE TABLE ActorsToMovies(
                            actor_id int,
                            movie_id  varchar,
                            FOREIGN KEY(actor_id)
                            REFERENCES Actors(actor_id)
                            ON UPDATE CASCADE ON DELETE CASCADE,
                            FOREIGN KEY(movie_id)
                            REFERENCES Movies(movie_id)
                            ON UPDATE CASCADE ON DELETE CASCADE
                );
    CREATE TABLE RolesToActor(
                                role_id int ,
                                actor_id int,
                                FOREIGN KEY(role_id)
                                REFERENCES Roles(role_id)
                                ON UPDATE CASCADE ON DELETE CASCADE,
                                FOREIGN KEY(actor_id)
                                REFERENCES Actors(actor_id)
                                ON UPDATE CASCADE ON DELETE CASCADE
        );
    CREATE TABLE Actors(
                            actor_id serial NOT NULL PRIMARY KEY,
                            actor_name  varchar
        );
    CREATE TABLE Movies(
                            movie_id varchar NOT NULL PRIMARY KEY,
                            movie_name  varchar,
                            movie_url varchar,
                            user_reviews int,
                            critic_reviews int,
                            awards_nominees varchar
        );
    CREATE TABLE Roles(
                          role_id serial NOT NULL PRIMARY KEY,
                          roles  varchar
        );
    CREATE TABLE RolesToMovies(
                        role_id int,
                        movie_id  varchar,
                        FOREIGN KEY(role_id)
                        REFERENCES Roles(role_id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY(movie_id)
                        REFERENCES Movies(movie_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
        );
     CREATE TABLE WriterToMovies(
                        writer_id int,
                        movie_id  varchar,
                        FOREIGN KEY(writer_id)
                        REFERENCES Writers(writer_id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY(movie_id)
                        REFERENCES Movies(movie_id)
                        ON UPDATE CASCADE ON DELETE CASCADE
        );
     CREATE TABLE DirectorToMovies(
                                director_id int ,
                                movie_id varchar,
                                FOREIGN KEY(director_id)
                                REFERENCES Directors(director_id)
                                ON UPDATE CASCADE ON DELETE CASCADE,
                                FOREIGN KEY(movie_id)
                                REFERENCES Movies(movie_id)
                                ON UPDATE CASCADE ON DELETE CASCADE
        );
    CREATE TABLE Writers(
                           writer_id serial NOT NULL PRIMARY KEY,
                            writer_name  varchar
        );
    CREATE TABLE Directors(
                           director_id serial NOT NULL PRIMARY KEY,
                           director_name varchar
       );

"""
    try:
        cursor.execute(table_create_query)
        connection.commit()
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in table_creation ", ERROR)


def movies_insert():
    table_insert_query = "insert into Movies(movie_id,movie_name,movie_url,user_reviews,critic_reviews," \
                         "awards_nominees) values(%s,%s,%s,%s,%s,%s)"
    data = load_file()
    for mov in data:
        data_values = []
        data_values.append(mov['movie_id'])
        data_values.append(mov['movie_name'])
        data_values.append(mov['url'])
        data_values.append(converter(mov['user_reviews']))
        data_values.append(converter((mov['critic_reviews'])))
        data_values.append(mov['awards_and_nominees'])
        try:
            cursor.execute(table_insert_query, data_values)
            connection.commit()
        except(Exception, psycopg2.Error) as ERROR:
            logger.error("Error in movie_insert ", ERROR)


def directors_insert():
    data = load_file()
    dir_data = []
    for director in data:
        dir_data.extend(director['directors'])
    try:
        insert_sql = "INSERT INTO Directors (director_name) VALUES (%s)"
        dir_tuple = [(name,) for name in dir_data]
        cursor.executemany(insert_sql, dir_tuple)
        connection.commit()
    except(Exception, psycopg2.Error) as ERROR:
        print("Error in directors_insert ", ERROR)


def writers_insert():
    data = load_file()
    wri_data = []
    for writer in data:
        wri_data.extend(writer['writers'])
    try:
        insert_query = "insert into Writers(writer_name) values(%s)"
        writer_tuple = [(name,) for name in wri_data]
        cursor.executemany(insert_query, writer_tuple)
        connection.commit()
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in writers_insert ", ERROR)


def actors_insert():
    data = load_file()
    act_data = []
    for actor in data:
        for j in actor['cast']:
            act_data.append(j['actor_name'])
    try:
        insert_query = "insert into Actors(actor_name) values(%s)"
        actor_tuple = [(name,) for name in act_data]
        cursor.executemany(insert_query, actor_tuple)
        connection.commit()
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in actors_insert ", ERROR)


def roles_insert():
    data = load_file()
    role_data = []
    for role in data:
        for j in role['cast']:
            role_data.append(j['role'])
    try:
        insert_query = "insert into Roles(roles) values(%s)"
        role_tuple = [(name,) for name in role_data]
        cursor.executemany(insert_query, role_tuple)
        connection.commit()
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in roles_insert ", ERROR)


def util_func(query, cursor):
    cursor.execute(query)
    return cursor.fetchall()


def actors_to_movies_insert(cursor):
    data = load_file()
    try:
        insert_query = "insert into ActorsToMovies(actor_id,movie_id) values(%s,%s)"
        read_query = """select actor_id,actor_name from actors;
        """
        actor_details = util_func(read_query, cursor)
        data_tuple = []
        for act_id, name in actor_details:
            for mov in data:
                for actor in mov['cast']:
                    if name in actor['actor_name']:
                        data_tuple.append((act_id, mov['movie_id']))
        return insert_query, data_tuple
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in roles_insert ", ERROR)


def directors_to_movies_insert(cursor):
    data = load_file()
    try:
        insert_query = "insert into DirectorToMovies(director_id,movie_id) values(%s,%s)"
        read_query = "select director_id,director_name from directors;"
        director_details = util_func(read_query, cursor)
        data_tuple = []
        for dir_id, name in director_details:
            for mov in data:
                if name in mov['directors']:
                    data_tuple.append((dir_id, mov['movie_id']))
        return insert_query, data_tuple
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in directors_to_movies_insert ", ERROR)


def writers_to_movies_insert(cursor):
    data = load_file()
    try:
        insert_query = "insert into WriterToMovies(movie_id,writer_id) values(%s,%s)"
        read_query = "select writer_id,writer_name from writers;"
        writer_details = util_func(read_query, cursor)
        data_tuple = []
        for writer_id, name in writer_details:
            for mov in data:
                if name in mov['writers']:
                    data_tuple.append((mov['movie_id'], writer_id))
        return insert_query, data_tuple
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in writers_to_movies_insert ", ERROR)


def roles_to_movies_insert(cursor):
    data = load_file()
    try:
        insert_query = "insert into RolesToMovies(movie_id,role_id) values(%s,%s)"
        read_query = "select role_id,roles from roles;"
        role_details = util_func(read_query, cursor)
        data_tuple = []
        for role_id, name in role_details:
            for mov in data:
                for rol in mov['cast']:
                    if name == rol['role']:
                        data_tuple.append((mov['movie_id'], role_id))
        return insert_query, data_tuple
    except(Exception, psycopg2.Error) as ERROR:
        logger.error("Error in roles_to_movies_insert ", ERROR)


def Roles_to_actors_insert(cursor):
    data = load_file()
    try:
        insert_query = "insert into RolesToActor(actor_id,role_id) values(%s,%s)"
        role_query = "select role_id,roles from roles;"
        role_details = util_func(role_query, cursor)
        actor_query = "select actor_id,actor_name from actors"
        actor_details = util_func(actor_query, cursor)
        role_id_map = {}
        for id, map in role_details:
            role_id_map[map] = id
        data_tuple = []
        for i, v in actor_details:
            for mov in data:
                for rol in mov['cast']:
                    if v == rol['actor_name']:
                        data_tuple.append((i, role_id_map[rol['role']]))
        return insert_query, data_tuple
    except(Exception, psycopg2.Error) as ERROR:
        print("Error in roles_insert ", ERROR)


if __name__ == '__main__':
    cursor = connection.cursor()
    # actor_movie_query, actor_movie_tup = actors_to_movies_insert(cursor)
    # director_movie_query, director_movie_tup = directors_to_movies_insert(cursor)
    # writer_movie_query, writer_movie_tup = writers_to_movies_insert(cursor)
    # role_actor_query, role_actor_tup = Roles_to_actors_insert(cursor)
    # role_movie_query, role_movies_tup = Roles_to_movies_insert(cursor)
    batch_size = 5000
    for i in range(0, len(writer_movie_tup), batch_size):
        logger.info(f"Inserting batch {i}")
        batch_data = writer_movie_tup[i: i + batch_size]
        cursor.executemany(writer_movie_query, batch_data)
        logger.info(f"{i + batch_size} data is inserted")
        connection.commit()
    logger.info("All records are inserted")
    if cursor:
        cursor.close()

"""
(removes duplicate data from the database)r
delete from Directors where director_id not in 
    (select min(director_id) from directors group by director_name )
"""
