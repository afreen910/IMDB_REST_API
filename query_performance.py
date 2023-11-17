
import psycopg2
import time

CONNECTION_STRING = ''
connection = psycopg2.connect(CONNECTION_STRING)
cursor = connection.cursor()

query_nested = """
            select movie_name from movies where movie_id in (select movie_id from directortomovies where director_id in
            (select director_id from directors where director_name  = 'James Cameron'))
        """
query_join = """
            SELECT DISTINCT m.movie_name
            FROM movies m
            JOIN directortomovies dm ON m.movie_id = dm.movie_id
            JOIN directors d ON dm.director_id = d.director_id
            WHERE d.director_name = 'James Cameron';
            """

def counter(query):
    # Enable timing
    start_time = time.perf_counter()

    # Execute the SQL query
    cursor.execute(query)

    # Fetch the results
    results = cursor.fetchall()

    # Calculate the execution time
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f'time taken by nested query: {execution_time}')


counter(query_nested)
counter(query_join)